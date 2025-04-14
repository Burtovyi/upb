from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.db.database import get_db
from app.auth import crud
from app.authors.models import Author

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Author:
    """
    Отримати поточного користувача за JWT-токеном.
    
    Args:
        token: JWT-токен із заголовка Authorization.
        db: Сесія бази даних.
    
    Returns:
        Author: Аутентифікований користувач.
    
    Raises:
        HTTPException: Якщо токен недійсний, користувача не знайдено або сталася помилка бази даних.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не вдалося пройти автентифікацію",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    try:
        user = crud.get_user_by_id(db, user_id=int(user_id))
        if not user:
            raise credentials_exception
        return user
    except (ValueError, SQLAlchemyError):
        raise credentials_exception

def get_current_active_user(current_user: Author = Depends(get_current_user)) -> Author:
    """
    Отримати поточного активного користувача.
    
    Args:
        current_user: Аутентифікований користувач.
    
    Returns:
        Author: Активний користувач.
    
    Raises:
        HTTPException: Якщо користувач неактивний.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Неактивний користувач")
    return current_user