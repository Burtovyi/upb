# app/categories/crud.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.categories import models, schemas

def get_categories(db: Session) -> List[models.Category]:
    """
    Повертає список усіх категорій.
    """
    return db.query(models.Category).all()

def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    """
    Повертає категорію за її ID.
    Якщо категорію не знайдено, повертає None.
    """
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def create_category(db: Session, category_in: schemas.CategoryCreate) -> models.Category:
    """
    Створює нову категорію та додає її до бази даних.
    """
    category = models.Category(
        name=category_in.name,
        slug=category_in.slug
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def update_category(db: Session, category: models.Category, category_in: schemas.CategoryUpdate) -> models.Category:
    """
    Оновлює дані категорії на основі переданих даних у схемі CategoryUpdate.
    """
    if category_in.name is not None:
        category.name = category_in.name
    if category_in.slug is not None:
        category.slug = category_in.slug
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category: models.Category) -> None:
    """
    Видаляє категорію з бази даних.
    """
    db.delete(category)
    db.commit()
