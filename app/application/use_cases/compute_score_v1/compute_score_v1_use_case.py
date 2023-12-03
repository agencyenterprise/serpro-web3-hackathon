import logging
from typing import Optional
from fastapi.concurrency import run_in_threadpool
from app.application.model.score import ScoreModel
from app.application.use_cases.controllers.score_controller import ScoreController
from app.application.use_cases.controllers.loan_transactions_controller import (
    LoanTransactionController,
)
from app.application.model.db import session
from app.domain.entities.score import Score
from tensorflow import keras
from keras.models import load_model, Model
import numpy as np

from app.domain.shared_ports.score_ports import ScorePorts

model: Model = load_model(
    "./app/application/use_cases/compute_loan_score_v1/zscore_complete.h5"
)


class ComputeScoreV1UseCase(ScorePorts):
    async def compute_score(
        self,
        address: str,
        eth_balance: float,
        nfts_held: int,
        account_age: int,
        erc20_tokens: float,
        k: int = 5,
        **kwargs,
    ) -> Score:
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
        loan_score = await run_in_threadpool(
            model.predict, input_features[np.newaxis, :]
        )
        loan_score = loan_score[0].tolist()[0]
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
            score=max((holdings_score + transaction_score) * loan_score, 100),
        )
        async with session() as db_session:
            db_session.add(score_model)
            await db_session.commit()
        return Score(
            address=score_model.address,
            score=score_model.score,
            id=score_model.id,
            created_at=score_model.created_at,
            updated_at=score_model.updated_at,
        )
