import logging
from typing import Optional
from fastapi.concurrency import run_in_threadpool
from api.application.model.score import ScoreModel
from api.application.use_cases.controllers.score_controller import ScoreController
from api.application.use_cases.controllers.loan_transactions_controller import (
    LoanTransactionController,
)
from api.application.model.db import session
from api.domain.entities.score import CompleteScore, Score
from tensorflow import keras
from keras.models import load_model, Model
import numpy as np
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
from api.domain.shared_ports.score_ports import ScorePorts

model: Model = load_model(
    "./api/application/use_cases/compute_loan_score_v1/zscore_complete.h5"
)


class ComputeScoreV1UseCase(ScorePorts):
    async def compute_score(
        self,
        address: str,
        eth_balance: float,
        nfts_held: int,
        account_age: float,
        erc20_tokens: float,
        k: int = 5,
        **kwargs,
    ) -> CompleteScore:
        loan_transaction_controller = LoanTransactionController()
        score_controller = ScoreController()
        transactions = await loan_transaction_controller.list_transactions(address, k)
        input_features = np.array(
            [
                [
                    transaction.total_collateral_eth,
                    transaction.current_liquidation_threshold,
                    transaction.available_borrows_eth,
                    transaction.total_debt_eth,
                ]
                for transaction in transactions
            ]
        )
        if len(input_features):
            loan_score = await run_in_threadpool(
                model.predict, input_features[np.newaxis, :]
            )
            loan_score = loan_score[0].tolist()[0]
        else:
            loan_score = 0.75
        logging.info(f"Loan score: {loan_score}")
        holdings_score = await score_controller.compute_holdings_score(
            eth_balance, nfts_held, account_age, erc20_tokens
        )
        logging.info(f"Holdings score: {holdings_score}")
        transaction_score = await score_controller.compute_transaction_score(
            address, holdings_score
        )
        logging.info(
            f"Transaction score: {transaction_score}, Holdings score: {holdings_score}, Loan score: {loan_score}"
        )
        score_model = ScoreModel(
            address=address,
            score=max((holdings_score + transaction_score) * loan_score, 10),
        )
        async with session() as db_session:
            # Check if a record with the given address already exists
            stmt = select(ScoreModel).where(ScoreModel.address == address)
            try:
                existing_record = await db_session.execute(stmt)
                existing_record = existing_record.scalar_one()
                # Update existing record
                existing_record.score = score_model.score
            except NoResultFound:
                # No existing record, so add a new one
                db_session.add(score_model)

            # Commit the transaction
            await db_session.commit()
        return CompleteScore(
            address=score_model.address,
            score=score_model.score,
            transaction_score=transaction_score,
            loan_score=loan_score,
            holdings_score=holdings_score,
            id=score_model.id,
            created_at=score_model.created_at,
            updated_at=score_model.updated_at,
        )
