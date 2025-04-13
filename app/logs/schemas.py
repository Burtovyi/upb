# app/logs/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LogBase(BaseModel):
    event_type: str = Field(..., max_length=50)
    user_id: Optional[int] = None
    object_type: Optional[str] = Field(None, max_length=50)
    object_id: Optional[int] = None
    details: Optional[str] = None

class LogCreate(LogBase):
    pass

class LogOut(LogBase):
    id: int
    event_time: datetime

    class Config:
        from_attributes = True
