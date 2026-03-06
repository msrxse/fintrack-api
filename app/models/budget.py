import enum
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class BudgetPeriod(enum.Enum):
    weekly = "weekly"
    monthly = "monthly"


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    limit_amount = Column(Numeric(12, 2), nullable=False)
    period = Column(Enum(BudgetPeriod), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "category_id", "period", name="uq_budget_user_category_period"),
    )

    user = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")
