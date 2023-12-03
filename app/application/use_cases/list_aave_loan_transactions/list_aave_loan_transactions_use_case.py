from typing import List
from app.application.use_cases.controllers.loan_transactions_controller import (
    LoanTransactionController,
)
from app.domain.entities.loan_transactions import LoanTransaction
from app.domain.shared_ports.loan_transaction_ports import LoanTransactionPorts


class ListAAVELoanTransactionUseCase(LoanTransactionPorts):
    async def list(self, address: str, k: int = 5, **kwargs) -> List[LoanTransaction]:
        controller = LoanTransactionController()
        transactions = await controller.list_transactions(address, k)
        return [LoanTransaction(**transaction) for transaction in transactions]
