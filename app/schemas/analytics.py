from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class AnalyticsSpendingByCategory(BaseModel):
  category_name: str
  total: Decimal

class AnalyticsMonthlySummary(BaseModel):
  month: datetime
  income: Decimal
  expenses: Decimal

class AnalyticsTopMerchant(BaseModel):
  merchant: str
  total: Decimal
  transaction_count: int

class AnalyticsBudgetStatus(BaseModel):
  category_name: str
  limit_amount: Decimal
  actual_spent: Decimal
  remaining: Decimal

class AnalyticsCashFlow(BaseModel):
  date: date
  net: Decimal
  running_balance: Decimal

class AnalyticsTrends(BaseModel):
  category_id: int
  month: datetime
  total: Decimal
  prev_month: Decimal | None
  change_pct: Decimal | None