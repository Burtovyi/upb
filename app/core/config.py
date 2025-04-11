# app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field, AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    # Рядок підключення до бази даних PostgreSQL (повинен бути заданий у .env)
    DATABASE_URL: str = Field(..., description="PostgreSQL database connection URL")
    
    # Секретний ключ для генерації та перевірки JWT (повинен бути заданий у .env)
    SECRET_KEY: str = Field(..., description="Secret key for JWT signing")
    
    # Алгоритм для шифрування JWT (повинен бути заданий у .env)
    ALGORITHM: str = Field(..., description="JWT encryption algorithm")
    
    # Тривалість життя access-токена в хвилинах (повинен бути заданий у .env)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., description="Access token expiration time in minutes")
    
    # Дозволені домени для CORS (повинні бути задані у .env як комою розділений рядок, наприклад: http://localhost:3000,http://mydomain.com)
    ALLOWED_ORIGINS: List[str] = Field(..., description="List of allowed CORS origins")

    model_config = {
        "env_file": ".env",              # Файл оточення, звідки завантажуються налаштування
        "env_file_encoding": "utf-8",      # Кодування файлу .env
        "extra": "ignore",               # Ігнорувати додаткові змінні, яких не описано в моделі
    }

# Єдиний екземпляр налаштувань, який використовується у всіх модулях проєкту
settings = Settings()
