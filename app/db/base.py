"""Base DB file"""

from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    """Base class for ORM models"""

    pass
