# app/authors/models.py

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, autoincrement=True, name="author_id")
    name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
    
    # Один автор може мати багато статей
    articles = relationship("Article", back_populates="author", cascade="all, delete-orphan")
