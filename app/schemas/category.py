from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.category import CategoryType


class CategoryCreate(BaseModel):
    name: str
    type: CategoryType


class CategoryUpdate(BaseModel):
    name: str | None = None


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: CategoryType
    is_system: bool
    user_id: int | None = None
    created_at: datetime
