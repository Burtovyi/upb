from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.media import schemas, crud, models
from app.db.database import get_db
from app.auth.dependencies import get_current_active_user

router = APIRouter()

@router.get("/{media_id}", response_model=schemas.MediaOut)
def read_media(
    media_id: int = Path(..., description="ID медіа"),
    db: Session = Depends(get_db)
):
    media_item = crud.get_media(db, media_id)
    if not media_item:
        raise HTTPException(status_code=404, detail="Медіа не знайдено")
    return media_item

@router.post("/", response_model=schemas.MediaOut)
def create_media(
    media_in: schemas.MediaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    # Передаємо current_user, щоб функція створення могла встановити зв’язок із автором
    return crud.create_media(db, media_in, current_user)

@router.delete("/{media_id}", status_code=204)
def delete_media(
    media_id: int = Path(..., description="ID медіа"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    media_item = crud.get_media(db, media_id)
    if not media_item:
        raise HTTPException(status_code=404, detail="Медіа не знайдено")
    crud.delete_media(db, media_item, current_user)
    return
