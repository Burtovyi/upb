# app/content_types/models.py

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class ContentType(Base):
    __tablename__ = "content_types"
    id = Column(Integer, primary_key=True, autoincrement=True, name="type_id")
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Один тип контенту може бути прив’язаний до багатьох статей
    articles = relationship("Article", back_populates="content_type", cascade="all, delete-orphan")
