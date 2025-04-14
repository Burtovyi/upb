from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import Optional
from app.auth import schemas, utils
from app.authors import models  # модуль з Author

def get_user_by_email(db: Session, email: str) -> Optional[models.Author]:
    """
    Знайти користувача (Author) за email.
    
    Args:
        db: Сесія бази даних.
        email: Email користувача.
    
    Returns:
        Optional[models.Author]: Користувач або None, якщо не знайдено.
    
    Raises:
        HTTPException: Якщо сталася помилка бази даних.
    """
    try:
        return db.query(models.Author).filter(models.Author.email == email).first()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при пошуку користувача")

def get_user_by_id(db: Session, user_id: int) -> Optional[models.Author]:
    """
    Знайти користувача (Author) за ID.
    
    Args:
        db: Сесія бази даних.
        user_id: ID користувача.
    
    Returns:
        Optional[models.Author]: Користувач або None, якщо не знайдено.
    
    Raises:
        HTTPException: Якщо сталася помилка бази даних.
    """
    try:
        return db.query(models.Author).filter(models.Author.id == user_id).first()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при пошуку користувача")

def create_user(db: Session, user_in: schemas.UserCreate) -> models.Author:
    """
    Створити нового користувача (Author) з роллю 'user' за замовчуванням.
    
    Args:
        db: Сесія бази даних.
        user_in: Дані для створення користувача (email, ім’я, пароль, біографія).
    
    Returns:
        models.Author: Створений користувач.
    
    Raises:
        HTTPException: Якщо ім’я чи email уже існують або сталася помилка бази даних.
    """
    try:
        if db.query(models.Author).filter(models.Author.name == user_in.name).first():
            raise HTTPException(status_code=400, detail="Користувач з таким ім'ям уже існує")
        hashed_password = utils.get_password_hash(user_in.password)
        author = models.Author(
            email=user_in.email,
            name=user_in.name,
            bio=user_in.bio,
            hashed_password=hashed_password,
            is_active=True,
            role="user"
        )
        db.add(author)
        db.commit()
        author.created_by = author.id  # Встановлюємо created_by як власний id
        db.commit()
        db.refresh(author)
        return author
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Помилка бази даних при створенні користувача")

def authenticate_user(db: Session, email: str, password: str) -> Optional[models.Author]:
    """
    Аутентифікувати користувача за email і паролем.
    
    Args:
        db: Сесія бази даних.
        email: Email користувача.
        password: Пароль користувача.
    
    Returns:
        Optional[models.Author]: Користувач, якщо аутентифікація успішна, інакше None.
    
    Raises:
        HTTPException: Якщо сталася помилка бази даних.
    """
    try:
        author = get_user_by_email(db, email)
        if not author or not author.is_active:
            return None
        if not utils.verify_password(password, author.hashed_password):
            return None
        return author
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при аутентифікації")