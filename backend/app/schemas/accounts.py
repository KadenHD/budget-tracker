from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, Field


# -----------------------------
# Base schemas
# -----------------------------
class AccountBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=20)

    model_config = ConfigDict(str_strip_whitespace=True)


# -----------------------------
# Request schemas
# -----------------------------
class AccountCreate(AccountBase):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class AccountUpdate(AccountBase):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


# -----------------------------
# Response schemas
# -----------------------------
class AccountResponse(AccountBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        str_strip_whitespace=True,
        from_attributes=True,
        extra="forbid",
    )
