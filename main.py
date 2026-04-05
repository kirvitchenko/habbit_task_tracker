from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api import router
from app.cache.connection import create_redis_client, close_redis_client
from app.kafka.connection import create_kafka_connection, close_kafka_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = create_redis_client()
    app.state.redis_client = redis_client
    kafka_producer = await create_kafka_connection()
    app.state.kafka_producer = kafka_producer
    yield
    await close_redis_client(redis_client)
    await close_kafka_client(kafka_producer)


app = FastAPI(title="HabbitTaskTracker", lifespan=lifespan)
app.include_router(router)
