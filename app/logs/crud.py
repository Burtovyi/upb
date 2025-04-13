# app/logs/crud.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.logs import models, schemas

def get_logs(db: Session) -> List[models.Log]:
    return db.query(models.Log).all()

def get_log(db: Session, log_id: int) -> Optional[models.Log]:
    return db.query(models.Log).filter(models.Log.id == log_id).first()

def create_log(db: Session, log_in: schemas.LogCreate) -> models.Log:
    log_entry = models.Log(**log_in.dict())
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry

def delete_log(db: Session, log_entry: models.Log) -> None:
    db.delete(log_entry)
    db.commit()
