import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class LoggingConfig(BaseModel):
    level: str = "INFO"
    format: str = "%(asctime)s - %(levelname)s - %(message)s"
    datefmt: str = "%Y-%m-%d %H:%M:%S"


class Settings(BaseSettings):
    app_name: str = "ZScore"
    organization: str = "AE Studio"
    version: str = "0.1.0"
    description: str = "ZScore API - A melhor ferramenta governamental para avaliação de risco de crédito em redes descentralizadas"
    logging: LoggingConfig = LoggingConfig(
        level=os.getenv("LOGGING_LEVEL", "INFO") or "INFO",
    )
    summary: str = "ZScore é uma ferramenta governamental para avaliação de risco de crédito. Através de uma API, o ZScore permite que o governo avalie o risco de crédito de um cidadão, com base em suas transações financeiras em redes descentralizadas."
    DATABASE_URL: str = os.getenv("DATABASE_URL") or "sqlite:///./app.db"
    ALEMBIC_DATABASE_URL: str = (
        os.getenv("DATABASE_URL", "").replace("postgresql+asyncpg", "postgresql")
        or "sqlite:///./app.db"
    )
    ALCHEMY_API_KEY: str = os.getenv("ALCHEMY_API_KEY")
    NFT_CONTRACT_ADDRESS: str = os.getenv("NFT_CONTRACT_ADDRESS")
    ALCHEMY_ENDPOINT: str = os.getenv(
        "ALCHEMY_ENDPOINT", "https://polygon-mumbai.g.alchemy.com/v2/"
    )
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "postgres")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "postgres")


settings = Settings()
