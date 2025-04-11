# app/categories/routes.py

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from app.categories import schemas, crud  # імпортуємо схеми і CRUD функції для категорій
from app.db.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.CategoryOut])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

@router.get("/{category_id}", response_model=schemas.CategoryOut)
def read_category(
    category_id: int = Path(..., description="ID категорії"),
    db: Session = Depends(get_db)
):
    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категорію не знайдено")
    return category

@router.post("/", response_model=schemas.CategoryOut)
def create_category(
    category_in: schemas.CategoryCreate, 
    db: Session = Depends(get_db)
):
    return crud.create_category(db, category_in)

@router.put("/{category_id}", response_model=schemas.CategoryOut)
def update_category(
    category_in: schemas.CategoryUpdate, 
    category_id: int = Path(..., description="ID категорії"),
    db: Session = Depends(get_db)
):
    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категорію не знайдено")
    return crud.update_category(db, category, category_in)

@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int = Path(..., description="ID категорії"),
    db: Session = Depends(get_db)
):
    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категорію не знайдено")
    crud.delete_category(db, category)
    return
