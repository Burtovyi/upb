from typing import List
from sqlalchemy import Integer, String, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

article_tags = Table(
    "article_tags",
    Base.metadata,
    mapped_column("article_id", Integer, ForeignKey("articles.article_id", ondelete="CASCADE"), primary_key=True),
    mapped_column("tag_id", Integer, ForeignKey("tags.tag_id", ondelete="CASCADE"), primary_key=True)
)

class Tag(Base):
    __tablename__ = "tags"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, name="tag_id")
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    articles: Mapped[List["Article"]] = relationship("Article", secondary=article_tags, back_populates="tags")
