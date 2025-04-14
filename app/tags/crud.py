from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.tags import models, schemas
from fastapi import HTTPException

def get_tags(db: Session, skip: int = 0, limit: int = 100):
    if skip < 0:
        raise HTTPException(status_code=400, detail="Параметр skip не може бути від'ємним")
    if limit < 1 or limit > 1000:
        raise HTTPException(status_code=400, detail="Параметр limit має бути від 1 до 1000")
    return db.query(models.Tag).offset(skip).limit(limit).all()

def create_tag(db: Session, tag_in: schemas.TagCreate):
    try:
        existing_tag = db.query(models.Tag).filter(models.Tag.name == tag_in.name).first()
        if existing_tag:
            raise HTTPException(status_code=400, detail="Тег із таким ім'ям уже існує")
        new_tag = models.Tag(name=tag_in.name)
        db.add(new_tag)
        db.commit()
        db.refresh(new_tag)
        return new_tag
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при створенні тегу")

def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.tag_id == tag_id).first()

def update_tag(db: Session, tag: models.Tag, tag_update: schemas.TagUpdate):
    if tag is None:
        raise HTTPException(status_code=404, detail="Тег не знайдено")
    try:
        if tag_update.name is not None:
            if tag_update.name != tag.name:
                existing_tag = db.query(models.Tag).filter(models.Tag.name == tag_update.name).first()
                if existing_tag and existing_tag.id != tag.id:
                    raise HTTPException(status_code=400, detail="Тег із таким ім'ям уже існує")
                tag.name = tag_update.name
        db.commit()
        db.refresh(tag)
        return tag
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при оновленні тегу")

def delete_tag(db: Session, tag: models.Tag):
    if tag is None:
        raise HTTPException(status_code=404, detail="Тег не знайдено")
    try:
        db.delete(tag)
        db.commit()
        return None
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при видаленні тегу")