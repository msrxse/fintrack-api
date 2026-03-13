from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
def auth_user_register(
    body:UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
  ):
  existing_user = db.query(User.email).filter(User.email == body.email).first()
  if existing_user:
    raise HTTPException(status_code=409, detail="This user already has an account. Login instead.")
  hashed = bcrypt.hashpw(body.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
  db_user = User(
    email=body.email,
    full_name=body.full_name,
    hashed_password=hashed
  )
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  background_tasks.add_task(send_welcome_email, str(db_user.email))

  return db_user

@router.post("/login")
def auth_user_login(body:UserCreate, db:Session = Depends(get_db)):
  existing_user = db.query(User).filter(User.email == body.email).first()
  if existing_user is None:
    raise HTTPException(status_code=401, detail="There was an error processing your request")

  if bcrypt.checkpw(body.password.encode("utf-8"), existing_user.hashed_password.encode("utf-8")) is False:
    raise HTTPException(status_code=401, detail="The password doesnt match.")

  encoded = jwt.encode({"user_id": existing_user.id, "exp": datetime.now(timezone.utc) + timedelta(hours=1)}, settings.secret_key, algorithm="HS256")

  return {"access_token": encoded, "token_type": "bearer"}

@router.get("/users/me", response_model=UserOut)
def get_auth_user_me(user:User =  Depends(get_current_user)):
  return user

def send_welcome_email(email: str):
  print(f"Sending welcome email to {email}")