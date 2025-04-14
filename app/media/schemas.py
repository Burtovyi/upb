from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from typing import Optional
from datetime import datetime

class MediaBase(BaseModel):
    article_id: int = Field(..., ge=1, description="ID статті")
    media_type: str = Field(..., pattern="^(image|video|audio)$", description="Тип медіа")
    url: HttpUrl
    description: Optional[str] = None

class MediaCreate(MediaBase):
    pass  # Залишено, якщо потрібен для структури

class MediaOut(MediaBase):
    id: int = Field(..., ge=1)
    created_by: int = Field(..., ge=1)
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)