
# GET    /budgets        → list (with filters)
# GET    /budgets/{id}   → single
# POST   /budgets        → create
# PUT    /budgets/{id}   → update
# DELETE /budgets/{id}   → soft delete

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.budget import Budget
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetOut, BudgetUpdate

router = APIRouter(prefix="/budgets", tags=["Budgets"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[BudgetOut])
def get_budgets(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  return db.query(Budget).filter(Budget.user_id == user.id).all()

@router.get("/{id}", response_model=BudgetOut)
def get_budget(id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  budget = db.query(Budget).filter(
    Budget.id == id,
    Budget.user_id == user.id).first()
  if budget is None:
    raise HTTPException(status_code=404, detail="Budget not found")
  return budget

@router.post("/", response_model=BudgetOut)
def post_budget(body:BudgetCreate, user: User = Depends(get_current_user), db:Session = Depends(get_db)):
  db_budget = Budget(**body.model_dump(), user_id=user.id)
  try:
    db.add(db_budget)
    db.commit()
  except IntegrityError:
    raise HTTPException(status_code=409, detail="A budget just like this already exists.")
  # reloads the object from the DB so id and created_at are populated
  db.refresh(db_budget)
  return db_budget

@router.put("/{id}", response_model=BudgetOut)
def put_budget(id: int, body: BudgetUpdate, db: Session = Depends(get_db)):
  db_budget = db.query(Budget).filter(
    Budget.id == id).first()
  if db_budget is None:
    raise HTTPException(status_code=404, detail="Budget not found")

  # exclude_unset=True — only includes fields the client actually sent,
  # not the ones that defaulted to None. So if
  # they only send {"description": "coffee"}, only description gets updated.
  for field, value in body.model_dump(exclude_unset=True).items():
    setattr(db_budget, field, value)
  db.commit()
  db.refresh(db_budget)
  return db_budget

@router.delete("/{id}", response_model=BudgetOut)
def delete_budget(id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  db_budget = db.query(Budget).filter(
    Budget.id == id,
    Budget.user_id == user.id
  ).first()
  if db_budget is None:
    raise HTTPException(status_code=404, detail="Budget not found")
  db_budget.category  # eagerly load before delete
  db.delete(db_budget)
  db.commit()
  return db_budget