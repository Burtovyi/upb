# app/roles/crud.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.roles import models, schemas

def get_roles(db: Session) -> List[models.Role]:
    return db.query(models.Role).all()

def get_role(db: Session, role_id: int) -> Optional[models.Role]:
    return db.query(models.Role).filter(models.Role.id == role_id).first()

def create_role(db: Session, role_in: schemas.RoleCreate) -> models.Role:
    role = models.Role(**role_in.dict())
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def update_role(db: Session, role: models.Role, role_in: schemas.RoleUpdate) -> models.Role:
    update_data = role_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(role, key, value)
    db.commit()
    db.refresh(role)
    return role

def delete_role(db: Session, role: models.Role) -> None:
    db.delete(role)
    db.commit()
