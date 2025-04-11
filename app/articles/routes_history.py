# app/articles/routes_history.py

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from app.articles import article_history_schemas as schemas  # схеми історії
from app.articles import crud_history as crud  # CRUD для історії статей
from app.db.database import get_db

router = APIRouter()

@router.get("/history/{article_id}", response_model=List[schemas.ArticleHistoryOut])
def read_article_history(
    article_id: int = Path(..., description="ID статті"),
    db: Session = Depends(get_db)
):
    history = crud.get_article_history(db, article_id)
    if not history:
        raise HTTPException(status_code=404, detail="Історію для цієї статті не знайдено")
    return history

@router.post("/history/{article_id}", response_model=schemas.ArticleHistoryOut)
def create_article_history(
    version_num: int,
    article_id: int = Path(..., description="ID статті"),
    title: str = None,
    content: str = None,
    action: str = None,
    db: Session = Depends(get_db)
):
    return crud.create_article_history(db, article_id, version_num, title, content, action)
