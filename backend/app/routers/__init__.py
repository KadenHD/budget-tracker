from fastapi import APIRouter
import psycopg2
from app.config import Config

config = Config()

router = APIRouter(
    tags=["defaults"],
)

@router.get("/")
def get_root():
    if config.DEBUG:
        return {"config": config, "status": "ok"}
    return {"status": "ok"}

@router.get("/health")
def health():
    try:
        conn = psycopg2.connect(config.POSTGRES_URL)
        conn.close()
        db_status = "ok"
    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "database": db_status
    }

@router.get("/ping")
def ping():
    return "pong"
