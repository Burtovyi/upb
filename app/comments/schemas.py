from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from datetime import datetime

class CommentBase(BaseModel):
    """
    Базова модель для коментаря.
    Містить вміст, ID батьківського коментаря та ID статті.
    """
    content: str = Field(..., min_length=1, max_length=1000)
    parent_id: Optional[int] = Field(None, ge=1)
    article_id: int = Field(..., ge=1)

    @field_validator("content")
    def validate_content(self, v):
        if not v.strip():
            raise ValueError("Коментар не може бути порожнім")
        return v.strip()

class CommentCreate(CommentBase):
    """
    Модель для створення коментаря.
    Успадковує усі поля від CommentBase.
    """
    pass

class CommentUpdate(BaseModel):
    """
    Модель для оновлення коментаря.
    Усі поля необов’язкові.
    """
    content: Optional[str] = Field(None, min_length=1, max_length=1000)
    parent_id: Optional[int] = Field(None, ge=1)

    @field_validator("content")
    def validate_content(self, v):
        if v is not None and not v.strip():
            raise ValueError("Коментар не може бути порожнім")
        return v.strip() if v else v

class CommentOut(CommentBase):
    """
    Модель для виведення коментаря.
    Містить ID, ID автора, час створення та успадковані поля від CommentBase.
    """
    id: int = Field(..., ge=1)
    author_id: int = Field(..., ge=1)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)