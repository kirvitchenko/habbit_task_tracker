"""SQLALCHEMY  session settings"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import DB_ASYNC_DSN

async_engine = create_async_engine(url=DB_ASYNC_DSN)
SessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession)
