from sqlalchemy import UUID, Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.services.database import Base


class Account(Base):
    __tablename__ = "accounts"

    name = Column(String(20), nullable=False)

    # NOTE: Composite unique constraint, name must be unique per user
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_account_name"),
    )

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="account", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Account(name={self.name})>"
