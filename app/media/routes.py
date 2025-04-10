# app/media/routes.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.media import schemas, crud
from app.db.database import get_db
from app.auth.dependencies import get_current_user
from app.auth.models import User

router = APIRouter()

@router.post("/upload", response_model=schemas.MediaOut)
async def upload_media(
    article_id: int = Form(..., description="ID статті, до якої прив'язати медіа"),
    file: UploadFile = File(...),
    description: str = Form(None, description="Опис/підпис для медіа"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    media_obj = await crud.upload_media(db, article_id, file, description, current_user)
    if not media_obj:
        raise HTTPException(status_code=400, detail="Помилка при завантаженні медіа")
    return media_obj

@router.delete("/{media_id}", status_code=204)
def delete_media(
    media_id: int = Path(..., description="ID медіа"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    media_obj = crud.get_media(db, media_id)
    if not media_obj:
        raise HTTPException(status_code=404, detail="Медіа не знайдено")
    crud.delete_media(db, media_obj, current_user)
    return
