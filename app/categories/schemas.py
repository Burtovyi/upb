from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    """
    Базова модель для категорії.
    Містить назву та необов’язковий опис.
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)

    @field_validator("name")
    def validate_name(self, v: str) -> str:
        if not v.strip():
            raise ValueError("Назва категорії не може бути порожньою")
        return v.strip()

class CategoryCreate(CategoryBase):
    """
    Модель для створення категорії.
    Успадковує усі поля від CategoryBase.
    """
    pass

class CategoryUpdate(BaseModel):
    """
    Модель для оновлення категорії.
    Усі поля необов’язкові.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)

    @field_validator("name")
    def validate_name(self, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Назва категорії не може бути порожньою")
        return v.strip() if v else v

class CategoryOut(CategoryBase):
    id: int = Field(..., ge=1)
    created_at: datetime
    created_by: int = Field(..., ge=1)
    model_config = ConfigDict(from_attributes=True)