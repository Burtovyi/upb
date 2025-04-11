# app/categories/models.py

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True, name="category_id")
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Один розділ (категорія) може мати багато статей
    articles = relationship("Article", back_populates="category", cascade="all, delete-orphan")
