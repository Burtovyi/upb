# app/auth/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings  # Має містити SECRET_KEY, ALGORITHM (наприклад, 'HS256') тощо
from app.db.database import get_db
from app.auth import crud  # Функції доступу до користувачів, наприклад, get_user_by_email

# Створюємо схему OAuth2, вказуючи URL для отримання токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Декодує JWT-токен, витягує email користувача з його payload, 
    завантажує користувача з бази даних і повертає об'єкт користувача.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не вдалося пройти автентифікацію",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise credentials_exception
    return user

def get_current_active_user(current_user = Depends(get_current_user)):
    """
    Перевіряє, що користувач активний. Якщо ні – повертає HTTPException.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Неактивний користувач")
    return current_user
