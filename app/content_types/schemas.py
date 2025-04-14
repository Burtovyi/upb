from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional

class ContentTypeBase(BaseModel):
    """
    Базова модель для типу контенту.
    Містить назву та необов’язковий опис.
    """
    name: str = Field(max_length=100)
    description: Optional[str] = None

    @field_validator("name")
    def validate_name(self, v):
        if not v.strip():
            raise ValueError("Назва не може бути порожньою")
        return v.strip()

class ContentTypeCreate(ContentTypeBase):
    """
    Модель для створення типу контенту.
    Успадковує усі поля від ContentTypeBase.
    """
    pass

class ContentTypeUpdate(BaseModel):
    """
    Модель для оновлення типу контенту.
    Усі поля необов’язкові.
    """
    name: Optional[str] = Field(max_length=100)
    description: Optional[str] = None

    @field_validator("name")
    def validate_name(self, v):
        if v is not None and not v.strip():
            raise ValueError("Назва не може бути порожньою")
        return v.strip() if v else v

class ContentTypeOut(ContentTypeBase):
    """
    Модель для виведення типу контенту.
    Містить ID та успадковані поля від ContentTypeBase.
    """
    id: int = Field(ge=1)

    model_config = ConfigDict(from_attributes=True)