# app/articles/models.py

from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Базовий клас для моделей (можна розмістити у app/db/database.py)
class Base(DeclarativeBase):
    pass

class Article(Base):
    __tablename__ = "articles"
    
    # Використовуємо mapped_column для кожного стовпця.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, name="article_id")
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, name="view_count")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("now()"), nullable=False, name="created_at")
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("now()"), onupdate=text("now()"), nullable=False, name="updated_at")
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, name="published_at")
    
    # Зовнішні ключі:
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("authors.author_id"), nullable=False, name="author_id")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.category_id"), nullable=False, name="category_id")
    content_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("content_types.type_id"), nullable=False, name="content_type_id")
    
    # Зв’язки:
    author: Mapped["Author"] = relationship("Author", back_populates="articles")
    category: Mapped["Category"] = relationship("Category", back_populates="articles")
    content_type: Mapped["ContentType"] = relationship("ContentType", back_populates="articles")
    tags: Mapped[list["Tag"]] = relationship("Tag", secondary="article_tags", back_populates="articles")
    article_history: Mapped[list["ArticleHistory"]] = relationship("ArticleHistory", back_populates="article", cascade="all, delete-orphan")


class ArticleHistory(Base):
    __tablename__ = "article_history"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, name="history_id")
    article_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("articles.article_id", ondelete="CASCADE"), 
        nullable=False, 
        name="article_id"
    )
    version_num: Mapped[int] = mapped_column(Integer, nullable=False, name="version_num")
    title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    edited_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("now()"), nullable=False, name="edited_at")
    action: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    article: Mapped["Article"] = relationship("Article", back_populates="article_history")
