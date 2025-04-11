# app/tags/models.py

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

# Асоціаційна таблиця для зв’язку статей і тегів
article_tags = Table(
    "article_tags",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.article_id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.tag_id", ondelete="CASCADE"), primary_key=True)
)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True, name="tag_id")
    name = Column(String(100), nullable=False)
    
    # Зв’язок багато-до-багатьох зі статтями
    articles = relationship("Article", secondary=article_tags, back_populates="tags")
