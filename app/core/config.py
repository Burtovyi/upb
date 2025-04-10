# app/core/config.py

from pydantic import BaseSettings, AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    # Рядок підключення до бази даних PostgreSQL
    DATABASE_URL: str = "postgresql://burtovyi:S845625s@localhost:5432/news_portal"
    
    # Секретний ключ для генерації та перевірки JWT
    SECRET_KEY: str = "my_projecrt_secret_key"
    
    # Алгоритм для шифрування JWT (наприклад, "HS256")
    ALGORITHM: str = "HS256"
    
    # Тривалість життя access-токена в хвилинах (наприклад, 60 хвилин)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Дозволені домени для CORS. Наприклад, під час розробки – "http://localhost:3000"
    ALLOWED_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]

    class Config:
        # Файл .env (розташований у корені проєкту) буде прочитаний автоматично для надсилання змінних оточення
        env_file = ".env"

# Екземпляр налаштувань, який можна імпортувати в усіх модулях
settings = Settings()
