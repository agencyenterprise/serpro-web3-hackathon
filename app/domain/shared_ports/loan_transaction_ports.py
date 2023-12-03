from abc import ABCMeta
from typing import List
from app.domain.entities.loan_transactions import LoanTransaction


class LoanTransactionPorts(metaclass=ABCMeta):
    async def list(
        self,
        address: str,
        k: int = 5,
        **kwargs,
    ) -> List[LoanTransaction]:
        raise NotImplementedError
