from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Any
from app.content_types import models, schemas
from fastapi import HTTPException

def get_content_types(db: Session, skip: int = 0, limit: int = 100) -> List[models.ContentType]:
    """
    Повертає список типів контенту з пагінацією.
    """
    return db.query(models.ContentType).offset(skip).limit(limit).all()

def get_content_type(db: Session, content_type_id: int) -> Optional[models.ContentType]:
    """
    Повертає тип контенту за його ID.
    Якщо запис не знайдено – повертає None.
    """
    return db.query(models.ContentType).filter(models.ContentType.id == content_type_id).first()

def create_content_type(db: Session, content_type_in: schemas.ContentTypeCreate, current_user: Any) -> models.ContentType:
    """
    Створює новий тип контенту на основі даних із ContentTypeCreate.
    Зберігає ID користувача, який створив тип контенту.
    """
    try:
        if not hasattr(current_user, "id"):
            raise HTTPException(status_code=400, detail="Некоректні дані користувача")
        existing_type = db.query(models.ContentType).filter(models.ContentType.name == content_type_in.name).first()
        if existing_type:
            raise HTTPException(status_code=400, detail="Тип контенту з таким ім’ям уже існує")
        content_type = models.ContentType(
            name=content_type_in.name,
            description=content_type_in.description,
            created_by=current_user.id
        )
        db.add(content_type)
        db.commit()
        db.refresh(content_type)
        return content_type
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при створенні типу контенту")

def update_content_type(db: Session, content_type: models.ContentType, content_type_in: schemas.ContentTypeUpdate) -> models.ContentType:
    """
    Оновлює існуючий тип контенту.
    """
    if content_type is None:
        raise HTTPException(status_code=404, detail="Тип контенту не знайдено")
    try:
        if content_type_in.name is not None:
            existing_type = db.query(models.ContentType).filter(models.ContentType.name == content_type_in.name).first()
            if existing_type and existing_type.id != content_type.id:
                raise HTTPException(status_code=400, detail="Тип контенту з таким ім’ям уже існує")
            content_type.name = content_type_in.name
        if content_type_in.description is not None:
            content_type.description = content_type_in.description
        db.commit()
        db.refresh(content_type)
        return content_type
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при оновленні типу контенту")

def delete_content_type(db: Session, content_type: models.ContentType, current_user: Any) -> None:
    """
    Видаляє тип контенту з бази даних.
    Дозволяє видалення лише адміністраторам.
    """
    if content_type is None:
        raise HTTPException(status_code=404, detail="Тип контенту не знайдено")
    try:
        if not hasattr(current_user, "role") or current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Недостатньо прав для видалення типу контенту")
        db.delete(content_type)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при видаленні типу контенту")