from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, PositiveInt, Field

from app.models.task import TaskStatusChoices
from app.schemas.category import CategoryViewSchema


class BaseTaskSchema(BaseModel):
    title: str = Field(max_length=100)
    description: Optional[str] = None
    due_date: Optional[date] = None
    deadline: Optional[date] = None
    status: Optional[TaskStatusChoices] = None


class TaskViewSchema(BaseTaskSchema):
    id: PositiveInt
    created_at: datetime
    category: Optional[CategoryViewSchema] = None


class TaskUpdateSchema(BaseTaskSchema):
    category_id: Optional[int] = None
