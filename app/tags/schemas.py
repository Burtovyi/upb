# app/tags/schemas.py

from pydantic import BaseModel
from typing import Optional

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    """
    Схема для створення нового тегу.
    Використовує обов’язкове поле name, яке задає назву тегу.
    """
    pass

class TagOut(TagBase):
    """
    Схема для повернення даних тегу клієнту.
    Додається ідентифікатор тегу.
    """
    id: int

    class Config:
        orm_mode = True
