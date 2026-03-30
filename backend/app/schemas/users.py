from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas import Mixin


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


class UserPasswordRequest(BaseModel):
    password: str = Field(..., min_length=8)

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

# -----------------------------
# Request schemas
# -----------------------------
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class UserResetPassword(UserPasswordRequest):
    pass


class UserDeleteAccount(UserPasswordRequest):
    pass


class UserChangePassword(BaseModel):
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class UserResendVerification(UserEmailRequest):
    pass


class UserForgotPassword(UserEmailRequest):
    pass


# -----------------------------
# Response schemas
# -----------------------------
class UserResponse(UserBase, Mixin):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        from_attributes=True,
        extra="forbid",
    )
