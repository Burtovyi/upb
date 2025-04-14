from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.tags import schemas, crud, models
from app.db.database import get_db
from app.auth.dependencies import get_current_active_user

router = APIRouter()

@router.get("/", response_model=list[schemas.TagOut])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tags(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.TagOut)
def create_tag(
    tag_in: schemas.TagCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    if current_user.role not in ("admin", "editor"):
        raise HTTPException(status_code=403, detail="Недостатньо прав для створення тегу")
    return crud.create_tag(db, tag_in)

@router.put("/{tag_id}", response_model=schemas.TagOut)
def update_tag(
    tag_id: int = Path(..., description="ID тегу"),
    tag_in: schemas.TagUpdate = ...,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    tag = crud.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Тег не знайдено")
    if current_user.role not in ("admin", "editor"):
        raise HTTPException(status_code=403, detail="Недостатньо прав для редагування тегу")
    return crud.update_tag(db, tag, tag_in)

@router.delete("/{tag_id}", status_code=204)
def delete_tag(
    tag_id: int = Path(..., description="ID тегу"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    tag = crud.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Тег не знайдено")
    if current_user.role not in ("admin", "editor"):
        raise HTTPException(status_code=403, detail="Недостатньо прав для видалення тегу")
    crud.delete_tag(db, tag)
    return
