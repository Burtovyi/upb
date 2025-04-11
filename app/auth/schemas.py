# app/auth/schemas.py

from pydantic import BaseModel, EmailStr, constr
from typing import Optional

# Базова схема для користувача (email та username)
class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None

# Схема для створення користувача (реєстрація)
class UserCreate(UserBase):
    # Використання constr дозволяє додати обмеження на довжину паролю (наприклад, мінімум 8 символів)
    password: constr(min_length=8)

# Схема для відображення даних користувача (без паролю)
class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

# Схема для токену аутентифікації
class Token(BaseModel):
    access_token: str
    token_type: str

# Схема даних, які витягуються з токену
class TokenData(BaseModel):
    email: Optional[str] = None
