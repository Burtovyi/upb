# app/roles/routes.py
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from app.roles import schemas, crud
from app.db.database import get_db
from app.auth.dependencies import get_current_user
from app.auth.models import User

router = APIRouter()

@router.get("/", response_model=List[schemas.RoleOut])
def read_roles(db: Session = Depends(get_db)):
    return crud.get_roles(db)

@router.get("/{role_id}", response_model=schemas.RoleOut)
def read_role(
    role_id: int = Path(..., description="ID ролі"),
    db: Session = Depends(get_db)
):
    role = crud.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Роль не знайдено")
    return role

@router.post("/", response_model=schemas.RoleOut)
def create_role(
    role_in: schemas.RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_role(db, role_in)

@router.put("/{role_id}", response_model=schemas.RoleOut)
def update_role(
    role_in: schemas.RoleUpdate,
    role_id: int = Path(..., description="ID ролі"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    role = crud.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Роль не знайдено")
    return crud.update_role(db, role, role_in)

@router.delete("/{role_id}", status_code=204)
def delete_role(
    role_id: int = Path(..., description="ID ролі"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    role = crud.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Роль не знайдено")
    crud.delete_role(db, role)
    return
