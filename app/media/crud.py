# app/media/crud.py

import os
import uuid
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.media.models import Media

# Якщо хочете робити асинхронний запис файлів, можна використати aiofiles.
# Для простоти тут використовується стандартний open(), що працює синхронно.

async def upload_media(db: Session, article_id: int, file: UploadFile, description: str, current_user) -> Media:
    """
    Завантажує файл із UploadFile та створює запис у таблиці Media.
    
    1. Перевіряє наявність папки для завантажень (uploads), створює її, якщо необхідно.
    2. Генерує унікальне ім'я файлу (зберігаючи розширення).
    3. Зчитує вміст файлу та записує його на диск.
    4. На основі MIME-типу файлу визначає, чи це зображення чи відео.
    5. Створює запис Media з даними про файл та прив'язує його до article_id.
    
    Повертає створений об'єкт Media.
    """
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # Отримуємо вихідне ім'я файлу та визначаємо розширення
    original_filename = file.filename
    extension = os.path.splitext(original_filename)[1] if original_filename else ""
    unique_filename = f"{uuid.uuid4()}{extension}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Зчитуємо дані файлу (асинхронно)
    file_bytes = await file.read()
    
    # Записуємо дані на диск. (Зауваження: для асинхронного запису можна використати aiofiles)
    with open(file_path, "wb") as f:
        f.write(file_bytes)
    
    # Визначаємо тип медіа за MIME-типом
    if file.content_type.startswith("image"):
        media_type = "image"
    elif file.content_type.startswith("video"):
        media_type = "video"
    else:
        media_type = "other"
    
    # Створюємо об'єкт Media з переданими даними
    media_obj = Media(
        media_type=media_type,
        url=file_path,  # Зберігаємо локальний шлях до файлу
        description=description,
        article_id=article_id
    )
    
    db.add(media_obj)
    db.commit()
    db.refresh(media_obj)
    return media_obj

def get_media(db: Session, media_id: int):
    """
    Повертає об'єкт Media за його ID із бази даних.
    Якщо запис не знайдено – повертає None.
    """
    return db.query(Media).filter(Media.id == media_id).first()

def delete_media(db: Session, media_obj: Media, current_user):
    """
    Видаляє об'єкт Media із бази даних та видаляє файл із файлової системи.
    Перевірка прав доступу для current_user може бути додана за потреби.
    """
    # Видаляємо файл, якщо він існує
    if os.path.exists(media_obj.url):
        os.remove(media_obj.url)
    
    db.delete(media_obj)
    db.commit()
