from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.categories import schemas, crud
from app.db.database import get_db
from app.auth.dependencies import get_current_active_user

router = APIRouter()

@router.get("/", response_model=list[schemas.CategoryOut])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

@router.post("/", response_model=schemas.CategoryOut)
def create_category(category_in: schemas.CategoryCreate, db: Session = Depends(get_db),
                    current_user = Depends(get_current_active_user)):
    if current_user.role not in ("admin", "editor"):
        raise HTTPException(status_code=403, detail="Недостатньо прав для створення категорії")
    return crud.create_category(db, category_in)

@router.put("/{category_id}", response_model=schemas.CategoryOut)
def update_category(category_id: int, category_in: schemas.CategoryUpdate,
                    db: Session = Depends(get_db),
                    current_user = Depends(get_current_active_user)):
    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категорію не знайдено")
    if current_user.role not in ("admin", "editor"):
        raise HTTPException(status_code=403, detail="Недостатньо прав для редагування категорії")
    return crud.update_category(db, category, category_in)

@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db),
                    current_user = Depends(get_current_active_user)):
    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категорію не знайдено")
    if current_user.role not in ("admin", "editor"):
        raise HTTPException(status_code=403, detail="Недостатньо прав для видалення категорії")
    crud.delete_category(db, category)
    return
