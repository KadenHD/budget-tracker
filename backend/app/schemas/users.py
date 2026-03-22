from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=20)
    email: EmailStr = Field(..., max_length=120)

    model_config = ConfigDict(str_strip_whitespace=True)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

class UserResponse(UserBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        str_strip_whitespace=True,
        from_attributes=True,
        extra="forbid",
    )

class UserUpdatePassword(BaseModel):
    password: str = Field(..., min_length=8)

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )
