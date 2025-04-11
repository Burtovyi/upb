# app/content_types/schemas.py

from pydantic import BaseModel
from typing import Optional

class ContentTypeBase(BaseModel):
    name: str

class ContentTypeCreate(ContentTypeBase):
    """
    Схема для створення нового типу контенту.
    Використовує основне поле name, яке є обов’язковим.
    """
    pass

class ContentTypeUpdate(BaseModel):
    """
    Схема для оновлення існуючого типу контенту.
    Поле name є опціональним, тому можна оновлювати лише передані дані.
    """
    name: Optional[str] = None

class ContentTypeOut(ContentTypeBase):
    """
    Схема для повернення даних типу контенту клієнту.
    Включає ідентифікатор.
    """
    id: int

    class Config:
        orm_mode = True
