# app/content_types/models.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class ContentType(Base):
    __tablename__ = "content_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    # Зв’язок зі статтями
    articles = relationship("Article", back_populates="content_type")
