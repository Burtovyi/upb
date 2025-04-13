from typing import Optional
from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class Media(Base):
    __tablename__ = "media"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    media_type: Mapped[str] = mapped_column(String, nullable=False)  # Наприклад: "image" або "video"
    url: Mapped[str] = mapped_column(String, nullable=False)         # Шлях або URL до файлу
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey("articles.id"), nullable=False)
    
    article: Mapped["Article"] = relationship("Article", back_populates="media_items")
