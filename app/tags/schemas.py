from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class TagCreate(TagBase):
    pass  # Залишено, якщо потрібен для структури

class TagUpdate(BaseModel):
    name: Optional[str] = None

class TagOut(TagBase):
    id: int = Field(..., ge=1)

    model_config = ConfigDict(from_attributes=True)