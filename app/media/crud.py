from sqlalchemy.orm import Session
from app.media import models, schemas
from fastapi import HTTPException

def get_media(db: Session, media_id: int):
    return db.query(models.Media).filter(models.Media.id == media_id).first()

def create_media(db: Session, media_in: schemas.MediaCreate, current_user):
    """
    Створює новий запис медіа, прив'язаний до користувача (current_user).
    Припускається, що модель Media має поля: article_id, media_type, url, description, created_by.
    """
    new_media = models.Media(
        article_id=media_in.article_id,
        media_type=media_in.media_type,
        url=media_in.url,
        description=media_in.description,
        created_by=current_user.id  # Використовуємо current_user для збереження автора завантаження
    )
    db.add(new_media)
    db.commit()
    db.refresh(new_media)
    return new_media

def delete_media(db: Session, media_item, current_user):
    """
    Видаляє медіа-елемент.
    За потреби тут можна додати перевірку прав доступу, наприклад, дозволяти видалення лише власнику або адміну.
    """
    db.delete(media_item)
    db.commit()
