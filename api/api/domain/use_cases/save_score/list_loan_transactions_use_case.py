from pydantic import BaseModel
from api.domain.entities.loan_transactions import LoanTransaction
from api.domain.shared_ports.score_ports import ScorePorts


class SaveScoreIn(BaseModel):
    address: str
    score: float


class SaveScoreOut(BaseModel):
    address: str
    float: float


class SaveScoresUseCase:
    def __init__(self, adapter: ScorePorts):
        self.adapter = adapter

    async def execute(self, use_case_in: SaveScoreIn) -> SaveScoreOut:
        artifacts = await self.adapter.save(
            address=use_case_in.address, score=use_case_in.score
        )
        return SaveScoreOut(
            address=artifacts.address,
            score=artifacts.score,
        )
