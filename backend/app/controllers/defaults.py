import psycopg2
from enum import Enum
from app.services.config import Config
from app.services.mailer import get_smtp

config = Config()

class MessageType(Enum):
    OK = "ok"
    ERROR = "error"
    PONG = "pong"

class DefaultsController:
    def get_root(self):
        if config.DEBUG:
            return {"config": config, "status": MessageType.OK}
        return {"status": MessageType.OK}

    def get_health(self):
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

    def get_ping(self):
        return MessageType.PONG

defaults_controller = DefaultsController()
