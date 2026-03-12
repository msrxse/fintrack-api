import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.user import User

security = HTTPBearer()


def get_current_user(credentials = Depends(security), db: Session = Depends(get_db)):
  token = credentials.credentials
  try:
    payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
  except jwt.PyJWTError:
    raise HTTPException(status_code=401, detail="Verify and or checking your signature failed.")

  existing_user = db.query(User).filter(User.id == payload["user_id"]).first()

  if existing_user is None:
    raise HTTPException(status_code=401, detail="Unknown error trying to find current user.")

  return existing_user
