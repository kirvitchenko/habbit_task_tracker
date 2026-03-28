import redis.asyncio as redis

from app.core.config import REDIS_DB, REDIS_PORT, REDIS_HOST


async def create_redis_client():
    client = redis.Redis(
        db=REDIS_DB,
        port=REDIS_PORT,
        host=REDIS_HOST,
        decode_responses=True,
        max_connections=10
    )
    return client

async def close_redis_client(client: redis.Redis):
    await client.close()