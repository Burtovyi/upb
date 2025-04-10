# app/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings  # Має містити налаштування, зокрема DATABASE_URL

# Отримуємо URL підключення до БД із налаштувань (наприклад, "postgresql://username:password@localhost:5432/dbname")
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Створюємо engine. Параметр pool_pre_ping=True дозволяє автоматично перевіряти стан з'єднання,
# а echo=True – виводити SQL-запити для дебагу (вимикайте в продакшн).
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True,
    echo=True
)

# SessionLocal – фабрика сесій, яка використовується для взаємодії з БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для всіх моделей (ORM). Всі SQLAlchemy моделі повинні успадковувати цей клас.
Base = declarative_base()


# Залежність для FastAPI: забезпечує відкриття сесії для кожного запиту і її закриття після роботи.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
