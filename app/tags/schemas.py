# app/tags/schemas.py

from pydantic import BaseModel, Field
from typing import Optional

class TagBase(BaseModel):
    name: str = Field(..., max_length=100)

class TagCreate(TagBase):
    pass

class TagOut(TagBase):
    id: int

    class Config:
        from_attributes = True
