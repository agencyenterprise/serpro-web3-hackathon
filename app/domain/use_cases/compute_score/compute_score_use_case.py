from typing import Union
from pydantic import BaseModel, Field
from app.domain.shared_ports.score_ports import ScorePorts


class ScoreIn(BaseModel):
    address: str
    k: int = Field(5, ge=5, le=5)
    eth_balance: float
    nfts_held: int
    account_age: int
    erc20_tokens: float


class ScoreOut(BaseModel):
    score: Union[float, list[float]]


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
            k=use_case_in.k,
        )
        return ScoreOut(
            score=score.score,
        )
