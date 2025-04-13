# app/metrics/models.py
from sqlalchemy import Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Metrics(Base):
    __tablename__ = "metrics"
    
    article_id: Mapped[int] = mapped_column(Integer, primary_key=True, name="article_id")
    view_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    like_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    comment_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    share_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
