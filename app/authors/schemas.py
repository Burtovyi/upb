# app/authors/schemas.py

from pydantic import BaseModel, Field
from typing import Optional

class AuthorBase(BaseModel):
    name: str = Field(..., max_length=100)
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = None

class AuthorOut(AuthorBase):
    id: int

    class Config:
        from_attributes = True
