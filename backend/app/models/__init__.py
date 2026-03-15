from datetime import datetime
from sqlalchemy import Column, DateTime

class TimestampMixin:
    __abstract__ = True

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

__all__ = [
    "TimestampMixin",
]
