import os
import uuid
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.media.models import Media

async def upload_media(
    db: Session, article_id: int, file: UploadFile, description: str, current_user
) -> Media:
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    original_filename = file.filename
    extension = os.path.splitext(original_filename)[1] if original_filename else ""
    unique_filename = f"{uuid.uuid4()}{extension}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    file_bytes = await file.read()
    
    with open(file_path, "wb") as f:
        f.write(file_bytes)
    
    if file.content_type.startswith("image"):
        media_type = "image"
    elif file.content_type.startswith("video"):
        media_type = "video"
    else:
        media_type = "other"
    
    media_obj = Media(
        media_type=media_type,
        url=file_path,
        description=description,
        article_id=article_id
    )
    
    db.add(media_obj)
    db.commit()
    db.refresh(media_obj)
    return media_obj

def get_media(db: Session, media_id: int):
    return db.query(Media).filter(Media.id == media_id).first()

def delete_media(db: Session, media_obj: Media, current_user):
    if os.path.exists(media_obj.url):
        os.remove(media_obj.url)
    db.delete(media_obj)
    db.commit()
