from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from datetime import datetime

class AuthorBase(BaseModel):
    """
    Базова модель для автора.
    Містить ім'я та необов’язкову біографію.
    """
    name: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=1000)

    @field_validator("name")
    def validate_name(self, v: str) -> str:
        if not v.strip():
            raise ValueError("Ім'я автора не може бути порожнім")
        return v.strip()

class AuthorCreate(AuthorBase):
    """
    Модель для створення автора.
    Успадковує усі поля від AuthorBase.
    """
    pass

class AuthorUpdate(BaseModel):
    """
    Модель для оновлення автора.
    Усі поля необов’язкові.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=1000)

    @field_validator("name")
    def validate_name(self, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Ім'я автора не може бути порожнім")
        return v.strip() if v else v

class AuthorOut(AuthorBase):
    """
    Модель для виведення автора.
    Містить ID, час створення та успадковані поля від AuthorBase.
    """
    id: int = Field(..., ge=1)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)