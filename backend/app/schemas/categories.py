from pydantic import UUID4, BaseModel, ConfigDict, Field

from app.schemas import Mixin


# -----------------------------
# Base schemas
# -----------------------------
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=20)

    model_config = ConfigDict(str_strip_whitespace=True)


# -----------------------------
# Request schemas
# -----------------------------
class CategoryCreate(CategoryBase):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class CategoryUpdate(CategoryBase):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


# -----------------------------
# Response schemas
# -----------------------------
class CategoryResponse(CategoryBase, Mixin):
    account_id: UUID4

    model_config = ConfigDict(
        str_strip_whitespace=True,
        from_attributes=True,
        extra="forbid",
    )
