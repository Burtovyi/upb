from fastapi import APIRouter, Depends, HTTPException, Path, Body
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.auth import schemas, crud, utils
from app.db.database import get_db
from app.auth.dependencies import get_current_user, get_current_active_user
from app.core.config import settings
from app.authors.models import Author

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Реєстрація нового користувача.
    
    Args:
        user_in: Дані користувача (email, ім’я, пароль, біографія).
        db: Сесія бази даних.
    
    Returns:
        schemas.UserOut: Створений користувач.
    
    Raises:
        HTTPException: Якщо email уже існує або сталася помилка бази даних.
    """
    try:
        existing_user = crud.get_user_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Користувач з таким email уже існує")
        return crud.create_user(db, user_in)  # created_by встановлюється в crud
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при реєстрації")

@router.post("/login", response_model=schemas.Token)
def login(form_data: utils.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Аутентифікація користувача за email і паролем.
    
    Args:
        form_data: Дані форми (username=email, password).
        db: Сесія бази даних.
    
    Returns:
        schemas.Token: Access- і refresh-токени.
    
    Raises:
        HTTPException: Якщо логін/пароль невірні або сталася помилка бази даних.
    """
    try:
        user: Author = crud.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=401, detail="Невірний логін або пароль")
        access_token = utils.create_access_token(data={"sub": str(user.id)})
        refresh_token = utils.create_refresh_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при аутентифікації")

@router.get("/me", response_model=schemas.UserOut)
def read_current_user(current_user: schemas.UserOut = Depends(get_current_user)):
    """
    Отримати дані поточного користувача.
    
    Args:
        current_user: Аутентифікований користувач.
    
    Returns:
        schemas.UserOut: Дані користувача.
    """
    return current_user

@router.post("/refresh", response_model=schemas.Token)
def refresh_token(refresh_token: str = Body(..., embed=True, alias="refresh_token"), db: Session = Depends(get_db)):
    """
    Отримати новий access-токен (і refresh-токен) за дійсним refresh-токеном.
    
    Args:
        refresh_token: Refresh-токен.
        db: Сесія бази даних.
    
    Returns:
        schemas.Token: Нові access- і refresh-токени.
    
    Raises:
        HTTPException: Якщо токен недійсний, користувач неактивний або сталася помилка.
    """
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Недійсний токен")
        user: Author = crud.get_user_by_id(db, user_id=int(user_id))
        if not user:
            raise HTTPException(status_code=401, detail="Користувача не знайдено")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Неактивний користувач")
        access_token = utils.create_access_token(data={"sub": str(user.id)})
        new_refresh_token = utils.create_refresh_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Недійсний токен")
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при оновленні токена")