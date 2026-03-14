from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
from app.database import Base
from app.models import TimestampMixin
import uuid

class Category(TimestampMixin, Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(20), nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)

    account = relationship("Account", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category(name={self.name})>"
