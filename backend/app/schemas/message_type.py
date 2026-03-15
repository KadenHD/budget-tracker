from enum import Enum

class MessageType(Enum):
    OK = "ok"
    ERROR = "error"
    PONG = "pong"
