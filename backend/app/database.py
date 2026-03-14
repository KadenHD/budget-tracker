from app.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

config = Config()

engine = create_engine(config.POSTGRES_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

# usage => def my_func(db: Session = Depends(get_db)):
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
