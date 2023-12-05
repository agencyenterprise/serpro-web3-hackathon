from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from api.application.model.mixin import Base
from sqlalchemy.orm import sessionmaker
from api.config import settings
from sqlalchemy.engine.url import URL

db_url = URL(
    "postgresql+asyncpg",
    username=settings.DATABASE_USER,
    password=settings.DATABASE_PASSWORD,
    host=settings.DATABASE_HOST,
    port=settings.DATABASE_PORT,
    database=settings.DATABASE_NAME,
    query=dict(database=settings.DATABASE_NAME),
)


engine = create_async_engine(db_url)
session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with session() as db_session:  # Use async with for session management
        yield db_session


from api.application.model import score
