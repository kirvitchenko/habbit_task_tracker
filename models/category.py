from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base
from models.mixins import IdAndCreatedMixin


class CategoryModel(IdAndCreatedMixin, Base):
    __tablename__ = "categories"

    title = Column(String(100))
    tasks = relationship(
        "models.task.TaskModel", back_populates="category", uselist=True
    )
