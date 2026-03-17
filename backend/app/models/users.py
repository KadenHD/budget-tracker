from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.services.database import Base

class User(Base):
    __tablename__ = "users"

    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
