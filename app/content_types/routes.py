from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from app.content_types import schemas, crud
from app.db.database import get_db
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.ContentTypeOut])
def read_content_types(db: Session = Depends(get_db)):
    return crud.get_content_types(db)

@router.post("/", response_model=schemas.ContentTypeOut)
def create_content_type(
    content_type_in: schemas.ContentTypeCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.create_content_type(db, content_type_in)

@router.put("/{content_type_id}", response_model=schemas.ContentTypeOut)
def update_content_type(
    content_type_in: schemas.ContentTypeUpdate, 
    content_type_id: int = Path(..., description="ID типу контенту"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    content_type = crud.get_content_type(db, content_type_id)
    if not content_type:
        raise HTTPException(status_code=404, detail="Тип контенту не знайдено")
    return crud.update_content_type(db, content_type, content_type_in)

@router.delete("/{content_type_id}", status_code=204)
def delete_content_type(
    content_type_id: int = Path(..., description="ID типу контенту"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    content_type = crud.get_content_type(db, content_type_id)
    if not content_type:
        raise HTTPException(status_code=404, detail="Тип контенту не знайдено")
    crud.delete_content_type(db, content_type, current_user)
    return
