# app/social_integrations/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SocialIntegrationBase(BaseModel):
    platform: str = Field(..., max_length=20)
    account_ref: str = Field(..., max_length=100)
    is_active: bool = True

class SocialIntegrationCreate(SocialIntegrationBase):
    author_id: int

class SocialIntegrationUpdate(BaseModel):
    platform: Optional[str] = Field(None, max_length=20)
    account_ref: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

class SocialIntegrationOut(SocialIntegrationBase):
    id: int
    author_id: int
    added_at: datetime

    class Config:
        from_attributes = True
