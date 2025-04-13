# app/metrics/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class MetricsBase(BaseModel):
    view_count: int = Field(0)
    like_count: int = Field(0)
    comment_count: int = Field(0)
    share_count: int = Field(0)
    
class MetricsCreate(MetricsBase):
    article_id: int

class MetricsUpdate(BaseModel):
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    share_count: Optional[int] = None

class MetricsOut(MetricsBase):
    article_id: int

    class Config:
        from_attributes = True
