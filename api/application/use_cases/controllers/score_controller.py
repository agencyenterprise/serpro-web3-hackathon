from fastapi.concurrency import run_in_threadpool
from api.application.controllers import DBController
from api.application.model.score import ScoreModel
from api.application.model.db import session
from api.application.score import (
    compute_holdings_based_score,
    compute_transaction_based_score,
    extract_payment_data,
)
from api.domain.entities.score import Score


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
        return await compute_holdings_based_score(
            eth_balance,
            nfts_held,
            account_age,
            erc20_tokens,
        )

    async def compute_transaction_score(
        self, address: str, holdings_score: float, **kwargs
    ) -> Score:
        transactions = await extract_payment_data(address)
        return await compute_transaction_based_score(
            transactions_df=transactions,
            user_score=holdings_score,
        )
