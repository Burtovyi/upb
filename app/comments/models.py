from sqlalchemy import Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.database import Base
from datetime import datetime
from typing import List, Optional

class Comment(Base):
    """
    Модель коментаря.
    Зберігає вміст, зв’язки з автором, статтею, батьківським коментарем і відповідями.
    """
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    article: Mapped["Article"] = relationship("Article", back_populates="comments")
    author: Mapped["User"] = relationship("User", back_populates="comments")
    replies: Mapped[List["Comment"]] = relationship("Comment", back_populates="parent", remote_side=[id])
    parent: Mapped[Optional["Comment"]] = relationship("Comment", back_populates="replies")