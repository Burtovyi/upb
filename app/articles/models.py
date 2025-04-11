# app/articles/models.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum

class ArticleStatusEnum(enum.Enum):
    draft = "draft"
    moderation = "moderation"
    published = "published"

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    status = Column(Enum(ArticleStatusEnum), default=ArticleStatusEnum.draft, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)
    
    # Зовнішні ключі
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    content_type_id = Column(Integer, ForeignKey("content_types.id"), nullable=False)
    
    # Зв’язки (Використовуємо рядкові посилання для уникнення циклічних імпортів)
    author = relationship("Author", back_populates="articles")
    category = relationship("Category", back_populates="articles")
    content_type = relationship("ContentType", back_populates="articles")
    tags = relationship("Tag", secondary="article_tags", back_populates="articles")
    media_items = relationship("Media", back_populates="article", cascade="all, delete")
    comments = relationship("Comment", back_populates="article", cascade="all, delete")
