import enum
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class AccountType(enum.Enum):
    checking = "checking"
    savings = "savings"
    credit = "credit"
    investment = "investment"


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(Enum(AccountType), nullable=False)
    currency = Column(String(3), default="EUR")
    balance = Column(Numeric(12, 2), default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")
