from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
import datetime
from app.db.database import Base

class Article(Base):
    """
    Модель статті.
    Містить дані про заголовок, вміст, автора, категорію, тип контенту, теги, коментарі та історію редагувань.
    """
    __tablename__ = "articles"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, CheckConstraint("view_count >= 0"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    published_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("authors.id", ondelete="RESTRICT"), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False, index=True)
    content_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("content_types.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    # Зв’язки
    author: Mapped["Author"] = relationship("Author", back_populates="articles")
    category: Mapped["Category"] = relationship("Category", back_populates="articles")
    content_type: Mapped["ContentType"] = relationship("ContentType", back_populates="articles")
    tags: Mapped[List["Tag"]] = relationship("Tag", secondary="article_tags", back_populates="articles")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="article", cascade="all, delete")
    history: Mapped[List["ArticleHistory"]] = relationship("ArticleHistory", back_populates="article", cascade="all, delete")

class ArticleHistory(Base):
    """
    Модель історії редагувань статті.
    Зберігає версії заголовка, вмісту та дії над статтею.
    """
    __tablename__ = "article_history"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True)
    version_num: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    edited_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    action: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Зв’язок
    article: Mapped["Article"] = relationship("Article", back_populates="history")