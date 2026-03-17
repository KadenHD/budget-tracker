from pydantic import BaseModel, Field, ConfigDict, EmailStr, UUID4
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=20)
    email: EmailStr = Field(..., max_length=120)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=20)
    email: Optional[EmailStr] = Field(None, max_length=120)

    model_config = ConfigDict(extra="forbid")
