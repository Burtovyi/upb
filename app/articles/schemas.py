# app/articles/schemas.py

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.articles.models import ArticleStatusEnum

class ArticleBase(BaseModel):
    title: str
    summary: Optional[str] = None
    content: str
    category_id: int
    content_type_id: int
    # Список ідентифікаторів тегів для прив'язки до статті
    tag_ids: Optional[List[int]] = []

class ArticleCreate(ArticleBase):
    """
    Схема для створення нової статті.
    Передбачається, що статус статті автоматично встановлюється як "draft".
    """
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    content_type_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    status: Optional[ArticleStatusEnum] = None

class ArticleOut(BaseModel):
    id: int
    title: str
    summary: Optional[str]
    content: str
    status: ArticleStatusEnum
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Додаткова схема (наприклад, для детального відображення) може включати вкладені дані,
# такі як інформація про автора, категорію, список тегів, медіа та коментарі.
class ArticleDetail(ArticleOut):
    # Наприклад, для тегів можна повернути список імен
    tag_names: Optional[List[str]] = []
