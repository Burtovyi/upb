from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MediaBase(BaseModel):
    article_id: int
    media_type: str
    url: str
    description: Optional[str] = None

class MediaCreate(MediaBase):
    pass

class MediaOut(MediaBase):
    id: int
    created_by: int
    uploaded_at: datetime

    class Config:
        orm_mode = True
