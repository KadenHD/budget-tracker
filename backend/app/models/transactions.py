from datetime import date
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum, UUID
from sqlalchemy.orm import relationship
from app.database import Base
from app.models import TimestampMixin
import enum
import uuid

class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class Transaction(TimestampMixin, Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column(Float, nullable=False)
    description = Column(String(100))
    date = Column(DateTime, default=date.today)
    type = Column(Enum(TransactionType), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(amount={self.amount}, type={self.type}, date={self.date})>"
