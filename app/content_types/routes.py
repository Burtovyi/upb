from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from typing import List, Any
from app.content_types import schemas, crud
from app.db.database import get_db
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.ContentTypeOut], summary="Отримати список типів контенту")
def read_content_types(
    skip: int = Query(0, ge=0, description="Кількість записів для пропуску"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальна кількість записів"),
    db: Session = Depends(get_db)
):
    """Отримати усі типи контенту з пагінацією."""
    return crud.get_content_types(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.ContentTypeOut, summary="Створити тип контенту")
def create_content_type(
    content_type_in: schemas.ContentTypeCreate, 
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
):
    """Створити новий тип контенту."""
    if not hasattr(current_user, "role") or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Недостатньо прав для створення типу контенту")
    return crud.create_content_type(db, content_type_in, current_user)

@router.put("/{content_type_id}", response_model=schemas.ContentTypeOut, summary="Оновити тип контенту")
def update_content_type(
    content_type_in: schemas.ContentTypeUpdate, 
    content_type_id: int = Path(..., description="ID типу контенту", ge=1),
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
):
    """Оновити існуючий тип контенту."""
    if not hasattr(current_user, "role") or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Недостатньо прав для оновлення типу контенту")
    content_type = crud.get_content_type(db, content_type_id)
    if not content_type:
        raise HTTPException(status_code=404, detail="Тип контенту не знайдено")
    return crud.update_content_type(db, content_type, content_type_in)

@router.delete("/{content_type_id}", status_code=204, summary="Видалити тип контенту")
def delete_content_type(
    content_type_id: int = Path(..., description="ID типу контенту", ge=1),
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
):
    """Видалити тип контенту за ID."""
    if not hasattr(current_user, "role") or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Недостатньо прав для видалення типу контенту")
    content_type = crud.get_content_type(db, content_type_id)
    if not content_type:
        raise HTTPException(status_code=404, detail="Тип контенту не знайдено")
    crud.delete_content_type(db, content_type, current_user)
    return None