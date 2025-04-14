from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.exc import OperationalError
from app.core.config import settings

try:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,  # Увімкнено лише в режимі розробки
        pool_size=5,
        max_overflow=10,
        pool_timeout=30
    )
    # Тестове підключення
    with engine.connect() as connection:
        connection.execute("SELECT 1")
except OperationalError as e:
    raise Exception(f"Не вдалося підключитися до бази даних: {e}")

SessionLocal = sessionmaker(bind=engine, autoflush=False)

def get_db():
    """
    Створює нову сесію SQLAlchemy для кожного запиту та закриває її після завершення.
    Використовується як залежність у FastAPI ендпоінтах.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

class Base(DeclarativeBase):
    metadata = MetaData()