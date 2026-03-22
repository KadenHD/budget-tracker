from datetime import date

from sqlalchemy import UUID, Column, Date, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship

from app.schemas.transactions import TransactionType
from app.services.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(String(100), nullable=True)
    date = Column(Date, default=date.today, nullable=False)
    type = Column(Enum(TransactionType, name="transactiontype"), nullable=False)

    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)

    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(amount={self.amount}, type={self.type}, date={self.date})>"
