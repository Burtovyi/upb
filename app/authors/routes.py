# app/authors/routes.py

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from app.authors import schemas, crud
from app.db.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.AuthorOut])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_authors(db)

@router.get("/{author_id}", response_model=schemas.AuthorOut)
def read_author(
    author_id: int = Path(..., description="ID автора"),
    db: Session = Depends(get_db)
):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Автор не знайдений")
    return author

@router.post("/", response_model=schemas.AuthorOut)
def create_author(author_in: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author_in)

@router.put("/{author_id}", response_model=schemas.AuthorOut)
def update_author(
    author_id: int = Path(..., description="ID автора"),
    author_in: schemas.AuthorUpdate, 
    db: Session = Depends(get_db)
):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Автор не знайдений")
    return crud.update_author(db, author, author_in)

@router.delete("/{author_id}", status_code=204)
def delete_author(
    author_id: int = Path(..., description="ID автора"),
    db: Session = Depends(get_db)
):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Автор не знайдений")
    crud.delete_author(db, author)
    return
