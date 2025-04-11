# app/articles/schemas.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class ArticleBase(BaseModel):
    title: str = Field(..., max_length=200)
    content: str
    view_count: int = 0

class ArticleCreate(ArticleBase):
    author_id: int
    category_id: int
    content_type_id: int
    tag_ids: Optional[List[int]] = None  # Список ID тегів, якщо потрібно

class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = None
    view_count: Optional[int] = None
    published_at: Optional[datetime] = None
    category_id: Optional[int] = None
    content_type_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None

class ArticleOut(ArticleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Схема для історії статті
class ArticleHistoryOut(BaseModel):
    id: int
    article_id: int
    version_num: int
    title: Optional[str]
    content: Optional[str]
    edited_at: datetime
    action: Optional[str]

    class Config:
        from_attributes = True
