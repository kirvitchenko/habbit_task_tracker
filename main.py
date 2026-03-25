from fastapi import FastAPI
from app.api.v_1.task import router as task_router

app = FastAPI(title="HabbitTaskTracker")
app.include_router(task_router)
