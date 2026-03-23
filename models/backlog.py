from sqlalchemy import Column, Integer

from db.base import Base


class BacklogTaskModel(Base):
    __tablename__ = 'backlog_tasks'

    id = Column(Integer, primary_key=True)
