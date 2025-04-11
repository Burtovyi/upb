# app/authors/schemas.py

from pydantic import BaseModel
from typing import Optional

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    """
    Схема для створення нового автора.
    Містить обов’язкове поле name та опціональне поле bio.
    """
    pass

class AuthorUpdate(BaseModel):
    """
    Схема для оновлення даних автора.
    Усі поля опціональні, що дозволяє оновлювати лише необхідні дані.
    """
    name: Optional[str] = None
    bio: Optional[str] = None

class AuthorOut(AuthorBase):
    """
    Схема для відображення автора клієнту.
    Включає ідентифікатор автора.
    """
    id: int

    class Config:
        orm_mode = True
