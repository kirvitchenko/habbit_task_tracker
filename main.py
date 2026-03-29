from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api import router
from app.cache.connection import create_redis_client, close_redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = create_redis_client()
    app.state.redis_client = redis_client
    yield
    await close_redis_client(redis_client)


app = FastAPI(title="HabbitTaskTracker", lifespan=lifespan)
app.include_router(router)
