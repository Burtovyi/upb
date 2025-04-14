from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.comments import models, schemas
from app.articles.models import Article  # Імпорт Article
from typing import List, Optional, Any

def get_comments_by_article(db: Session, article_id: int, skip: int = 0, limit: int = 100) -> List[models.Comment]:
    """
    Повертає список коментарів для статті за її ID.
    
    Args:
        db: Сесія бази даних.
        article_id: ID статті.
        skip: Кількість коментарів для пропуску (для пагінації).
        limit: Максимальна кількість коментарів (для пагінації).
    
    Returns:
        List[models.Comment]: Список коментарів.
    """
    return db.query(models.Comment).filter(models.Comment.article_id == article_id).offset(skip).limit(limit).all()

def create_comment(db: Session, comment_in: schemas.CommentCreate, current_user: Any) -> models.Comment:
    """
    Створює новий коментар для статті від поточного користувача.
    
    Args:
        db: Сесія бази даних.
        comment_in: Дані для створення коментаря.
        current_user: Поточний користувач.
    
    Returns:
        models.Comment: Створений коментар.
    
    Raises:
        HTTPException: Якщо стаття або батьківський коментар не знайдені.
    """
    try:
        article = db.query(Article).filter(Article.id == comment_in.article_id).first()
        if not article:
            raise HTTPException(status_code=404, detail="Стаття не знайдена")
        if comment_in.parent_id:
            parent = db.query(models.Comment).filter(models.Comment.id == comment_in.parent_id).first()
            if not parent:
                raise HTTPException(status_code=404, detail="Батьківський коментар не знайдено")
        if not hasattr(current_user, "is_active") or not current_user.is_active:
            raise HTTPException(status_code=403, detail="Користувач не активний")
        new_comment = models.Comment(
            content=comment_in.content,
            parent_id=comment_in.parent_id,
            article_id=comment_in.article_id,
            author_id=current_user.id
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при створенні коментаря")

def get_comment(db: Session, comment_id: int) -> Optional[models.Comment]:
    """
    Повертає коментар за заданим ID.
    
    Args:
        db: Сесія бази даних.
        comment_id: ID коментаря.
    
    Returns:
        Optional[models.Comment]: Коментар або None, якщо не знайдено.
    """
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def update_comment(db: Session, comment: models.Comment, comment_in: schemas.CommentUpdate, current_user: Any) -> models.Comment:
    """
    Оновлює коментар.
    Лише автор або користувач з роллю admin/editor має право редагувати.
    
    Args:
        db: Сесія бази даних.
        comment: Коментар для оновлення.
        comment_in: Дані для оновлення.
        current_user: Поточний користувач.
    
    Returns:
        models.Comment: Оновлений коментар.
    
    Raises:
        HTTPException: Якщо коментар не знайдено або недостатньо прав.
    """
    if comment is None:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")
    try:
        if current_user.role not in ("admin", "editor") and comment.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Недостатньо прав для редагування коментаря")
        if comment_in.content is not None:
            comment.content = comment_in.content
        if comment_in.parent_id is not None:
            if comment_in.parent_id:
                parent = db.query(models.Comment).filter(models.Comment.id == comment_in.parent_id).first()
                if not parent:
                    raise HTTPException(status_code=404, detail="Батьківський коментар не знайдено")
            comment.parent_id = comment_in.parent_id
        db.commit()
        db.refresh(comment)
        return comment
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при оновленні коментаря")

def delete_comment(db: Session, comment: models.Comment, current_user: Any) -> None:
    """
    Видаляє коментар.
    Лише автор або користувач з роллю admin/editor має право видаляти.
    
    Args:
        db: Сесія бази даних.
        comment: Коментар для видалення.
        current_user: Поточний користувач.
    
    Raises:
        HTTPException: Якщо коментар не знайдено або недостатньо прав.
    """
    if comment is None:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")
    try:
        if current_user.role not in ("admin", "editor") and comment.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Недостатньо прав для видалення коментаря")
        db.delete(comment)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при видаленні коментаря")