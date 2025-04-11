# app/authors/models.py

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    bio = Column(Text, nullable=True)
    # Опціонально: додаткові поля для профілю (зображення, контакти тощо)
    
    # Зв’язок зі статтями
    articles = relationship("Article", back_populates="author", cascade="all, delete")
