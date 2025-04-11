# app/categories/schemas.py

from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    slug: str

class CategoryCreate(CategoryBase):
    """
    Схема для створення нової категорії.
    Поля: name та slug є обов'язковими.
    """
    pass

class CategoryUpdate(BaseModel):
    """
    Схема для оновлення даних категорії.
    Усі поля опціональні, що дозволяє оновлювати лише ті дані, які передані.
    """
    name: Optional[str] = None
    slug: Optional[str] = None

class CategoryOut(CategoryBase):
    """
    Схема для відображення категорії клієнту.
    Додається ідентифікатор категорії.
    """
    id: int

    class Config:
        orm_mode = True
