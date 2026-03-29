"""Schema for tasks"""

from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, PositiveInt, Field

from app.schemas.category import CategoryViewSchema


class TaskFiltersSchema(BaseModel):
    """Schema for task filters"""

    status: Optional[str] = None
    due_date: Optional[date] = None
    deadline: Optional[date] = None


class BaseTaskSchema(BaseModel):
    """Base schema for task schema"""

    title: str = Field(max_length=100)
    description: Optional[str] = None
    due_date: Optional[date] = None
    deadline: Optional[date] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True


class TaskViewSchema(BaseTaskSchema):
    """View schema for returning task"""

    id: PositiveInt
    created_at: datetime
    category: Optional[CategoryViewSchema] = None


class TaskUpdateSchema(BaseTaskSchema):
    """Schema for updating and creating task"""

    category_id: Optional[int] = None
