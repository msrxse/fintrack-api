
# GET    /categories        → list (with filters)
# GET    /categories/{id}   → single
# POST   /categories        → create
# PUT    /categories/{id}   → update
# DELETE /categories/{id}   → soft delete

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
  return db.query(Category).all()

@router.get("/{id}", response_model=CategoryOut)
def get_category(id: int, db: Session = Depends(get_db)):
  category = db.query(Category).filter(
    Category.id == id).first()
  if category is None:
    raise HTTPException(status_code=404, detail="Category not found")
  return category

@router.post("/", response_model=CategoryOut)
def post_category(body:CategoryCreate, db:Session = Depends(get_db)):
  db_category = Category(**body.model_dump())
  db.add(db_category)
  db.commit()
  # reloads the object from the DB so id and created_at are populated
  db.refresh(db_category)
  return db_category

@router.put("/{id}", response_model=CategoryOut)
def put_category(id: int, body: CategoryUpdate, db: Session = Depends(get_db)):
  db_category = db.query(Category).filter(
    Category.id == id).first()
  if db_category is None:
    raise HTTPException(status_code=404, detail="Category not found")

  # exclude_unset=True — only includes fields the client actually sent,
  # not the ones that defaulted to None. So if
  # they only send {"description": "coffee"}, only description gets updated.
  for field, value in body.model_dump(exclude_unset=True).items():
    setattr(db_category, field, value)
  db.commit()
  db.refresh(db_category)
  return db_category

@router.delete("/{id}", response_model=CategoryOut)
def delete_category(id: int, db: Session = Depends(get_db)):
  db_category = db.query(Category).filter(
    Category.id == id,
  ).first()
  if db_category is None:
    raise HTTPException(status_code=404, detail="Category not found")
  if db_category.is_system:
    raise HTTPException(status_code=400, detail="Connot delete system categories")
  db.delete(db_category)
  db.commit()
  return db_category