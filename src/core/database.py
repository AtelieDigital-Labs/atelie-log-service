from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    connect_args={'options': f'-c search_path={settings.DATABASE_SCHEMA}'},
)


class Base(DeclarativeBase):
    pass


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
