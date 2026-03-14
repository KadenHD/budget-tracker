from datetime import date
from sqlalchemy import Column, String, Float, Date, ForeignKey, Enum, UUID
from sqlalchemy.orm import relationship
from app.database import Base
from app.models import TimestampMixin
from app.schemas.transaction_type import TransactionType
import uuid

class Transaction(TimestampMixin, Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column(Float, nullable=False)
    description = Column(String(100))
    date = Column(Date, nullable=False, default=date.today)
    type = Column(Enum(TransactionType, name="transactiontype"), nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))

    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(amount={self.amount}, type={self.type}, date={self.date})>"
