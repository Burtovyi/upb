# app/social_integrations/routes.py
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from app.social_integrations import schemas, crud
from app.db.database import get_db
from app.auth.dependencies import get_current_user
from app.auth.models import User

router = APIRouter()

@router.get("/", response_model=List[schemas.SocialIntegrationOut])
def read_social_integrations(db: Session = Depends(get_db)):
    return crud.get_social_integrations(db)

@router.get("/{integration_id}", response_model=schemas.SocialIntegrationOut)
def read_social_integration(
    integration_id: int = Path(..., description="ID інтеграції"),
    db: Session = Depends(get_db)
):
    integration = crud.get_social_integration(db, integration_id)
    if not integration:
        raise HTTPException(status_code=404, detail="Інтеграцію не знайдено")
    return integration

@router.post("/", response_model=schemas.SocialIntegrationOut)
def create_social_integration(
    integration_in: schemas.SocialIntegrationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_social_integration(db, integration_in)

@router.put("/{integration_id}", response_model=schemas.SocialIntegrationOut)
def update_social_integration(
    integration_in: schemas.SocialIntegrationUpdate,
    integration_id: int = Path(..., description="ID інтеграції"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    integration = crud.get_social_integration(db, integration_id)
    if not integration:
        raise HTTPException(status_code=404, detail="Інтеграцію не знайдено")
    return crud.update_social_integration(db, integration, integration_in)

@router.delete("/{integration_id}", status_code=204)
def delete_social_integration(
    integration_id: int = Path(..., description="ID інтеграції"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    integration = crud.get_social_integration(db, integration_id)
    if not integration:
        raise HTTPException(status_code=404, detail="Інтеграцію не знайдено")
    crud.delete_social_integration(db, integration)
    return
