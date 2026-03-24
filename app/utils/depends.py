from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import AsyncGenerator

from app.db.session import SessionLocal


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
