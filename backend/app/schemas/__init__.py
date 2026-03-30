from datetime import datetime

from pydantic import UUID4, BaseModel


class IDMixin(BaseModel):
    id: UUID4

class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime

class Mixin(IDMixin, TimestampMixin):
    pass


class MessageResponse(BaseModel):
    message: str

class StatusResponse(BaseModel):
    status: str

class HealthResponse(BaseModel):
    status: str
    database: str
    mailer: str
