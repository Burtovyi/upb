# app/auth/crud.py

from sqlalchemy.orm import Session
from app.auth import models, schemas
from app.auth.utils import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    """
    Повертає користувача з БД за вказаною електронною поштою.
    Якщо користувача не знайдено – повертає None.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user_in: schemas.UserCreate):
    """
    Створює нового користувача:
    - Хешує пароль із user_in.password.
    - Створює запис користувача із зазначеним email, username та хешованим паролем.
    - За потреби можна за замовчуванням встановлювати роль (якщо, наприклад, роль "reader" або "editor").
    - Після збереження запису користувача повертає створений об'єкт.
    """
    hashed_password = get_password_hash(user_in.password)
    # Створюємо нового користувача; у цьому прикладі роль не присвоюється автоматично, але її можна встановити (role_id)
    user = models.User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_password,
        is_active=True  # При створенні користувача він активний за замовчуванням
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    """
    Аутентифікує користувача:
    - Шукає користувача за email.
    - Якщо користувача не знайдено або пароль не вірний – повертає None.
    - Якщо аутентифікація успішна – повертає об'єкт користувача.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
