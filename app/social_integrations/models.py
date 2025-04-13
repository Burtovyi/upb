# app/social_integrations/models.py
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class SocialIntegration(Base):
    __tablename__ = "social_integrations"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    platform: Mapped[str] = mapped_column(String(20), nullable=False)  # Наприклад: 'Telegram', 'Twitter', 'TikTok', etc.
    account_ref: Mapped[str] = mapped_column(String(100), nullable=False)  # Ідентифікатор акаунта або токен
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    added_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Зв’язок із автором (користувачем)
    author: Mapped["User"] = relationship("User", back_populates="social_integrations")
