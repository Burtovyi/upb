from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import List, Optional, Any
from app.authors import models, schemas
from app.articles.models import Article

def get_authors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Author]:
    """
    Повертає список всіх авторів з пагінацією.
    
    Args:
        db: Сесія бази даних.
        skip: Кількість авторів для пропуску (для пагінації).
        limit: Максимальна кількість авторів (для пагінації).
    
    Returns:
        List[models.Author]: Список авторів.
    
    Raises:
        HTTPException: Якщо сталася помилка бази даних.
    """
    try:
        return db.query(models.Author).offset(skip).limit(limit).all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при отриманні авторів")

def get_author(db: Session, author_id: int) -> Optional[models.Author]:
    """
    Повертає автора за ID або None, якщо не знайдено.
    
    Args:
        db: Сесія бази даних.
        author_id: ID автора.
    
    Returns:
        Optional[models.Author]: Автор або None.
    
    Raises:
        HTTPException: Якщо сталася помилка бази даних.
    """
    try:
        return db.query(models.Author).filter(models.Author.id == author_id).first()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при отриманні автора")

def create_author(db: Session, author_in: schemas.AuthorCreate, current_user: Any) -> models.Author:
    """
    Створює нового автора та додає його до бази даних.
    
    Args:
        db: Сесія бази даних.
        author_in: Дані для створення автора.
        current_user: Поточний користувач (для created_by).
    
    Returns:
        models.Author: Створений автор.
    
    Raises:
        HTTPException: Якщо ім'я вже існує або сталася помилка бази даних.
    """
    try:
        if db.query(models.Author).filter(models.Author.name == author_in.name).first():
            raise HTTPException(status_code=400, detail="Автор з таким ім'ям вже існує")
        new_author = models.Author(**author_in.dict(), created_by=current_user.id)
        db.add(new_author)
        db.commit()
        db.refresh(new_author)
        return new_author
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при створенні автора")

def update_author(db: Session, author: models.Author, author_in: schemas.AuthorUpdate) -> models.Author:
    """
    Оновлює дані автора з використанням даних із AuthorUpdate.
    
    Args:
        db: Сесія бази даних.
        author: Автор для оновлення.
        author_in: Дані для оновлення.
    
    Returns:
        models.Author: Оновлений автор.
    
    Raises:
        HTTPException: Якщо автор не знайдений, ім'я вже існує або сталася помилка бази даних.
    """
    if author is None:
        raise HTTPException(status_code=404, detail="Автор не знайдений")
    try:
        update_data = author_in.dict(exclude_unset=True)
        if "name" in update_data and update_data["name"] != author.name:
            if db.query(models.Author).filter(models.Author.name == update_data["name"]).first():
                raise HTTPException(status_code=400, detail="Автор з таким ім'ям вже існує")
        for key, value in update_data.items():
            setattr(author, key, value)
        db.commit()
        db.refresh(author)
        return author
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при оновленні автора")

def delete_author(db: Session, author: models.Author) -> None:
    """
    Видаляє автора з бази даних.
    
    Args:
        db: Сесія бази даних.
        author: Автор для видалення.
    
    Raises:
        HTTPException: Якщо автор не знайдений, має статті або сталася помилка бази даних.
    """
    if author is None:
        raise HTTPException(status_code=404, detail="Автор не знайдений")
    try:
        if db.query(Article).filter(Article.author_id == author.id).count() > 0:
            raise HTTPException(status_code=400, detail="Неможливо видалити автора, який має статті")
        db.delete(author)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при видаленні автора")