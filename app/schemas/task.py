from datetime import datetime

from pydantic import BaseModel, PositiveInt, Field

from app.models.task import TaskStatusChoices


class BaseTaskSchema(BaseModel):
    title: str = Field(max_length=100)
    description: str | None
    due_date: datetime
    deadline: datetime
    status: TaskStatusChoices


class TaskViewSchema(BaseTaskSchema):
    id: PositiveInt
    created_at: datetime


class TaskUpdateSchema(BaseTaskSchema):
    pass
