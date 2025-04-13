# app/social_integrations/crud.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.social_integrations import models, schemas

def get_social_integrations(db: Session) -> List[models.SocialIntegration]:
    return db.query(models.SocialIntegration).all()

def get_social_integration(db: Session, integration_id: int) -> Optional[models.SocialIntegration]:
    return db.query(models.SocialIntegration).filter(models.SocialIntegration.id == integration_id).first()

def create_social_integration(
    db: Session, integration_in: schemas.SocialIntegrationCreate
) -> models.SocialIntegration:
    integration = models.SocialIntegration(**integration_in.dict())
    db.add(integration)
    db.commit()
    db.refresh(integration)
    return integration

def update_social_integration(
    db: Session, integration: models.SocialIntegration, integration_in: schemas.SocialIntegrationUpdate
) -> models.SocialIntegration:
    update_data = integration_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(integration, key, value)
    db.commit()
    db.refresh(integration)
    return integration

def delete_social_integration(db: Session, integration: models.SocialIntegration) -> None:
    db.delete(integration)
    db.commit()
