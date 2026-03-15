from fastapi import APIRouter
import psycopg2
from app.config import Config
from app.mailer import get_smtp
from app.schemas import MessageType

config = Config()

router = APIRouter(
    tags=["defaults"],
)

@router.get("/")
def get_root():
    if config.DEBUG:
        return {"config": config, "status": MessageType.OK}
    return {"status": MessageType.OK}

@router.get("/health")
def health():
    try:
        conn = psycopg2.connect(config.POSTGRES_URL)
        conn.close()
        db_status = MessageType.OK
    except Exception:
        db_status = MessageType.ERROR

    try:
        with get_smtp():
            pass
        mail_status = MessageType.OK
    except Exception:
        mail_status = MessageType.ERROR


    return {
        "status": MessageType.OK,
        "database": db_status,
        "mailer": mail_status,
    }

@router.get("/ping")
def ping():
    return MessageType.PONG
