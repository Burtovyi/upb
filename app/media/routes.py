from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.media import schemas, crud, models
from app.db.database import get_db
from app.auth.dependencies import get_current_active_user
from typing import Any

router = APIRouter()

@router.get("/{media_id}", response_model=schemas.MediaOut, summary="Отримати медіа за ID")
def read_media(
    media_id: int = Path(..., description="ID медіа", ge=1),
    db: Session = Depends(get_db)
):
    """Отримати деталі медіа за його ID."""
    media_item = crud.get_media(db, media_id)
    if not media_item:
        raise HTTPException(status_code=404, detail="Медіа не знайдено")
    return media_item

@router.post("/", response_model=schemas.MediaOut, summary="Створити медіа")
def create_media(
    media_in: schemas.MediaCreate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user)
):
    """Створити новий медіа-об'єкт."""
    return crud.create_media(db, media_in, current_user)

@router.delete("/{media_id}", status_code=204, summary="Видалити медіа")
def delete_media(
    media_id: int = Path(..., description="ID медіа", ge=1),
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user)
):
    """Видалити медіа за його ID."""
    media_item = crud.get_media(db, media_id)
    if not media_item:
        raise HTTPException(status_code=404, detail="Медіа не знайдено")
    if media_item.created_by != current_user.id and current_user.role not in ("admin",):
        raise HTTPException(status_code=403, detail="Недостатньо прав для видалення медіа")
    crud.delete_media(db, media_item, current_user)
    return None