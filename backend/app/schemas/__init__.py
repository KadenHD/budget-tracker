from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str

class StatusResponse(BaseModel):
    status: str

class HealthResponse(BaseModel):
    status: str
    database: str
    mailer: str
