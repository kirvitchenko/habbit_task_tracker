"""Redis services for cache"""

import json
from typing import TypeVar, Generic, Type

import redis.asyncio as redis
from pydantic import BaseModel

from app.schemas.category import CategoryViewSchema
from app.schemas.task import TaskViewSchema

BaseSchema = TypeVar("BaseSchema", bound=BaseModel)


class RedisService(Generic[BaseSchema]):
    """
    Base redis class for cache services
    child classes should rewrite attributes:
    model_key -> model name
    pydantic_model -> Pydantic Model to serialize entity
    """

    model_key = None
    pydantic_model: Type[BaseSchema]

    def __init__(self, client: redis.Redis):
        self.client = client

    async def get(self, obj_id: int) -> BaseSchema | None:
        """
        Function to get data from cache
        Needs obj_id to search in cache
        Returns data
        If not data, function should return None
        """
        data = await self.client.hget(name=self.model_key, key=str(obj_id))
        if data:
            return self.pydantic_model(**json.loads(data))
        return None

    async def set(self, obj_id: int, value: BaseSchema, ttl: int = 300) -> None:
        """
        Function to set data in cache
        Needs obj_id and value to set
        Saves data in cache and set ttl - default = 300
        Function return None
        """
        await self.client.hset(
            name=self.model_key,
            key=str(obj_id),
            value=json.dumps(value.model_dump(mode="json")),
        )
        await self.client.expire(name=self.model_key, time=ttl)

    async def delete(self, obj_id) -> None:
        """
        Function to delete data from cache
        Needs obj_id to delete
        Function return None
        """
        await self.client.hdel(name=self.model_key, key=str(obj_id))


class TaskRedisService(RedisService[TaskViewSchema]):
    model_key = "task"
    pydantic_model = TaskViewSchema


class CategoryRedisService(RedisService[CategoryViewSchema]):
    model_key = "category"
    pydantic_model = CategoryViewSchema
