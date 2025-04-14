from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from typing import TypedDict

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Перевіряє, чи збігається звичайний пароль із хешованим.
    
    Args:
        plain_password: Пароль у відкритому вигляді.
        hashed_password: Хешований пароль із бази даних.
    
    Returns:
        bool: True, якщо паролі збігаються, інакше False.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Створює хеш пароля за допомогою bcrypt.
    
    Args:
        password: Пароль у відкритому вигляді.
    
    Returns:
        str: Хешований пароль.
    
    Raises:
        ValueError: Якщо пароль занадто довгий для bcrypt.
    """
    if len(password.encode()) > 72:
        raise ValueError("Пароль занадто довгий для bcrypt (максимум 72 байти)")
    return pwd_context.hash(password)

class TokenData(TypedDict):
    sub: str

def create_access_token(data: TokenData, expires_delta: timedelta = None) -> str:
    """
    Генерує JWT access-токен.
    
    Args:
        data: Дані для кодування в токені (наприклад, {'sub': user_id}).
        expires_delta: Час життя токена. Якщо None, використовується ACCESS_TOKEN_EXPIRE_MINUTES.
    
    Returns:
        str: Закодований JWT-токен.
    
    Raises:
        ValueError: Якщо дані або конфігурація некоректні.
        JWTError: Якщо сталася помилка кодування токена.
    """
    if not settings.SECRET_KEY or not settings.ALGORITHM:
        raise ValueError("SECRET_KEY або ALGORITHM не налаштовані")
    if "sub" not in data:
        raise ValueError("Поле 'sub' обов’язкове для JWT-токена")
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    
    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    except JWTError:
        raise ValueError("Помилка кодування JWT-токена")

def create_refresh_token(data: TokenData) -> str:
    """
    Генерує JWT refresh-токен з тривалістю, визначеною в налаштуваннях.
    
    Args:
        data: Дані для кодування в токені (наприклад, {'sub': user_id}).
    
    Returns:
        str: Закодований JWT-токен.
    
    Raises:
        ValueError: Якщо дані або конфігурація некоректні.
        JWTError: Якщо сталася помилка кодування токена.
    """
    if not settings.SECRET_KEY or not settings.ALGORITHM:
        raise ValueError("SECRET_KEY або ALGORITHM не налаштовані")
    if "sub" not in data:
        raise ValueError("Поле 'sub' обов’язкове для JWT-токена")
    
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    
    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    except JWTError:
        raise ValueError("Помилка кодування JWT-токена")

__all__ = [
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "create_refresh_token",
    "OAuth2PasswordRequestForm",
]