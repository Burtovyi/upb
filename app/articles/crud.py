from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import List, Optional
from datetime import datetime, timezone
from app.articles import models, schemas
from app.tags.models import Tag
from app.authors.models import Author
from app.categories.models import Category

def get_articles(db: Session, skip: int = 0, limit: int = 100) -> List[models.Article]:
    """
    Отримати список статей із пагінацією.
    
    Args:
        db: Сесія бази даних.
        skip: Кількість пропущених записів.
        limit: Максимальна кількість записів для повернення.
    
    Returns:
        List[models.Article]: Список статей.
    
    Raises:
        HTTPException: Якщо сталася помилка бази даних або параметри некоректні.
    """
    try:
        if skip < 0 or limit < 1:
            raise HTTPException(status_code=400, detail="skip має бути невід'ємним, а limit - позитивним")
        return db.query(models.Article).offset(skip).limit(limit).all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при отриманні статей")

def get_article(db: Session, article_id: int) -> Optional[models.Article]:
    """
    Отримати статтю за ID.
    
    Args:
        db: Сесія бази даних.
        article_id: ID статті.
    
    Returns:
        Optional[models.Article]: Стаття або None, якщо не знайдено.
    
    Raises:
        HTTPException: Якщо сталася помилка бази даних.
    """
    try:
        return db.query(models.Article).filter(models.Article.id == article_id).first()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при отриманні статті")

def create_article(db: Session, article_in: schemas.ArticleCreate) -> models.Article:
    """
    Створити нову статтю.
    
    Args:
        db: Сесія бази даних.
        article_in: Дані для створення статті.
    
    Returns:
        models.Article: Створена стаття.
    
    Raises:
        HTTPException: Якщо автор, категорія чи теги не знайдені, або сталася помилка бази даних.
    """
    try:
        # Перевіряємо існування автора
        author = db.query(Author).filter(Author.id == article_in.author_id).first()
        if not author:
            raise HTTPException(status_code=400, detail="Автор не знайдений")
        
        # Перевіряємо існування категорії
        category = db.query(Category).filter(Category.id == article_in.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Категорія не знайдена")
        
        # Створюємо статтю
        new_article = models.Article(
            title=article_in.title,
            description=article_in.description,
            content=article_in.content,
            view_count=article_in.view_count,
            author_id=article_in.author_id,
            category_id=article_in.category_id
        )
        
        # Обробляємо теги
        if article_in.tag_ids:
            tags = db.query(Tag).filter(Tag.id.in_(article_in.tag_ids)).all()
            if len(tags) != len(article_in.tag_ids):
                raise HTTPException(status_code=400, detail="Один або кілька тегів не знайдено")
            new_article.tags = tags
        
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        return new_article
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при створенні статті")

def update_article(db: Session, article: models.Article, article_in: schemas.ArticleUpdate) -> models.Article:
    """
    Оновити статтю.
    
    Args:
        db: Сесія бази даних.
        article: Існуюча стаття.
        article_in: Дані для оновлення статті.
    
    Returns:
        models.Article: Оновлена стаття.
    
    Raises:
        HTTPException: Якщо категорія чи теги не знайдені, або сталася помилка бази даних.
    """
    try:
        # Оновлюємо основні поля
        update_data = article_in.model_dump(exclude_unset=True, exclude={"tag_ids", "category_id"})
        for key, value in update_data.items():
            setattr(article, key, value)
        
        # Оновлюємо категорію, якщо передано
        if article_in.category_id is not None:
            category = db.query(Category).filter(Category.id == article_in.category_id).first()
            if not category:
                raise HTTPException(status_code=400, detail="Категорія не знайдена")
            article.category_id = article_in.category_id
        
        # Оновлюємо теги, якщо передано
        if article_in.tag_ids is not None:
            tags = db.query(Tag).filter(Tag.id.in_(article_in.tag_ids)).all()
            if len(tags) != len(article_in.tag_ids):
                raise HTTPException(status_code=400, detail="Один або кілька тегів не знайдено")
            article.tags = tags
        
        # Зберігаємо історію редагувань
        if update_data or article_in.tag_ids is not None or article_in.category_id is not None:
            history_entry = models.ArticleHistory(
                article_id=article.id,
                version_num=(db.query(models.ArticleHistory)
                            .filter(models.ArticleHistory.article_id == article.id)
                            .count() + 1),
                title=article.title,
                content=article.content,
                edited_at=datetime.now(timezone.utc),
                action="updated"
            )
            db.add(history_entry)
        
        db.commit()
        db.refresh(article)
        return article
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при оновленні статті")

def delete_article(db: Session, article: models.Article) -> None:
    """
    Видалити статтю.
    
    Args:
        db: Сесія бази даних.
        article: Стаття для видалення.
    
    Raises:
        HTTPException: Якщо сталася помилка бази даних.
    """
    try:
        db.delete(article)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при видаленні статті")