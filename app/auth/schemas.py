from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: constr(strip_whitespace=True, min_length=1, max_length=100)

class UserCreate(UserBase):
    password: constr(min_length=8)

class UserOut(UserBase):
    id: int
    is_active: bool
    role: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
