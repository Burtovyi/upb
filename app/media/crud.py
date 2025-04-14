from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.media import models, schemas
from app.articles.models import Article
from fastapi import HTTPException
from typing import Any

def get_media(db: Session, media_id: int):
    return db.query(models.Media).filter(models.Media.id == media_id).first()

def create_media(db: Session, media_in: schemas.MediaCreate, current_user: Any):
    """
    Створює новий запис медіа, прив'язаний до користувача (current_user).
    Припускається, що модель Media має поля: article_id, media_type, url, description, created_by.
    """
    try:
        if not hasattr(current_user, 'id'):
            raise HTTPException(status_code=400, detail="Некоректні дані користувача")
        article = db.query(Article).filter(Article.id == media_in.article_id).first()
        if not article:
            raise HTTPException(status_code=404, detail="Стаття не знайдена")
        allowed_types = {"image", "video", "audio"}
        if media_in.media_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Недопустимий тип медіа")
        new_media = models.Media(
            article_id=media_in.article_id,
            media_type=media_in.media_type,
            url=media_in.url,
            description=media_in.description,
            created_by=current_user.id
        )
        db.add(new_media)
        db.commit()
        db.refresh(new_media)
        return new_media
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при створенні медіа")

def delete_media(db: Session, media_item: models.Media, current_user: Any):
    """
    Видаляє медіа-елемент.
    Дозволяє видалення лише власнику або адміну.
    """
    try:
        if media_item is None:
            raise HTTPException(status_code=404, detail="Медіа не знайдено")
        if not hasattr(current_user, 'id'):
            raise HTTPException(status_code=400, detail="Некоректні дані користувача")
        if media_item.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Недостатньо прав для видалення медіа")
        db.delete(media_item)
        db.commit()
        return None
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при видаленні медіа")