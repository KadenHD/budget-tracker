from pydantic import UUID4, BaseModel, ConfigDict, Field
from app.schemas import Mixin

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
class AccountResponse(AccountBase, Mixin):
    user_id: UUID4

    model_config = ConfigDict(
        str_strip_whitespace=True,
        from_attributes=True,
        extra="forbid",
    )
