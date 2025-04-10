# app/articles/routes.py

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from typing import List
from app.articles import schemas, crud
from app.db.database import get_db
from app.auth.dependencies import get_current_user
from app.auth.models import User

router = APIRouter()

@router.get("/", response_model=List[schemas.ArticleOut])
def read_articles(
    skip: int = 0, 
    limit: int = 10, 
    status: str = Query("published", description="Фільтр за статусом (draft, moderation, published)"),
    db: Session = Depends(get_db)
):
    articles = crud.get_articles(db, skip=skip, limit=limit, status=status)
    return articles

@router.get("/{article_id}", response_model=schemas.ArticleDetail)
def read_article(
    article_id: int = Path(..., description="ID статті"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    article = crud.get_article(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Статтю не знайдено")
    # Додаткова перевірка: якщо стаття не опублікована, доступ дозволяється тільки автору/редактору/адміну
    return article

@router.post("/", response_model=schemas.ArticleOut)
def create_article(
    article_in: schemas.ArticleCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_article(db, article_in, current_user)

@router.put("/{article_id}", response_model=schemas.ArticleOut)
def update_article(
    article_id: int,
    article_in: schemas.ArticleUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    article = crud.get_article(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Статтю не знайдено")
    updated_article = crud.update_article(db, article, article_in, current_user)
    return updated_article

@router.delete("/{article_id}", status_code=204)
def delete_article(
    article_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    article = crud.get_article(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Статтю не знайдено")
    crud.delete_article(db, article, current_user)
    return
