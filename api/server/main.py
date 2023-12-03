import uvicorn
from fastapi import FastAPI
from api.config import settings
from fastapi.middleware.cors import CORSMiddleware
from api.server.api.loan.view import router as loan_router
from api.server.api.score.view import router as score_router


app = FastAPI(
    docs_url="/docs/",
    openapi_url=f"/api/v1/openapi.json",
)

app.include_router(loan_router, prefix="/api/v1/loan", tags=["loan"])
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=58000, reload=False)
