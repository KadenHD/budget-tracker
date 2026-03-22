from pydantic import BaseModel, SecretStr

from app.services.config import Config

config = Config()

class Settings:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self.__class__._initialized:
            return

        self.secret_key: SecretStr = SecretStr(config.SECRET_KEY)
        self.algorithm: str = "HS256"
        self.access_token_expire_minutes: int = 30

        self.__class__._initialized = True

class Token(BaseModel):
    access_token: str
    token_type: str
