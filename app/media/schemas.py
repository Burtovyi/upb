# app/media/schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MediaBase(BaseModel):
    media_type: str
    url: str
    description: Optional[str] = None
    article_id: int

class MediaCreate(MediaBase):
    """
    Схема для створення медіа-об’єкта.
    Вхідні дані містять інформацію про тип медіа, шлях (url) до файлу,
    опис (опціонально) та зв’язок із статтею (article_id).
    """
    pass

class MediaOut(MediaBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
