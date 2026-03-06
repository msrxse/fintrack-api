import enum
from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class TransactionType(enum.Enum):
    income = "income"
    expense = "expense"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    amount = Column(Numeric(12, 2), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    description = Column(String, nullable=True)
    merchant = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
