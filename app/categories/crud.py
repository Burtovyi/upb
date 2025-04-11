from sqlalchemy.orm import Session
from typing import List, Optional
from app.categories import models, schemas

def get_categories(db: Session) -> List[models.Category]:
    """Повертає список всіх категорій."""
    return db.query(models.Category).all()

def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    """Повертає категорію за її ID або None, якщо не знайдено."""
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def create_category(db: Session, category_in: schemas.CategoryCreate) -> models.Category:
    """Створює нову категорію на основі даних із CategoryCreate."""
    new_category = models.Category(**category_in.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def update_category(db: Session, category: models.Category, category_in: schemas.CategoryUpdate) -> models.Category:
    """Оновлює дані категорії із використанням CategoryUpdate."""
    update_data = category_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category: models.Category) -> None:
    """Видаляє категорію з бази даних."""
    db.delete(category)
    db.commit()
