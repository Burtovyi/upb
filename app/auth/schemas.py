from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import Optional, Literal
from datetime import datetime
from enum import Enum
import re

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    EDITOR = "editor"

class UserBase(BaseModel):
    """
    Базова модель користувача.
    Містить email, ім’я та біографію.
    """
    email: EmailStr
    name: str = Field(..., strip_whitespace=True, min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=1000)

class UserCreate(UserBase):
    """
    Модель для створення користувача.
    Містить пароль із валідацією.
    """
    password: str = Field(..., min_length=8)

    @field_validator("password")
    def validate_password(self, v: str) -> str:
        if not re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", v):
            raise ValueError("Пароль повинен містити принаймні одну велику літеру, цифру та спеціальний символ")
        return v

class UserOut(UserBase):
    """
    Модель для виведення користувача.
    Містить додаткові поля з бази даних.
    """
    id: int = Field(..., ge=1)
    is_active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime
    created_by: int = Field(..., ge=1)
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    """
    Модель для токенів аутентифікації.
    Містить access-токен, refresh-токен і тип токена.
    """
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"]