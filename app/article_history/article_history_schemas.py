from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ArticleHistoryOut(BaseModel):
    id: int
    article_id: int
    version_num: int
    title: Optional[str]
    content: Optional[str]
    edited_at: datetime
    action: Optional[str]

    class Config:
        from_attributes = True
