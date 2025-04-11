# app/media/models.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True, index=True)
    media_type = Column(String, nullable=False)  # Наприклад: "image" або "video"
    url = Column(String, nullable=False)         # Шлях або URL до файлу
    description = Column(Text, nullable=True)      # Опціональний опис або підпис
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Зовнішній ключ до статті
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    
    # Зв’язок зі статтею
    article = relationship("Article", back_populates="media_items")
