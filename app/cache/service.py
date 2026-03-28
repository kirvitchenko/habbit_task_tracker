import json
from typing import Any

import redis.asyncio as redis


class RedisService:
    model_key = None

    def __init__(self, client: redis.Redis):
        self.client = client

    async def get(self, obj_id: int):
        data = await self.client.hget(name=self.model_key, key=str(obj_id))
        if data:
            return json.loads(data)
        return None

    async def get_list(self):
        data = await self.client.hgetall(name=self.model_key)
        return {k: json.loads(v) for k, v in data.items()}

    async def set(self, obj_id:int, value: Any, ttl: int = 300):
        await self.client.hset(name=self.model_key, key=str(obj_id), value=json.dumps(value))
        await self.client.expire(name=self.model_key, time=ttl)

    async def delete(self, obj_id):
        await self.client.hdel(name=self.model_key, key=str(obj_id))

    async def delete_all(self):
        return await self.client.delete(name=self.model_key)

class TaskRedisService(RedisService):
    model_key = 'task'

class CategoryRedisService(RedisService):
    model_key = 'category'
