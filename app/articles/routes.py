from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.articles import schemas, crud
from app.db.database import get_db
from app.auth.dependencies import get_current_active_user

router = APIRouter()

@router.get("/", response_model=list[schemas.ArticleOut])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_articles(db, skip=skip, limit=limit)

@router.get("/{article_id}", response_model=schemas.ArticleOut)
def read_article(article_id: int = Path(..., description="ID статті"), db: Session = Depends(get_db)):
    article = crud.get_article(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Статтю не знайдено")
    return article

@router.post("/", response_model=schemas.ArticleOut)
def create_article(article_in: schemas.ArticleCreate, db: Session = Depends(get_db),
                   current_user = Depends(get_current_active_user)):
    # Якщо роль user – встановити author_id на себе (ігноруючи переданий)
    if current_user.role == "user":
        article_in.author_id = current_user.id
    return crud.create_article(db, article_in)

@router.put("/{article_id}", response_model=schemas.ArticleOut)
def update_article(article_in: schemas.ArticleUpdate,
                   article_id: int = Path(..., description="ID статті"),
                   db: Session = Depends(get_db),
                   current_user = Depends(get_current_active_user)):
    article = crud.get_article(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Статтю не знайдено")
    # Дозволено автору (якщо звичайний користувач) або редакторам/адмінам
    if current_user.role not in ("admin", "editor") and article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостатньо прав для оновлення статті")
    return crud.update_article(db, article, article_in)

@router.delete("/{article_id}", status_code=204)
def delete_article(article_id: int = Path(..., description="ID статті"),
                   db: Session = Depends(get_db),
                   current_user = Depends(get_current_active_user)):
    article = crud.get_article(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Статтю не знайдено")
    # Дозволено автору або редакторам/адмінам
    if current_user.role not in ("admin", "editor") and article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостатньо прав для видалення статті")
    crud.delete_article(db, article)
    return
