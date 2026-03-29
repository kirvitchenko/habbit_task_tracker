"""Category model in DB"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base import BaseModel
from app.models.mixins import IdAndCreatedMixin


class CategoryModel(IdAndCreatedMixin, BaseModel):
    """ORM category model"""

    __tablename__ = "categories"

    title = Column(String(100))
    tasks = relationship(
        "app.models.task.TaskModel",
        back_populates="category",
        uselist=True,
    )
