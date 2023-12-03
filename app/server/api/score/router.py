from fastapi import APIRouter
from app.server.api.router import get_router
from app.server.api.score.view import router

router = APIRouter(prefix="")

router.include_router(router, prefix="/score", tags=["score"])
