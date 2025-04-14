import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Додаємо кореневу директорію до sys.path для правильного імпорту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Отримуємо конфігураційний об'єкт Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Імпортуємо налаштування БД та базовий клас моделей
from app.core.config import settings
from app.db.database import Base

# Імпортуємо всі модулі з моделями, щоб Alembic бачив їх метадані
# (Авторизація вже в моделях Author)
import app.articles.models
import app.categories.models
import app.tags.models
import app.authors.models
import app.comments.models
import app.media.models
import app.content_types.models

# Метадані всіх моделей
target_metadata = Base.metadata
# Оновлюємо URL підключення з конфігурації
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
# ... (далі налаштування offline/online режимів міграцій) ...
