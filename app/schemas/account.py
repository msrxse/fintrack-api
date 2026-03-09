from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from app.models.account import AccountType


class AccountCreate(BaseModel):
    name: str
    type: AccountType
    currency: str = "EUR"
    balance: Decimal = Decimal("0")


class AccountUpdate(BaseModel):
    name: str | None = None
    currency: str | None = None
    is_active: bool | None = None


class AccountOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    type: AccountType
    currency: str
    balance: Decimal
    is_active: bool
    created_at: datetime
