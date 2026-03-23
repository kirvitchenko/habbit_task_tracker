from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class CategoryModel(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    tasks = relationship('models.category.CurrentTaskModel', back_populates='category', uselist=True)