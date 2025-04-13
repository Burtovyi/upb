# alembic/env.py

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Додаємо кореневу директорію проєкту до шляху, щоб імпорт працював коректно
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Отримуємо конфігураційний об'єкт Alembic
config = context.config

# Налаштовуємо логування на основі файлу конфігурації Alembic (alembic.ini)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Імпортуємо налаштування нашого проєкту з app/core/config.py
from app.core.config import settings

# Імпортуємо базовий клас для моделей із app/db/database.py
from app.db.database import Base

# Імпортуємо всі модулі з моделями, щоб їх метадані були враховані Alembic
import app.auth.models
import app.articles.models
import app.categories.models
import app.tags.models
import app.authors.models
import app.comments.models
import app.media.models
import app.content_types.models

# Встановлюємо target_metadata – це метадані всіх моделей
target_metadata = Base.metadata

print("DATABASE_URL:", settings.DATABASE_URL)

# Оновлюємо значення URL підключення з налаштувань (DATABASE_URL)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """
    Запуск міграцій у режимі offline: конфігурація контексту лише з URL.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Запуск міграцій у режимі online: створюється Engine, встановлюється з'єднання,
    а потім запускаються міграції.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Дозволяє автоматично виявляти зміни типів колонок
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
