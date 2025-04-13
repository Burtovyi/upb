from typing import List, Optional
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class ContentType(Base):
    __tablename__ = "content_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, name="type_id")
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    articles: Mapped[List["Article"]] = relationship("Article", back_populates="content_type", cascade="all, delete-orphan")
