from sqlalchemy.orm import Session
from typing import List, Optional
from app.metrics import models, schemas

def get_all_metrics(db: Session) -> List[models.Metrics]:
    return db.query(models.Metrics).all()

def get_metrics_by_article(db: Session, article_id: int) -> Optional[models.Metrics]:
    return db.query(models.Metrics).filter(models.Metrics.article_id == article_id).first()

def create_metrics(db: Session, metrics_in: schemas.MetricsCreate) -> models.Metrics:
    metrics = models.Metrics(**metrics_in.dict())
    db.add(metrics)
    db.commit()
    db.refresh(metrics)
    return metrics

def update_metrics(db: Session, metrics: models.Metrics, metrics_in: schemas.MetricsUpdate) -> models.Metrics:
    update_data = metrics_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(metrics, key, value)
    db.commit()
    db.refresh(metrics)
    return metrics

def delete_metrics(db: Session, metrics: models.Metrics) -> None:
    db.delete(metrics)
    db.commit()
