from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, EmailStr, Field


# -----------------------------
# Base schemas
# -----------------------------
class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=20)
    email: EmailStr = Field(..., max_length=120)

    model_config = ConfigDict(str_strip_whitespace=True)


class UserEmailRequest(BaseModel):
    email: EmailStr = Field(..., max_length=120)

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


# -----------------------------
# Request schemas
# -----------------------------
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class UserVerifyEmail(BaseModel):
    token: str

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class UserResetPassword(UserVerifyEmail):
    password: str = Field(..., min_length=8)


class UserDeleteAccount(BaseModel):
    password: str = Field(..., min_length=8)

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class UserChangePassword(BaseModel):
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


# -----------------------------
# Email-related requests
# -----------------------------
class UserResendVerification(UserEmailRequest):
    pass


class UserForgotPassword(UserEmailRequest):
    pass


# -----------------------------
# Response schemas
# -----------------------------
class UserResponse(UserBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        str_strip_whitespace=True,
        from_attributes=True,
        extra="forbid",
    )
