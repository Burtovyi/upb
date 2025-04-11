# app/articles/models.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, autoincrement=True, name="article_id")
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    view_count = Column(Integer, default=0, nullable=False, name="view_count")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, name="created_at")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, name="updated_at")
    published_at = Column(DateTime, nullable=True, name="published_at")
    
    author_id = Column(Integer, ForeignKey("authors.author_id"), nullable=False, name="author_id")
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False, name="category_id")
    content_type_id = Column(Integer, ForeignKey("content_types.type_id"), nullable=False, name="content_type_id")
    
    # Відношення до інших таблиць
    author = relationship("Author", back_populates="articles")
    category = relationship("Category", back_populates="articles")
    content_type = relationship("ContentType", back_populates="articles")
    tags = relationship("Tag", secondary="article_tags", back_populates="articles")
    article_history = relationship("ArticleHistory", back_populates="article", cascade="all, delete-orphan")

# Також додаємо модель історії статей
class ArticleHistory(Base):
    __tablename__ = "article_history"
    id = Column(Integer, primary_key=True, autoincrement=True, name="history_id")
    article_id = Column(Integer, ForeignKey("articles.article_id", ondelete="CASCADE"), nullable=False, name="article_id")
    version_num = Column(Integer, nullable=False, name="version_num")
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=True)
    edited_at = Column(DateTime, server_default=func.now(), nullable=False, name="edited_at")
    action = Column(String(50), nullable=True)
    
    article = relationship("Article", back_populates="article_history")
