from fastapi import FastAPI
from app.api import router

app = FastAPI(title="HabbitTaskTracker")
app.include_router(router)
