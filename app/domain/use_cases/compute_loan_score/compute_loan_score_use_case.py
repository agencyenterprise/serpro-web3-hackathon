from typing import Union
from pydantic import BaseModel
from app.domain.shared_ports.score_ports import ScorePorts


class LoanScoreIn(BaseModel):
    address: str
    k: int


class LoanScoreOut(BaseModel):
    score: Union[float, list[float]]


class ComputeLoanScoresUseCase:
    def __init__(self, adapter: ScorePorts):
        self.adapter = adapter

    async def execute(self, use_case_in: LoanScoreIn) -> LoanScoreOut:
        score = await self.adapter.compute_loan_score(
            address=use_case_in.address, score=use_case_in.k
        )
        return LoanScoreOut(
            score=score,
        )
