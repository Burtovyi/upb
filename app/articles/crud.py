# app/articles/crud.py

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.articles import models, schemas

def get_article(db: Session, article_id: int) -> Optional[models.Article]:
    """Отримує статтю за її ID."""
    return db.query(models.Article).filter(models.Article.id == article_id).first()

def get_articles(db: Session, skip: int = 0, limit: int = 10, status: str = "published") -> List[models.Article]:
    """
    Отримує список статей із заданим статусом.
    За замовчуванням повертаються лише опубліковані статті.
    """
    query = db.query(models.Article)
    if status:
        query = query.filter(models.Article.status == status)
    return query.offset(skip).limit(limit).all()

def create_article(db: Session, article_in: schemas.ArticleCreate, current_user) -> models.Article:
    """
    Створює нову статтю.
    Передбачається, що current_user відповідає запису автора, тому його id записується в author_id.
    Статус статті встановлюється як "draft".
    """
    article = models.Article(
        title=article_in.title,
        summary=article_in.summary,
        content=article_in.content,
        category_id=article_in.category_id,
        content_type_id=article_in.content_type_id,
        author_id=current_user.id,
        status=models.ArticleStatusEnum.draft
    )
    # Якщо передані теги, виконуємо запит до таблиці тегів і встановлюємо зв’язок
    if article_in.tag_ids:
        from app.tags.models import Tag  # Імпорт тут для уникнення циклічних імпортів
        tags = db.query(Tag).filter(Tag.id.in_(article_in.tag_ids)).all()
        article.tags = tags

    db.add(article)
    db.commit()
    db.refresh(article)
    return article

def update_article(db: Session, article: models.Article, article_in: schemas.ArticleUpdate, current_user) -> models.Article:
    """
    Оновлює поля статті.
    При зміні статусу, якщо він стає "published", встановлюється час публікації.
    Також оновлюється зв’язок з тегами, якщо передані нові значення.
    """
    if article_in.title is not None:
        article.title = article_in.title
    if article_in.summary is not None:
        article.summary = article_in.summary
    if article_in.content is not None:
        article.content = article_in.content
    if article_in.category_id is not None:
        article.category_id = article_in.category_id
    if article_in.content_type_id is not None:
        article.content_type_id = article_in.content_type_id
    if article_in.status is not None:
        article.status = article_in.status
        if article_in.status == models.ArticleStatusEnum.published:
            article.published_at = datetime.utcnow()

    if article_in.tag_ids is not None:
        from app.tags.models import Tag  # Імпорт для роботи із зв’язками
        tags = db.query(Tag).filter(Tag.id.in_(article_in.tag_ids)).all()
        article.tags = tags

    db.commit()
    db.refresh(article)
    return article

def delete_article(db: Session, article: models.Article, current_user):
    """
    Видаляє статтю.
    Перед видаленням можна реалізувати перевірку прав доступу (чи дозволено видаляти поточному користувачу).
    """
    db.delete(article)
    db.commit()
