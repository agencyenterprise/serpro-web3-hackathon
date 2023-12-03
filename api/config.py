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
    app_name: str = "Hushed Labs Bridge"
    organization: str = "AE Studio"
    version: str = "0.1.0"
    description: str = "Hushed Labs Bridge API"
    logging: LoggingConfig = LoggingConfig(
        level=os.getenv("LOGGING_LEVEL", "INFO") or "INFO",
    )
    DATABASE_URL: str = os.getenv("DATABASE_URL") or "sqlite:///./app.db"
    ALEMBIC_DATABASE_URL: str = (
        os.getenv("DATABASE_URL").replace("postgresql+asyncpg", "postgresql")
        or "sqlite:///./app.db"
    )
    ALCHEMY_API_KEY: str = os.getenv("ALCHEMY_API_KEY")
    NFT_CONTRACT_ADDRESS: str = os.getenv("NFT_CONTRACT_ADDRESS")


settings = Settings()
