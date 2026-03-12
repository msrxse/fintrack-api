
# GET    /accounts        → list (with filters)
# GET    /accounts/{id}   → single
# POST   /accounts        → create
# PUT    /accounts/{id}   → update
# DELETE /accounts/{id}   → soft delete

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.account import Account
from app.models.user import User
from app.schemas.account import AccountCreate, AccountOut, AccountUpdate

router = APIRouter(prefix="/accounts", tags=["Accounts"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[AccountOut])
def get_accounts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  return db.query(Account).filter(Account.user_id == user.id).all()

@router.get("/{id}", response_model=AccountOut)
def get_account(id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  account = db.query(Account).filter(
    Account.id == id,
    Account.user_id == user.id).first()
  if account is None:
    raise HTTPException(status_code=404, detail="Account not found")
  return account

@router.post("/", response_model=AccountOut)
def post_account(body:AccountCreate, db:Session = Depends(get_db)):
  db_account = Account(**body.model_dump())
  db.add(db_account)
  db.commit()
  # reloads the object from the DB so id and created_at are populated
  db.refresh(db_account)
  return db_account

@router.put("/{id}", response_model=AccountOut)
def put_account(id: int, body: AccountUpdate, db: Session = Depends(get_db)):
  db_account = db.query(Account).filter(
    Account.id == id,
    Account.is_active == True).first()
  if db_account is None:
    raise HTTPException(status_code=404, detail="Account not found")

  # exclude_unset=True — only includes fields the client actually sent,
  # not the ones that defaulted to None. So if
  # they only send {"description": "coffee"}, only description gets updated.
  for field, value in body.model_dump(exclude_unset=True).items():
    setattr(db_account, field, value)
  db.commit()
  db.refresh(db_account)
  return db_account

@router.delete("/{id}", response_model=AccountOut)
def delete_account(id: int, db: Session = Depends(get_db)):
  db_account = db.query(Account).filter(
    Account.id == id,
    Account.is_active == True
  ).first()
  if db_account is None:
    raise HTTPException(status_code=404, detail="Account not found")
  db_account.is_active = False
  db.commit()
  return db_account