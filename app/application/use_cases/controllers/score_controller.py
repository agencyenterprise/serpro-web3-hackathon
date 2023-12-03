from fastapi.concurrency import run_in_threadpool
from app.application.controllers import DBController
from app.application.model.score import ScoreModel
from app.application.model.db import session
from app.application.score import (
    compute_holdings_based_score,
    compute_transaction_based_score,
    extract_payment_data,
)
from app.domain.entities.score import Score


class ScoreController(DBController):
    async def save_score(self, address: str, score: float, **kwargs) -> ScoreModel:
        async with session() as db_session:
            score_model = ScoreModel(address=address, score=score)
            db_session.add(score_model)
            db_session.commit()
            return score_model

    async def compute_holdings_score(
        self,
        eth_balance: float,
        nfts_held: int,
        account_age: int,
        erc20_tokens: float,
        **kwargs
    ) -> Score:
        return await run_in_threadpool(
            compute_holdings_based_score,
            eth_balance,
            nfts_held,
            account_age,
            erc20_tokens,
        )

    async def compute_transaction_score(
        self, address: str, holdings_score: float, **kwargs
    ) -> Score:
        transactions = await run_in_threadpool(extract_payment_data, address)
        return await run_in_threadpool(
            compute_transaction_based_score,
            transactions_df=transactions,
            user_score=holdings_score,
        )
