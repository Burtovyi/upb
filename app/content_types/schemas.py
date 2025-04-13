from pydantic import BaseModel, Field
from typing import Optional

class ContentTypeBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None

class ContentTypeCreate(ContentTypeBase):
    pass

class ContentTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None

class ContentTypeOut(ContentTypeBase):
    id: int

    class Config:
        from_attributes = True
