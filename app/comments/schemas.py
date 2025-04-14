from pydantic import BaseModel
from typing import Optional

class CommentBase(BaseModel):
    content: str
    parent_id: Optional[int] = None
    article_id: int

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: Optional[str] = None
    parent_id: Optional[int] = None

class CommentOut(CommentBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True
