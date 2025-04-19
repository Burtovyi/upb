from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

class ArticleAction(str, Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"

class ArticleBase(BaseModel):
    """
    Базова модель статті.
    Містить основні поля: заголовок, опис, вміст, кількість переглядів.
    """
    title: str = Field(..., max_length=200, strip_whitespace=True)
    description: Optional[str] = Field(None, max_length=1000)
    content: str = Field(..., max_length=10000)
    view_count: int = Field(default=0, ge=0)

class ArticleCreate(ArticleBase):
    """
    Модель для створення статті.
    Містить додаткові поля: ID автора, категорії, теги.
    """
    author_id: int = Field(..., ge=1)
    category_id: int = Field(..., ge=1)
    tag_ids: Optional[List[int]] = None

    @field_validator("tag_ids")
    def validate_tag_ids(self, v: Optional[List[int]]) -> Optional[List[int]]:
        if v is not None and any(tag_id < 1 for tag_id in v):
            raise ValueError("Усі tag_ids повинні бути позитивними числами")
        return v

class ArticleUpdate(BaseModel):
    """
    Модель для оновлення статті.
    Усі поля необов’язкові.
    """
    title: Optional[str] = Field(None, max_length=200, strip_whitespace=True)
    description: Optional[str] = Field(None, max_length=1000)
    content: Optional[str] = Field(None, max_length=10000)
    view_count: Optional[int] = Field(None, ge=0)
    published_at: Optional[datetime] = None
    category_id: Optional[int] = Field(None, ge=1)
    tag_ids: Optional[List[int]] = None

    @field_validator("tag_ids")
    def validate_tag_ids(self, v: Optional[List[int]]) -> Optional[List[int]]:
        if v is not None and any(tag_id < 1 for tag_id in v):
            raise ValueError("Усі tag_ids повинні бути позитивними числами")
        return v

class ArticleOut(ArticleBase):
    """
    Модель для виведення статті.
    Містить додаткові поля з бази даних: ID, дати, автор, категорія, теги.
    """
    id: int
    author_id: int = Field(..., ge=1)
    category_id: int = Field(..., ge=1)
    tag_ids: Optional[List[int]] = None
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class ArticleHistoryOut(BaseModel):
    """
    Модель для історії редагувань статті.
    Містить дані про версію, дію та час редагування.
    """
    id: int
    article_id: int
    version_num: int
    title: Optional[str]
    content: Optional[str]
    edited_at: datetime
    action: Optional[ArticleAction] = None
    model_config = ConfigDict(from_attributes=True)