import os
from enum import Enum

from dotenv import load_dotenv


class EnvType(Enum):
    DEVELOPMENT="development"
    PRODUCTION="production"

class Config:
    _instance = None
    _initialized = False

    _development=("development", "dev")
    _production=("production", "prod")
    _true=("true", "yes", "1")
    _false=("false", "no", "0")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self.__class__._initialized:
            return

        load_dotenv()

        self.HOST = os.getenv("APP_HOST", "localhost")
        self.PORT = int(os.getenv("APP_PORT", "5000"))
        self.ENV = self.set_app_env(os.getenv("APP_ENV", "development"))
        self.SECRET_KEY = os.getenv("APP_SECRET_KEY", "mysecretkey")
        self.CORS_ORIGINS = self.set_cors_origins(os.getenv("APP_CORS_ORIGINS", ""))

        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
        self.POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
        self.POSTGRES_USER = os.getenv("POSTGRES_USER", "root")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "root")
        self.POSTGRES_DB = os.getenv("POSTGRES_DB", "default_db")

        self.SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
        self.SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))
        self.SMTP_SECURE = self.set_smtp_secure(os.getenv("SMTP_SECURE", "false"))
        self.SMTP_USER = os.getenv("SMTP_USER", "")
        self.SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

        self.URL = f"http://{self.HOST}:{self.PORT}"
        self.DEBUG = self.ENV == EnvType.DEVELOPMENT.value
        self.POSTGRES_URL = (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

        self.__class__._initialized = True

    def set_smtp_secure(self, smtp_secure: str) -> bool:
        secure = smtp_secure.lower()
        if secure in self._true:
            return True
        if secure in self._false:
            return False
        raise ValueError(f"Invalid SMTP_SECURE: {smtp_secure}")

    def set_app_env(self, app_env: str) -> str:
        env = app_env.lower()
        if env in self._development:
            return EnvType.DEVELOPMENT.value
        if env in self._production:
            return EnvType.PRODUCTION.value
        raise ValueError(f"Invalid APP_ENV: {app_env}")

    def set_cors_origins(self, app_cors_origins: str) -> list[str]:
        return [
            origin.strip()
            for origin in app_cors_origins.split(",")
            if origin.strip()
        ]
