from typing import Any
import uvicorn
from fastapi import FastAPI
from api.config import settings
from fastapi.middleware.cors import CORSMiddleware
from api.server.api.score.view import router as score_router


app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    summary=settings.summary,
    docs_url="/docs/",
    openapi_url=f"/api/v1/openapi.json",
)

app.include_router(score_router, prefix="/api/v1", tags=["score"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/")
# def root():
#     return {"status": "ok"}


@app.get(
    f"/healthCheck",
)
async def health() -> Any:
    return {"status": 200, "message": "up and working..."}


@app.get(
    f"/",
)
async def health_v1() -> Any:
    return {"status": 200, "message": "up and working..."}


@app.get(
    f"/health",
)
async def health_v2() -> Any:
    return {"status": 200, "message": "up and working..."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=58000, reload=False)
