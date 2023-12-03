import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api.server.main:app",
        host="localhost",
        reload=True,
    )
