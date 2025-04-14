from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.comments import schemas, crud, models
from app.db.database import get_db
from app.auth.dependencies import get_current_active_user

router = APIRouter()

@router.get("/article/{article_id}", response_model=list[schemas.CommentOut])
def read_comments(article_id: int = Path(..., description="ID статті"), db: Session = Depends(get_db)):
    comments = crud.get_comments_by_article(db, article_id)
    return comments

@router.post("/", response_model=schemas.CommentOut)
def create_comment(
    comment_in: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return crud.create_comment(db, comment_in, current_user)

@router.get("/{comment_id}", response_model=schemas.CommentOut)
def read_comment(comment_id: int = Path(..., description="ID коментаря"), db: Session = Depends(get_db)):
    comment = crud.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")
    return comment

@router.put("/{comment_id}", response_model=schemas.CommentOut)
def update_comment(
    comment_in: schemas.CommentUpdate,
    comment_id: int = Path(..., description="ID коментаря"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    comment = crud.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")
    return crud.update_comment(db, comment, comment_in, current_user)

@router.delete("/{comment_id}", status_code=204)
def delete_comment(
    comment_id: int = Path(..., description="ID коментаря"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    comment = crud.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")
    crud.delete_comment(db, comment, current_user)
    return
