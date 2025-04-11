# app/auth/utils.py

from datetime import datetime, timedelta
from jose import jwt  # Переконайтеся, що встановлено python-jose
from app.core.config import settings  # Імпорт налаштувань (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)

# Існуючі функції для роботи з паролями:
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Додаємо функцію для створення JWT токена
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Генерує JWT-токен.
    
    :param data: Дані, які потрібно закодувати в токені (наприклад, {"sub": user.email})
    :param expires_delta: (Опціонально) тривалість токена у вигляді timedelta;
           якщо не задано, використовується значення, задане в settings.ACCESS_TOKEN_EXPIRE_MINUTES.
    :return: Згенерований JWT-токен як рядок.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # Додаємо до payload час закінчення дії токена
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
