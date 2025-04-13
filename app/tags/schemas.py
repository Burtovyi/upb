from pydantic import BaseModel, Field

class TagBase(BaseModel):
    name: str = Field(..., max_length=100)

class TagCreate(TagBase):
    pass

class TagOut(TagBase):
    id: int

    class Config:
        from_attributes = True
