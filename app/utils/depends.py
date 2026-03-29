"""Depends on project"""

from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import AsyncGenerator

from app.cache.service import RedisService, TaskRedisService, CategoryRedisService
from app.db.session import SessionLocal
from app.repository.category import CategoryRepository
from app.repository.task import TaskRepository
from app.services.category import CategoryService
from app.services.task import TaskService


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Get db session"""
    async with SessionLocal() as session:
        yield session


def get_redis_client(request: Request) -> redis.Redis:
    """Get redis client"""
    return request.app.state.redis_client


def get_redis_service(
    redis_client: redis.Redis = Depends(get_redis_client),
) -> RedisService:
    """Get base redis service"""
    return RedisService(client=redis_client)


def get_redis_task_service(
    redis_client: redis.Redis = Depends(get_redis_client),
) -> TaskRedisService:
    """Get redis task service"""
    return TaskRedisService(client=redis_client)


def get_redis_category_service(
    redis_client: redis.Redis = Depends(get_redis_client),
) -> CategoryRedisService:
    """Get redis category service"""
    return CategoryRedisService(client=redis_client)


def get_task_service(
    db: AsyncSession = Depends(get_async_db),
    cache: RedisService = Depends(get_redis_task_service),
) -> TaskService:
    """Get task service"""
    repo = TaskRepository(db)
    return TaskService(repo=repo, cache=cache)


def get_category_service(
    db: AsyncSession = Depends(get_async_db),
    cache: RedisService = Depends(get_redis_category_service),
) -> CategoryService:
    """Get category service"""
    repo = CategoryRepository(db)
    return CategoryService(repo=repo, cache=cache)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]
