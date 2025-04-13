# app/roles/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class RoleBase(BaseModel):
    name: str = Field(..., max_length=50)
    can_read: bool = True
    can_write: bool = False
    can_moderate: bool = False
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    can_read: Optional[bool] = None
    can_write: Optional[bool] = None
    can_moderate: Optional[bool] = None
    description: Optional[str] = None

class RoleOut(RoleBase):
    id: int

    class Config:
        from_attributes = True
