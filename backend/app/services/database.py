from app.services.config import Config
from sqlalchemy import create_engine, Column, DateTime, UUID
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone
import uuid

config = Config()

engine = create_engine(config.POSTGRES_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

class IDMixin:
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

class TimestampMixin:
    __abstract__ = True

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

class BaseModel(IDMixin, TimestampMixin):
    __abstract__ = True

Base = declarative_base(cls=BaseModel)

# usage => def my_func(db: Session = Depends(get_db)):
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
