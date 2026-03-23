import enum

from sqlalchemy import Column, Integer, String, Text, Date, Enum

from db.base import Base


class TaskStatusChoices(enum.Enum):
    new = 'new'
    processed = 'processed'
    done = 'done'


class CurrentTaskModel(Base):
    __tablename__ = 'tasks'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(100))
    description: str = Column(Text, nullable=True)
    date = Column(Date)
    status = Column(Enum(TaskStatusChoices), default=TaskStatusChoices.new)

