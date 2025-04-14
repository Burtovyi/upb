from sqlalchemy.orm import Session
from app.tags import models, schemas
from fastapi import HTTPException

def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tag).offset(skip).limit(limit).all()

def create_tag(db: Session, tag_in: schemas.TagCreate):
    new_tag = models.Tag(name=tag_in.name)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag

def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()

def update_tag(db: Session, tag: models.Tag, tag_update: schemas.TagUpdate):
    if tag_update.name is not None:
        tag.name = tag_update.name
    db.commit()
    db.refresh(tag)
    return tag

def delete_tag(db: Session, tag: models.Tag):
    db.delete(tag)
    db.commit()
