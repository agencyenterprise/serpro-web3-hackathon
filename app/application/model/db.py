from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.application.model.mixin import Base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL)
session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with session() as db_session:  # Use async with for session management
        yield db_session


from app.application.model import score
