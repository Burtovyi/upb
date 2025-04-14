from typing import List, Optional
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.db.database import Base

class ContentType(Base):
    """
    Модель типу контенту.
    Зберігає назву, опис, автора та пов’язані статті.
    """
    __tablename__ = "content_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now)
    
    articles: Mapped[List["Article"]] = relationship("Article", back_populates="content_type", cascade="all, delete-orphan")