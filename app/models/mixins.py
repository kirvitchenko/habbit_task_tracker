from datetime import datetime

from sqlalchemy import Column, Integer, DateTime


class IdAndCreatedMixin:
    """Mixin for ID and created_at in models"""

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
