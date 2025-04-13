from sqlalchemy.orm import Session
from typing import List, Optional
from app.content_types import models, schemas

def get_content_types(db: Session) -> List[models.ContentType]:
    """
    Повертає список усіх типів контенту.
    """
    return db.query(models.ContentType).all()

def get_content_type(db: Session, content_type_id: int) -> Optional[models.ContentType]:
    """
    Повертає тип контенту за його ID.
    Якщо запис не знайдено – повертає None.
    """
    return db.query(models.ContentType).filter(models.ContentType.id == content_type_id).first()

def create_content_type(db: Session, content_type_in: schemas.ContentTypeCreate) -> models.ContentType:
    """
    Створює новий тип контенту на основі даних із ContentTypeCreate.
    """
    content_type = models.ContentType(name=content_type_in.name)
    db.add(content_type)
    db.commit()
    db.refresh(content_type)
    return content_type

def update_content_type(db: Session, content_type: models.ContentType, content_type_in: schemas.ContentTypeUpdate) -> models.ContentType:
    """
    Оновлює існуючий тип контенту.
    """
    update_data = content_type_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(content_type, key, value)
    db.commit()
    db.refresh(content_type)
    return content_type

def delete_content_type(db: Session, content_type: models.ContentType, current_user) -> None:
    """
    Видаляє тип контенту з бази даних.
    (При потребі додати перевірку прав current_user.)
    """
    db.delete(content_type)
    db.commit()
