import json
from typing import Any, TypeVar, Generic, Type

import redis.asyncio as redis
from pydantic import BaseModel

from app.schemas.category import CategoryViewSchema
from app.schemas.task import TaskViewSchema

BaseSchema = TypeVar('BaseSchema', bound=BaseModel)

class RedisService(Generic[BaseSchema]):
    model_key = None
    pydantic_model: Type[BaseSchema]

    def __init__(self, client: redis.Redis):
        self.client = client

    async def get(self, obj_id: int) -> BaseSchema | None:
        data = await self.client.hget(name=self.model_key, key=str(obj_id))
        if data:
            return self.pydantic_model(**json.loads(data))
        return None

    async def set(self, obj_id:int, value: BaseSchema, ttl: int = 300) -> None:
        await self.client.hset(name=self.model_key, key=str(obj_id), value=json.dumps(value.model_dump(mode='json')))
        await self.client.expire(name=self.model_key, time=ttl)

    async def delete(self, obj_id) -> None:
        await self.client.hdel(name=self.model_key, key=str(obj_id))


class TaskRedisService(RedisService):
    model_key = 'task'
    pydantic_model = TaskViewSchema

class CategoryRedisService(RedisService):
    model_key = 'category'
    pydantic_model = CategoryViewSchema
