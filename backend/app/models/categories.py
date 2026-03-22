from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.services.database import Base


class Category(Base):
    __tablename__ = "categories"

    name = Column(String(20), nullable=False)

    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)

    account = relationship("Account", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category(name={self.name})>"
