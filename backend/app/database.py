from app.config import Config
from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

config = Config()

engine = create_engine(config.POSTGRES_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

class TimestampMixin:
    __abstract__ = True

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

Base = declarative_base(cls=TimestampMixin)

# usage => def my_func(db: Session = Depends(get_db)):
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
