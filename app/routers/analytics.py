from fastapi import APIRouter, Depends
from sqlalchemy import case, func, text
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.budget import Budget
from app.models.category import Category
from app.models.transaction import Transaction, TransactionType
from app.schemas.analytics import (
  AnalyticsBudgetStatus,
  AnalyticsCashFlow,
  AnalyticsMonthlySummary,
  AnalyticsSpendingByCategory,
  AnalyticsTopMerchant,
  AnalyticsTrends,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/spending-by-category", response_model=list[AnalyticsSpendingByCategory])
def get_spending_by_category(type:TransactionType, db: Session = Depends(get_db)):
  results = db.query(
    Category.name,
    func.sum(Transaction.amount).label("total")
    ).join(Transaction, Transaction.category_id == Category.id
      ).filter(Transaction.type == type
        ).group_by(Category.name
          ).all()

  return [{
    "category_name": row.name,
    "total": row.total,
  } for row in results]

@router.get("/monthly-summary", response_model=list[AnalyticsMonthlySummary])
def get_monthly_summary(db: Session = Depends(get_db)):
  results = db.query(
    func.date_trunc('month', Transaction.date).label("month"),
    func.sum(case((
      Transaction.type == TransactionType.income,
      Transaction.amount), else_=0
      )).label("income"),
    func.sum(case((
      Transaction.type == TransactionType.expense,
      Transaction.amount), else_=0
      )).label("expenses")
  ).group_by(
    func.date_trunc('month', Transaction.date)
  ).all()

  return [{
    "month": row.month,
    "income":row.income,
    "expenses":row.expenses,
  } for row in results]

@router.get("/top-merchants", response_model=list[AnalyticsTopMerchant])
def get_top_merchants(db:Session = Depends(get_db)):
  results = db.query(
    Transaction.merchant,
    func.sum(Transaction.amount).label("total"),
    func.count(Transaction.id).label("transaction_count")
  ).filter(
    Transaction.merchant != None
  ).group_by(
    Transaction.merchant
  ).order_by(
    func.sum(Transaction.amount).desc()
  ).limit(10).all()

  return [{
    "merchant": row.merchant,
    "total": row.total,
    "transaction_count": row.transaction_count
  } for row in results]

@router.get("/budget-status", response_model=list[AnalyticsBudgetStatus])
def get_budget_status(db:Session = Depends(get_db)):
  results = db.query(
    Budget.limit_amount,
    Category.name.label("category_name"),
    func.sum(Transaction.amount).label("actual_spent"),
    (Budget.limit_amount - func.sum(Transaction.amount)).label("remaining")
  ).join(Category, Category.id == Budget.category_id
         ).join(Transaction, Transaction.category_id == Category.id
                ).group_by(Category.name, Budget.limit_amount
                           ).all()
  return [{
    "category_name": row.category_name,
    "limit_amount": row.limit_amount,
    "actual_spent": row.actual_spent,
    "remaining": row.remaining
  } for row in results]


@router.get("/cash-flow", response_model=list[AnalyticsCashFlow])
def get_cash_flow(db:Session = Depends(get_db)):
  results = db.execute(text("""
    SELECT
        date,
        SUM(amount) as net,
        SUM(SUM(amount)) OVER (ORDER BY date) as running_balance
    FROM transactions
    WHERE is_deleted = false
    GROUP BY date
    ORDER BY date
  """)).all()

  return [{
    "date": row.date,
    "net": row.net,
    "running_balance": row.running_balance,
  } for row in results]


@router.get("/trends", response_model=list[AnalyticsTrends])
def get_trends(db:Session = Depends(get_db)):
  results = db.execute(text("""
    SELECT
    category_id,
    date_trunc('month', date) as month,
    SUM(amount) as total,
    LAG(SUM(amount)) OVER (PARTITION BY category_id ORDER BY date_trunc('month', date)) as prev_month
    FROM transactions
    WHERE type = 'expense' AND is_deleted = false
    GROUP BY category_id, date_trunc('month', date)
    ORDER BY category_id, month
  """)).all()

  return [{
    "category_id": row.category_id,
    "month": row.month,
    "total": row.total,
    "prev_month": row.prev_month,
    "change_pct": round((row.total - row.prev_month) / row.prev_month * 100, 2) if row.prev_month else None,
  } for row in results]
