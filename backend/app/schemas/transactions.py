from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict, Field

from app.schemas import Mixin


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


# -----------------------------
# Base schemas
# -----------------------------
class TransactionBase(BaseModel):
    amount: Decimal = Field(..., gt=0)
    description: str | None = Field(None, max_length=100)
    date: date
    type: TransactionType
    category_id: UUID4 | None

    model_config = ConfigDict(str_strip_whitespace=True)


# -----------------------------
# Request schemas
# -----------------------------
class TransactionCreate(TransactionBase):
    model_config = ConfigDict(extra="forbid")


class TransactionUpdate(BaseModel):
    amount: Decimal | None = Field(None, gt=0)
    description: str | None = Field(None, max_length=100)
    date: Optional[date] = None # pyright: ignore[reportInvalidTypeForm] # noqa: UP045
    type: TransactionType | None = None
    category_id: UUID4 | None = None

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )


# -----------------------------
# Response schemas
# -----------------------------
class TransactionResponse(TransactionBase, Mixin):
    account_id: UUID4

    model_config = ConfigDict(
        str_strip_whitespace=True,
        from_attributes=True,
        extra="forbid",
    )
