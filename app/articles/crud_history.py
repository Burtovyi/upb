from sqlalchemy.orm import Session
from typing import List, Optional
from app.articles import models, article_history_schemas as schemas

def get_article_history(db: Session, article_id: int) -> List[models.ArticleHistory]:
    """Повертає список історичних записів для заданої статті, відсортованих за датою редагування."""
    return db.query(models.ArticleHistory).filter(models.ArticleHistory.article_id == article_id).order_by(models.ArticleHistory.edited_at.desc()).all()

def get_article_history_entry(db: Session, history_id: int) -> Optional[models.ArticleHistory]:
    """Повертає запис історії статті за його ID."""
    return db.query(models.ArticleHistory).filter(models.ArticleHistory.id == history_id).first()

def create_article_history(db: Session, article_id: int, version_num: int, title: Optional[str] = None, content: Optional[str] = None, action: Optional[str] = None) -> models.ArticleHistory:
    """Створює новий запис історії для статті."""
    history = models.ArticleHistory(
        article_id=article_id,
        version_num=version_num,
        title=title,
        content=content,
        action=action
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history

def delete_article_history(db: Session, history_entry: models.ArticleHistory) -> None:
    """Видаляє запис історії статті."""
    db.delete(history_entry)
    db.commit()
