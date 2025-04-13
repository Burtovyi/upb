# app/logs/routes.py
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from app.logs import schemas, crud
from app.db.database import get_db
from app.auth.dependencies import get_current_user
from app.auth.models import User

router = APIRouter()

@router.get("/", response_model=List[schemas.LogOut])
def read_logs(db: Session = Depends(get_db)):
    return crud.get_logs(db)

@router.get("/{log_id}", response_model=schemas.LogOut)
def read_log(
    log_id: int = Path(..., description="ID запису логу"),
    db: Session = Depends(get_db)
):
    log_entry = crud.get_log(db, log_id)
    if not log_entry:
        raise HTTPException(status_code=404, detail="Лог не знайдено")
    return log_entry

@router.post("/", response_model=schemas.LogOut)
def create_log(
    log_in: schemas.LogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_log(db, log_in)

@router.delete("/{log_id}", status_code=204)
def delete_log(
    log_id: int = Path(..., description="ID запису логу"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log_entry = crud.get_log(db, log_id)
    if not log_entry:
        raise HTTPException(status_code=404, detail="Лог не знайдено")
    crud.delete_log(db, log_entry)
    return
