# app/authors/crud.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.authors import models, schemas

def get_authors(db: Session) -> List[models.Author]:
    """
    Повертає список усіх авторів.
    """
    return db.query(models.Author).all()

def get_author(db: Session, author_id: int) -> Optional[models.Author]:
    """
    Повертає автора за його ID.
    Якщо автор не знайдений, повертає None.
    """
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def create_author(db: Session, author_in: schemas.AuthorCreate) -> models.Author:
    """
    Створює нового автора та додає його до бази даних.
    
    :param db: Сесія бази даних.
    :param author_in: Pydantic-схема для створення автора.
    :return: Створений об'єкт моделі Author.
    """
    new_author = models.Author(
        name=author_in.name,
        bio=author_in.bio
        # Якщо потрібно, можна додати додаткові поля
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

def update_author(db: Session, author: models.Author, author_in: schemas.AuthorUpdate) -> models.Author:
    """
    Оновлює дані автора на основі переданих даних із схеми AuthorUpdate.
    
    :param db: Сесія бази даних.
    :param author: Існуючий об'єкт автора.
    :param author_in: Pydantic-схема для оновлення автора.
    :return: Оновлений об'єкт моделі Author.
    """
    if author_in.name is not None:
        author.name = author_in.name
    if author_in.bio is not None:
        author.bio = author_in.bio
    db.commit()
    db.refresh(author)
    return author

def delete_author(db: Session, author: models.Author) -> None:
    """
    Видаляє автора з бази даних.
    
    :param db: Сесія бази даних.
    :param author: Об'єкт автора, який слід видалити.
    """
    db.delete(author)
    db.commit()
