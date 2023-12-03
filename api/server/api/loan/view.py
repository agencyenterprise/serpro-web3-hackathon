from fastapi import APIRouter
from api.application.use_cases.list_aave_loan_transactions.list_aave_loan_transactions_use_case import (
    ListAAVELoanTransactionUseCase,
)
from api.domain.use_cases.list_loan_transactions.list_loan_transactions_use_case import (
    ListLoanTransactionIn,
    ListLoanTransactionOut,
    ListLoanTransactionsUseCase,
)
from api.server.api.router import get_router


router = get_router()


@router.post("/")
async def save_artifacts(
    use_case_in: ListLoanTransactionIn,
) -> ListLoanTransactionOut:
    use_case_out = await ListLoanTransactionsUseCase(
        adapter=ListAAVELoanTransactionUseCase()
    ).execute(use_case_in=use_case_in)
    return use_case_out
