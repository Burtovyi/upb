# app/core/config.py

from pydantic.v1 import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Рядок підключення до бази даних PostgreSQL
    DATABASE_URL: str = "postgresql://burtovyi:S845625s@localhost:5432/news_portal"
    
    # Секретний ключ для генерації та перевірки JWT
    SECRET_KEY: str = "my_project_secret_key"
    
    # Алгоритм для шифрування JWT (наприклад, "HS256")
    ALGORITHM: str = "HS256"
    
    # Тривалість життя access-токена в хвилинах
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Дозволені домени для CORS. Використовуємо список рядків, що дозволяє вказувати як конкретні URL, так і ' * '
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        # Файл .env (розташований у корені проєкту) буде завантажений автоматично,
        # що дозволить переписати значення за замовчуванням із змінних оточення.
        env_file = ".env"

# Єдиний екземпляр налаштувань, який можна імпортувати в усіх модулях
settings = Settings()
