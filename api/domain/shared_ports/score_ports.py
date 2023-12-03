from abc import ABCMeta
from typing import Optional
from api.domain.entities.score import HoldingsScore, LoanScore, Score


class ScorePorts(metaclass=ABCMeta):
    async def save(
        self,
        address: str,
        score: float,
        **kwargs,
    ) -> Score:
        raise NotImplementedError

    async def compute_loan_score(
        self,
        address: str,
        k: int,
        **kwargs,
    ) -> LoanScore:
        raise NotImplementedError

    async def compute_score(
        self,
        address: str,
        eth_balance: Optional[float] = None,
        nfts_held: Optional[int] = None,
        account_age: Optional[int] = None,
        erc20_tokens: Optional[float] = None,
        k: int = 5,
        **kwargs,
    ) -> HoldingsScore:
        raise NotImplementedError
