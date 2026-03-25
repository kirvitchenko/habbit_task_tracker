import enum

from sqlalchemy import Column, Integer, String, Text, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import BaseModel
from app.models.mixins import IdAndCreatedMixin


class TaskStatusChoices(enum.Enum):
    backlog = "backlog"
    in_process = "in_process"
    done = "done"


class TaskModel(IdAndCreatedMixin, BaseModel):
    __tablename__ = "tasks"

    title = Column(String(100))
    description = Column(Text, nullable=True)
    due_date = Column(Date, nullable=True)
    deadline = Column(Date, nullable=True)
    status = Column(Enum(TaskStatusChoices), default=TaskStatusChoices.backlog)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("app.models.category.CategoryModel", back_populates="tasks")
