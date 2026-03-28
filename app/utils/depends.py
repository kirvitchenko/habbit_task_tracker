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
    async with SessionLocal() as session:
        yield session

async def get_redis_client(request: Request):
    return request.app.state.redis_client

async def get_redis_service(redis_client: redis.Redis = Depends(get_redis_client)):
    return RedisService(client=redis_client)

async def get_redis_task_service(redis_client: redis.Redis = Depends(get_redis_client)):
    return TaskRedisService(client=redis_client)

async def get_redis_category_service(redis_client: redis.Redis = Depends(get_redis_client)):
    return CategoryRedisService(client=redis_client)

async def get_task_service(db: AsyncSession = Depends(get_async_db),
                           cache: RedisService = Depends(get_redis_task_service)) -> TaskService:
    repo = TaskRepository(db)
    return TaskService(repo=repo, cache=cache)

async def get_category_service(db: AsyncSession = Depends(get_async_db),
                               cache: RedisService = Depends(get_redis_category_service)) -> CategoryService:
    repo = CategoryRepository(db)
    return CategoryService(repo=repo, cache=cache)
