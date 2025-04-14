from sqlalchemy.orm import Session
from app.auth import schemas, utils
from app.authors import models  # модуль з Author

def get_user_by_email(db: Session, email: str):
    """Знайти користувача (Author) за email"""
    return db.query(models.Author).filter(models.Author.email == email).first()

def create_user(db: Session, user_in: schemas.UserCreate):
    """Створити нового користувача (Author) з роллю 'user' за замовчуванням"""
    hashed_password = utils.get_password_hash(user_in.password)
    author = models.Author(
        email=user_in.email,
        name=user_in.name,
        hashed_password=hashed_password,
        is_active=True,
        role="user"
    )
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

def authenticate_user(db: Session, email: str, password: str):
    author = get_user_by_email(db, email)
    if not author:
        return None
    if not utils.verify_password(password, author.hashed_password):
        return None
    return author
