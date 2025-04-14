from fastapi import APIRouter, Depends, HTTPException, Path, Body
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.auth import schemas, crud, utils
from app.db.database import get_db
from app.auth.dependencies import get_current_user, get_current_active_user
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Користувач з таким email уже існує")
    return crud.create_user(db, user_in)

@router.post("/login", response_model=schemas.Token)
def login(form_data: utils.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Невірний логін або пароль")
    access_token = utils.create_access_token(data={"sub": user.email})
    refresh_token = utils.create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def read_current_user(current_user = Depends(get_current_user)):
    return current_user

@router.post("/refresh", response_model=schemas.Token)
def refresh_token(refresh_token: str = Body(..., embed=True, alias="refresh_token"), db: Session = Depends(get_db)):
    """
    Отримати новий access-токен (і refresh-токен) за дійсним refresh-токеном.
    """
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        if email is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Недійсний токен")
    except JWTError:
        raise HTTPException(status_code=401, detail="Недійсний токен")
    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=401, detail="Користувача не знайдено")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Неактивний користувач")
    access_token = utils.create_access_token(data={"sub": user.email})
    new_refresh_token = utils.create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
