# app/comments/schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentBase(BaseModel):
    content: str
    parent_id: Optional[int] = None  # Якщо це відповідь на інший коментар

class CommentCreate(CommentBase):
    """
    Схема для створення нового коментаря.
    Використовує поля з CommentBase, тому вхідні дані містять обов’язкове поле content і
    опціонально parent_id.
    """
    pass

class CommentUpdate(BaseModel):
    """
    Схема для оновлення коментаря.
    Поля опціональні, тому можна оновлювати лише необхідні дані.
    """
    content: Optional[str] = None
    parent_id: Optional[int] = None

class CommentOut(CommentBase):
    """
    Схема для повернення даних коментаря клієнту.
    Включає ID коментаря, ID статті, ID користувача та дату створення.
    """
    id: int
    article_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
