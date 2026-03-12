
# GET    /transactions        → list (with filters)
# GET    /transactions/{id}   → single
# POST   /transactions        → create
# PUT    /transactions/{id}   → update
# DELETE /transactions/{id}   → soft delete

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionOut, TransactionUpdate

router = APIRouter(prefix="/transactions", tags=["Transactions"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[TransactionOut])
def get_transactions(db: Session = Depends(get_db)):
  return db.query(Transaction).filter(Transaction.is_deleted == False).all()

@router.get("/{id}", response_model=TransactionOut)
def get_transaction(id: int, db: Session = Depends(get_db)):
  transaction = db.query(Transaction).filter(
    Transaction.id == id,
    Transaction.is_deleted == False).first()
  if transaction is None:
    raise HTTPException(status_code=404, detail="Transaction not found")
  return transaction

@router.post("/", response_model=TransactionOut)
def post_transaction(body:TransactionCreate, db:Session = Depends(get_db)):
  db_transaction = Transaction(**body.model_dump())
  db.add(db_transaction)
  db.commit()
  # reloads the object from the DB so id and created_at are populated
  db.refresh(db_transaction)
  return db_transaction

@router.put("/{id}", response_model=TransactionOut)
def put_transaction(id: int, body: TransactionUpdate, db: Session = Depends(get_db)):
  db_transaction = db.query(Transaction).filter(
    Transaction.id == id,
    Transaction.is_deleted == False).first()
  if db_transaction is None:
    raise HTTPException(status_code=404, detail="Transaction not found")

  # exclude_unset=True — only includes fields the client actually sent,
  # not the ones that defaulted to None. So if
  # they only send {"description": "coffee"}, only description gets updated.
  for field, value in body.model_dump(exclude_unset=True).items():
    setattr(db_transaction, field, value)
  db.commit()
  db.refresh(db_transaction)
  return db_transaction

@router.delete("/{id}", response_model=TransactionOut)
def delete_transaction(id: int, db: Session = Depends(get_db)):
  db_transaction = db.query(Transaction).filter(
    Transaction.id == id,
    Transaction.is_deleted == False
  ).first()
  if db_transaction is None:
    raise HTTPException(status_code=404, detail="Transaction not found")
  db_transaction.is_deleted = True
  db.commit()
  return db_transaction