from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from app.comments import schemas, crud
from app.db.database import get_db
from app.auth.dependencies import get_current_user
from app.auth.models import User

router = APIRouter()

@router.get("/article/{article_id}", response_model=List[schemas.CommentOut])
def read_comments_for_article(
    article_id: int = Path(..., description="ID статті"),
    db: Session = Depends(get_db)
):
    return crud.get_comments_by_article(db, article_id)

@router.post("/article/{article_id}", response_model=schemas.CommentOut)
def create_comment(
    comment_in: schemas.CommentCreate, 
    article_id: int = Path(..., description="ID статті"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_comment(db, article_id, comment_in, current_user)

@router.put("/{comment_id}", response_model=schemas.CommentOut)
def update_comment(
    comment_in: schemas.CommentUpdate, 
    comment_id: int = Path(..., description="ID коментаря"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = crud.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")
    return crud.update_comment(db, comment, comment_in, current_user)

@router.delete("/{comment_id}", status_code=204)
def delete_comment(
    comment_id: int = Path(..., description="ID коментаря"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = crud.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")
    crud.delete_comment(db, comment, current_user)
    return
