from typing import List
from api.application.use_cases.controllers.loan_transactions_controller import (
    LoanTransactionController,
)
from api.application.use_cases.controllers.score_controller import ScoreController
from api.domain.entities.loan_transactions import LoanTransaction
from api.domain.entities.score import Score
from api.domain.shared_ports.loan_transaction_ports import LoanTransactionPorts


class SaveScoreV1UseCase(LoanTransactionPorts):
    async def save(self, address: str, score: float, **kwargs) -> Score:
        controller = ScoreController()
        score = await controller.save_score(address=address, score=score)
        return Score(**score.__dict__())
