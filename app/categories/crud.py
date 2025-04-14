from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import List, Optional, Any
from app.categories import models, schemas
from app.articles.models import Article  # Імпорт Article для перевірки

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
    """
    Повертає список всіх категорій з пагінацією.
    
    Args:
        db: Сесія бази даних.
        skip: Кількість категорій для пропуску (для пагінації).
        limit: Максимальна кількість категорій (для пагінації).
    
    Returns:
        List[models.Category]: Список категорій.
    """
    try:
        return db.query(models.Category).offset(skip).limit(limit).all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при отриманні категорій")

def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    """
    Повертає категорію за її ID або None, якщо не знайдено.
    
    Args:
        db: Сесія бази даних.
        category_id: ID категорії.
    
    Returns:
        Optional[models.Category]: Категорія або None.
    """
    try:
        return db.query(models.Category).filter(models.Category.id == category_id).first()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при отриманні категорії")

def create_category(db: Session, category_in: schemas.CategoryCreate, current_user: Any) -> models.Category:
    """
    Створює нову категорію на основі даних із CategoryCreate.
    
    Args:
        db: Сесія бази даних.
        category_in: Дані для створення категорії.
        current_user: Поточний користувач (для created_by).
    
    Returns:
        models.Category: Створена категорія.
    
    Raises:
        HTTPException: Якщо назва категорії вже існує.
    """
    try:
        if db.query(models.Category).filter(models.Category.name == category_in.name).first():
            raise HTTPException(status_code=400, detail="Категорія з такою назвою вже існує")
        new_category = models.Category(**category_in.dict(), created_by=current_user.id)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при створенні категорії")

def update_category(db: Session, category: models.Category, category_in: schemas.CategoryUpdate) -> models.Category:
    """
    Оновлює дані категорії із використанням CategoryUpdate.
    
    Args:
        db: Сесія бази даних.
        category: Категорія для оновлення.
        category_in: Дані для оновлення.
    
    Returns:
        models.Category: Оновлена категорія.
    
    Raises:
        HTTPException: Якщо категорія не знайдена або назва вже існує.
    """
    if category is None:
        raise HTTPException(status_code=404, detail="Категорію не знайдено")
    try:
        update_data = category_in.dict(exclude_unset=True)
        if "name" in update_data and update_data["name"] != category.name:
            if db.query(models.Category).filter(models.Category.name == update_data["name"]).first():
                raise HTTPException(status_code=400, detail="Категорія з такою назвою вже існує")
        for key, value in update_data.items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
        return category
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при оновленні категорії")

def delete_category(db: Session, category: models.Category) -> None:
    """
    Видаляє категорію з бази даних.
    
    Args:
        db: Сесія бази даних.
        category: Категорія для видалення.
    
    Raises:
        HTTPException: Якщо категорія не знайдена або використовується статтями.
    """
    if category is None:
        raise HTTPException(status_code=404, detail="Категорію не знайдено")
    try:
        if db.query(Article).filter(Article.category_id == category.id).count() > 0:
            raise HTTPException(status_code=400, detail="Неможливо видалити категорію, яка використовується статтями")
        db.delete(category)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при видаленні категорії")