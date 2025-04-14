from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Any
from app.categories import schemas, crud
from app.db.database import get_db
from app.auth.dependencies import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[schemas.CategoryOut], summary="Отримати усі категорії")
def read_categories(
    skip: int = Query(0, ge=0, description="Кількість категорій для пропуску"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальна кількість категорій"),
    db: Session = Depends(get_db)
):
    """Отримати список категорій з пагінацією."""
    try:
        return crud.get_categories(db, skip=skip, limit=limit)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при отриманні категорій")

@router.post("/", response_model=schemas.CategoryOut, summary="Створити категорію")
def create_category(
    category_in: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user)
):
    """Створити нову категорію."""
    try:
        if current_user.role not in ("admin", "editor"):
            raise HTTPException(status_code=403, detail="Недостатньо прав для створення категорії")
        return crud.create_category(db, category_in, current_user)  # Додаємо current_user
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при створенні категорії")

@router.get("/{category_id}", response_model=schemas.CategoryOut, summary="Отримати категорію")
def read_category(
    category_id: int = Path(..., description="ID категорії", ge=1),
    db: Session = Depends(get_db)
):
    """Отримати категорію за її ID."""
    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категорію не знайдено")
    return category

@router.put("/{category_id}", response_model=schemas.CategoryOut, summary="Оновити категорію")
def update_category(
    category_in: schemas.CategoryUpdate,
    category_id: int = Path(..., description="ID категорії", ge=1),
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user)
):
    """Оновити існуючу категорію."""
    try:
        category = crud.get_category(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Категорію не знайдено")
        if current_user.role not in ("admin", "editor"):
            raise HTTPException(status_code=403, detail="Недостатньо прав для редагування категорії")
        return crud.update_category(db, category, category_in)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при оновленні категорії")

@router.delete("/{category_id}", status_code=204, summary="Видалити категорію")
def delete_category(
    category_id: int = Path(..., description="ID категорії", ge=1),
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user)
):
    """Видалити категорію за її ID."""
    try:
        category = crud.get_category(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Категорію не знайдено")
        if current_user.role not in ("admin", "editor"):
            raise HTTPException(status_code=403, detail="Недостатньо прав для видалення категорії")
        crud.delete_category(db, category)
        return None
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при видаленні категорії")