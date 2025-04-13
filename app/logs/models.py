# app/logs/models.py
from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    object_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    object_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    event_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Optionally, встановіть зв’язок з користувачем:
    user = relationship("User", back_populates="logs")
