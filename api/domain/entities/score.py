from typing import List, Union
from pydantic import BaseModel
from api.domain.entities.base import BaseEntity


class Score(BaseEntity):
    address: str
    score: float


class ComputedScore(BaseModel):
    score: Union[float, List[float]]


class LoanScore(ComputedScore):
    score: List[float]


class TransactionScore(ComputedScore):
    score: float


class HoldingsScore(ComputedScore):
    score: float


class CompleteScore(Score):
    score: float
    loan_score: float
    transaction_score: float
    holdings_score: float
