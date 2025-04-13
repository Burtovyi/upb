from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from app.metrics import schemas, crud
from app.db.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.MetricsOut])
def read_all_metrics(db: Session = Depends(get_db)):
    metrics_list = crud.get_all_metrics(db)
    if not metrics_list:
        raise HTTPException(status_code=404, detail="Метрики не знайдено")
    return metrics_list

@router.get("/{article_id}", response_model=schemas.MetricsOut)
def read_metrics(
    article_id: int = Path(..., description="ID статті"),
    db: Session = Depends(get_db)
):
    metrics = crud.get_metrics_by_article(db, article_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="Метрики не знайдено")
    return metrics

@router.post("/", response_model=schemas.MetricsOut)
def create_metrics(
    metrics_in: schemas.MetricsCreate,
    db: Session = Depends(get_db)
):
    return crud.create_metrics(db, metrics_in)

@router.put("/{article_id}", response_model=schemas.MetricsOut)
def update_metrics(
    metrics_in: schemas.MetricsUpdate,
    article_id: int = Path(..., description="ID статті"),
    db: Session = Depends(get_db)
):
    metrics = crud.get_metrics_by_article(db, article_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="Метрики не знайдено")
    return crud.update_metrics(db, metrics, metrics_in)

@router.delete("/{article_id}", status_code=204)
def delete_metrics(
    article_id: int = Path(..., description="ID статті"),
    db: Session = Depends(get_db)
):
    metrics = crud.get_metrics_by_article(db, article_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="Метрики не знайдено")
    crud.delete_metrics(db, metrics)
    return
