# app/tags/routes.py

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from app.tags import schemas, crud
from app.db.database import get_db
from app.auth.dependencies import get_current_user
from app.auth.models import User

router = APIRouter()

@router.get("/", response_model=List[schemas.TagOut])
def read_tags(db: Session = Depends(get_db)):
    return crud.get_tags(db)

@router.post("/", response_model=schemas.TagOut)
def create_tag(
    tag_in: schemas.TagCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_tag(db, tag_in)

@router.delete("/{tag_id}", status_code=204)
def delete_tag(
    tag_id: int = Path(..., description="ID тегу"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tag = crud.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Тег не знайдено")
    crud.delete_tag(db, tag)
    return
