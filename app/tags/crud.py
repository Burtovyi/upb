# app/tags/crud.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.tags import models, schemas

def get_tags(db: Session) -> List[models.Tag]:
    return db.query(models.Tag).all()

def get_tag(db: Session, tag_id: int) -> Optional[models.Tag]:
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()

def create_tag(db: Session, tag_in: schemas.TagCreate) -> models.Tag:
    tag = models.Tag(name=tag_in.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

def delete_tag(db: Session, tag: models.Tag) -> None:
    db.delete(tag)
    db.commit()
