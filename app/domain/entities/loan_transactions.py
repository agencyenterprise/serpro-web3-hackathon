from pydantic import BaseModel


class LoanTransaction(BaseModel):
    total_collateral_eth: float
    current_liquidation_threshold: float
    available_borrows_eth: float
    total_debt_eth: float
