import uuid
from collections.abc import AsyncGenerator
from datetime import UTC, datetime

from sqlalchemy import UUID, Column, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.services.config import Config

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
        default=lambda: datetime.now(UTC)
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)
    )

class BaseModel(IDMixin, TimestampMixin):
    __abstract__ = True

Base = declarative_base(cls=BaseModel)

# NOTE: async def mymethod(db: Annotated[AsyncSession, Depends(get_db)]):
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        yield db
