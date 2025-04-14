from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
import datetime
from app.db.database import Base

class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    view_count: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("authors.author_id"), nullable=False, name="author_id")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.category_id"), nullable=False, name="category_id")
    content_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("content_types.type_id"), nullable=False, name="content_type_id")
    # Зв’язки:
    author: Mapped["Author"] = relationship("Author", back_populates="articles")
    category: Mapped["Category"] = relationship("Category", back_populates="articles")
    content_type: Mapped["ContentType"] = relationship("ContentType", back_populates="articles")
    tags: Mapped[List["Tag"]] = relationship("Tag", secondary="article_tags", back_populates="articles")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="article", cascade="all, delete")
