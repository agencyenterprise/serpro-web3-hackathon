from typing import Union
from pydantic import BaseModel
from api.domain.shared_ports.score_ports import ScorePorts


class ScoreIn(BaseModel):
    address: str
    eth_balance: float
    nfts_held: int
    account_age: float
    erc20_tokens: float


class ScoreOut(BaseModel):
    score: Union[float, list[float]]
    loan_score: float
    transaction_score: float
    holdings_score: float
    address: str


class ComputeScoresUseCase:
    def __init__(self, adapter: ScorePorts):
        self.adapter = adapter

    async def execute(self, use_case_in: ScoreIn) -> ScoreOut:
        score = await self.adapter.compute_score(
            address=use_case_in.address,
            eth_balance=use_case_in.eth_balance,
            nfts_held=use_case_in.nfts_held,
            account_age=use_case_in.account_age,
            erc20_tokens=use_case_in.erc20_tokens,
        )
        return ScoreOut(
            score=score.score,
            loan_score=score.loan_score,
            transaction_score=score.transaction_score,
            holdings_score=score.holdings_score,
            address=score.address,
        )
