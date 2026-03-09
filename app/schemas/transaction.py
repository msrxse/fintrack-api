from datetime import date as Date
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.transaction import TransactionType
from app.schemas.category import CategoryOut


class TransactionCreate(BaseModel):
    account_id: int
    category_id: int | None = None
    amount: Decimal
    type: TransactionType
    description: str | None = None
    merchant: str | None = None
    date: Date


class TransactionUpdate(BaseModel):
    category_id: int | None = None
    description: str | None = None
    merchant: str | None = None
    date: Date | None = None


class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    account_id: int
    amount: Decimal
    type: TransactionType
    description: str | None = None
    merchant: str | None = None
    date: Date
    created_at: datetime
    category: CategoryOut | None = None
