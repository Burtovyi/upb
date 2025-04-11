# app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os

class Settings(BaseSettings):
    # Рядок підключення до бази даних PostgreSQL
    # Використовуємо Field для безпечного значення за замовчуванням
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/news_portal",
        description="PostgreSQL database connection URL"
    )
    
    # Секретний ключ для JWT
    # Рекомендується зберігати в змінній оточення
    SECRET_KEY: str = Field(
        default_factory=lambda: os.urandom(32).hex(),
        description="Secret key for JWT signing"
    )
    
    # Алгоритм для шифрування JWT
    ALGORITHM: str = Field(
        default="HS256",
        description="JWT encryption algorithm"
    )
    
    # Тривалість життя access-токена в хвилинах
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60,
        ge=1,
        description="Access token expiration time in minutes"
    )
    
    # Дозволені домени для CORS
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000"],
        description="List of allowed CORS origins"
    )

    model_config = {
        # Налаштування для завантаження з .env файлу
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        # Ігноруємо невизначені змінні
        "extra": "ignore"
    }

# Єдиний екземпляр налаштувань
settings = Settings()