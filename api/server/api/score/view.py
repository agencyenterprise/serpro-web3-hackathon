from api.application.use_cases.compute_loan_score_v1.compute_loan_score_v1_use_case import (
    ComputeLoanScoreV1UseCase,
)
from api.application.use_cases.compute_score_v1.compute_score_v1_use_case import (
    ComputeScoreV1UseCase,
)
from api.application.use_cases.save_score_v1.save_score_v1_use_case import (
    SaveScoreV1UseCase,
)
from api.domain.use_cases.compute_loan_score.compute_loan_score_use_case import (
    ComputeLoanScoresUseCase,
    LoanScoreIn,
    LoanScoreOut,
)
from api.domain.use_cases.compute_score.compute_score_use_case import (
    ComputeScoresUseCase,
    ScoreIn,
)
from api.domain.use_cases.save_score.list_loan_transactions_use_case import (
    SaveScoreIn,
    SaveScoreOut,
    SaveScoresUseCase,
)
from api.server.api.router import get_router

router = get_router()


@router.post("/")
async def save_score(
    use_case_in: SaveScoreIn,
) -> SaveScoreOut:
    use_case_out = await SaveScoresUseCase(adapter=SaveScoreV1UseCase()).execute(
        use_case_in=use_case_in
    )
    return use_case_out


@router.get("/loan/{address}")
async def compute_loan_score(
    address: str,
) -> LoanScoreOut:
    use_case_in = LoanScoreIn(address=address, k=5)
    use_case_out = await ComputeLoanScoresUseCase(
        adapter=ComputeLoanScoreV1UseCase()
    ).execute(use_case_in=use_case_in)
    return use_case_out


@router.post("/complete")
async def compute_loan_score(
    use_case_in: ScoreIn,
) -> LoanScoreOut:
    use_case_out = await ComputeScoresUseCase(adapter=ComputeScoreV1UseCase()).execute(
        use_case_in=use_case_in
    )
    return use_case_out
