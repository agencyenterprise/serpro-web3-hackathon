from typing import List

from pydantic import BaseModel
from api.domain.entities.loan_transactions import LoanTransaction
from api.domain.shared_ports.loan_transaction_ports import LoanTransactionPorts


class ListLoanTransactionIn(BaseModel):
    address: str
    k: int = 5


class ListLoanTransactionOut(BaseModel):
    transactions: List[LoanTransaction]


class ListLoanTransactionsUseCase:
    def __init__(self, adapter: LoanTransactionPorts):
        self.adapter = adapter

    async def execute(
        self, use_case_in: ListLoanTransactionIn
    ) -> ListLoanTransactionOut:
        artifacts = await self.adapter.list(
            address=use_case_in.address, k=use_case_in.k
        )
        return ListLoanTransactionOut(
            artifacts=artifacts,
        )
