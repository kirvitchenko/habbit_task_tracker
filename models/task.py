import enum

from sqlalchemy import Column, Integer, String, Text, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class TaskStatusChoices(enum.Enum):
    new = 'new'
    processed = 'processed'
    done = 'done'


class CurrentTaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(Text, nullable=True)
    date = Column(Date)
    status = Column(Enum(TaskStatusChoices), default=TaskStatusChoices.new)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('models.category.CategoryModels', back_populates='tasks')

