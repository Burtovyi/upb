from sqlalchemy.orm import Session
from typing import List, Optional
from app.authors import models, schemas

def get_authors(db: Session) -> List[models.Author]:
    """Повертає список всіх авторів."""
    return db.query(models.Author).all()

def get_author(db: Session, author_id: int) -> Optional[models.Author]:
    """Повертає автора за ID або None, якщо не знайдено."""
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def create_author(db: Session, author_in: schemas.AuthorCreate) -> models.Author:
    """Створює нового автора та додає його до бази даних."""
    new_author = models.Author(**author_in.dict())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

def update_author(db: Session, author: models.Author, author_in: schemas.AuthorUpdate) -> models.Author:
    """Оновлює дані автора з використанням даних із AuthorUpdate."""
    update_data = author_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(author, key, value)
    db.commit()
    db.refresh(author)
    return author

def delete_author(db: Session, author: models.Author) -> None:
    """Видаляє автора з бази даних."""
    db.delete(author)
    db.commit()
