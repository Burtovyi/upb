from sqlalchemy.orm import Session
from typing import List, Optional
from app.articles import models, schemas

def get_articles(db: Session, skip: int = 0, limit: int = 100) -> List[models.Article]:
    """Повертає список статей із підтримкою пагінації."""
    return db.query(models.Article).offset(skip).limit(limit).all()

def get_article(db: Session, article_id: int) -> Optional[models.Article]:
    """Повертає статтю за її ID або None, якщо не знайдено."""
    return db.query(models.Article).filter(models.Article.id == article_id).first()

def create_article(db: Session, article_in: schemas.ArticleCreate) -> models.Article:
    """
    Створює нову статтю на основі даних із ArticleCreate.
    Якщо в article_in передано tag_ids (список ID тегів), виконується зв’язок статті з тегами.
    """
    # Створюємо нову статтю, виключаючи поле tag_ids, яке використовується лише для асоціації
    new_article = models.Article(**article_in.dict(exclude={"tag_ids"}))
    if article_in.tag_ids:
        from app.tags.models import Tag  # Імпорт для зменшення циклічних залежностей
        tags = db.query(Tag).filter(Tag.id.in_(article_in.tag_ids)).all()
        new_article.tags = tags
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

def update_article(db: Session, article: models.Article, article_in: schemas.ArticleUpdate) -> models.Article:
    """
    Оновлює статтю за даними з ArticleUpdate.
    Якщо передано tag_ids, оновлюється асоціація тегів.
    """
    update_data = article_in.dict(exclude_unset=True, exclude={"tag_ids"})
    for key, value in update_data.items():
        setattr(article, key, value)
    if "tag_ids" in article_in.dict():
        if article_in.tag_ids is not None:
            from app.tags.models import Tag
            tags = db.query(Tag).filter(Tag.id.in_(article_in.tag_ids)).all()
            article.tags = tags
    db.commit()
    db.refresh(article)
    return article

def delete_article(db: Session, article: models.Article) -> None:
    """Видаляє статтю з бази даних."""
    db.delete(article)
    db.commit()
