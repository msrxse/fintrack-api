from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from app.models.budget import BudgetPeriod
from app.schemas.category import CategoryOut


class BudgetCreate(BaseModel):
    category_id: int
    limit_amount: Decimal
    period: BudgetPeriod


class BudgetUpdate(BaseModel):
    limit_amount: Decimal | None = None


class BudgetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    limit_amount: Decimal
    period: BudgetPeriod
    created_at: datetime
    category: CategoryOut
