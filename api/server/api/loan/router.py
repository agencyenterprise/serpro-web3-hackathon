from fastapi import APIRouter
from api.server.api.router import get_router
from api.server.api.loan.view import router


router = APIRouter(prefix="")

router.include_router(router, prefix="/aave", tags=["aave"])
