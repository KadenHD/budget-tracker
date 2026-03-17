from typing import AsyncGenerator
from app.services.config import Config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import Column, DateTime, UUID
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone
import uuid

config = Config()

engine = create_async_engine(config.POSTGRES_URL.replace("postgresql://", "postgresql+asyncpg://"))

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
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

# async def mymethod(db: Annotated[AsyncSession, Depends(get_db)]):
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        yield db
