from datetime import datetime

from pydantic import BaseModel, PositiveInt, Field, StringConstraints
from sqlalchemy.sql.annotation import Annotated

from models.task import TaskStatusChoices


class BaseCurrentTaskSchema(BaseModel):
    name: str = Field(max_length=100)
    description: str | None
    date: datetime
    status: TaskStatusChoices


class CurrentTaskSchema(BaseCurrentTaskSchema):
    id: PositiveInt


class CurrentTaskUpdateSchema(BaseCurrentTaskSchema):
    pass

