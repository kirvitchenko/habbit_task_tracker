from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import IdAndCreatedMixin


class CategoryModel(IdAndCreatedMixin, Base):
    __tablename__ = "categories"

    title = Column(String(100))
    tasks = relationship(
        "app.models.task.TaskModel", back_populates="category", uselist=True
    )
