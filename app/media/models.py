from typing import Optional
from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func  # Коректний імпорт
from app.db.database import Base

class Media(Base):
    __tablename__ = "media"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    media_type: Mapped[str] = mapped_column(String(20), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now)  # Без виклику
    
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey("articles.id"), nullable=False, index=True)
    
    article: Mapped["Article"] = relationship("Article", back_populates="media_items")