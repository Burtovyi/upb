from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError  # Додаємо імпорт
from typing import List, Any
from app.comments import schemas, crud, models
from app.db.database import get_db
from app.auth.dependencies import get_current_active_user

router = APIRouter()

@router.get("/article/{article_id}", response_model=List[schemas.CommentOut], summary="Отримати коментарі до статті")
def read_comments(
    article_id: int = Path(..., description="ID статті", ge=1),
    skip: int = Query(0, ge=0, description="Кількість коментарів для пропуску"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальна кількість коментарів"),
    db: Session = Depends(get_db)
):
    """Отримати усі коментарі для вказаної статті з пагінацією."""
    comments = crud.get_comments_by_article(db, article_id, skip=skip, limit=limit)
    return comments

@router.post("/", response_model=schemas.CommentOut, summary="Створити коментар")
def create_comment(
    comment_in: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user)
):
    """Створити новий коментар до статті."""
    try:
        return crud.create_comment(db, comment_in, current_user)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при створенні коментаря")

@router.get("/{comment_id}", response_model=schemas.CommentOut, summary="Отримати коментар")
def read_comment(
    comment_id: int = Path(..., description="ID коментаря", ge=1),
    db: Session = Depends(get_db)
):
    """Отримати коментар за його ID."""
    comment = crud.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")
    return comment

@router.put("/{comment_id}", response_model=schemas.CommentOut, summary="Оновити коментар")
def update_comment(
    comment_in: schemas.CommentUpdate,
    comment_id: int = Path(..., description="ID коментаря", ge=1),
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user)
):
    """Оновити існуючий коментар."""
    comment = crud.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")
    if comment.author_id != current_user.id and (not hasattr(current_user, "role") or current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Недостатньо прав для редагування коментаря")
    try:
        return crud.update_comment(db, comment, comment_in, current_user)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при оновленні коментаря")

@router.delete("/{comment_id}", status_code=204, summary="Видалити коментар")
def delete_comment(
    comment_id: int = Path(..., description="ID коментаря", ge=1),
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user)
):
    """Видалити коментар за його ID."""
    comment = crud.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")
    if comment.author_id != current_user.id and (not hasattr(current_user, "role") or current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Недостатньо прав для видалення коментаря")
    try:
        crud.delete_comment(db, comment, current_user)
        return None
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при видаленні коментаря")