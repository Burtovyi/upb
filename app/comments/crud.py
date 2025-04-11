# app/comments/crud.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.comments import models, schemas

def get_comment(db: Session, comment_id: int) -> Optional[models.Comment]:
    """
    Повертає коментар за його ID.
    Якщо коментар не знайдений, повертає None.
    """
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def get_comments_by_article(db: Session, article_id: int) -> List[models.Comment]:
    """
    Повертає список коментарів для статті з заданим article_id.
    Коментарі повертаються у порядку створення (від найстаршого).
    """
    return db.query(models.Comment).filter(models.Comment.article_id == article_id).order_by(models.Comment.created_at).all()

def create_comment(db: Session, article_id: int, comment_in: schemas.CommentCreate, current_user) -> models.Comment:
    """
    Створює новий коментар.
    
    Параметри:
      - db: сесія бази даних.
      - article_id: ID статті, до якої прив’язується коментар (отримується з URL).
      - comment_in: дані коментаря (контент, parent_id тощо).
      - current_user: об'єкт користувача, який створює коментар.
    
    Після додавання коментаря в БД виконується commit і повертається створений об’єкт.
    """
    new_comment = models.Comment(
        content=comment_in.content,
        article_id=article_id,
        user_id=current_user.id,
        parent_id=comment_in.parent_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def update_comment(db: Session, comment: models.Comment, comment_in: schemas.CommentUpdate, current_user) -> models.Comment:
    """
    Оновлює дані існуючого коментаря.
    
    Зазвичай тут доцільно перевірити, чи має current_user право редагувати коментар (наприклад, автор коментаря або адміністратор).
    
    Якщо в схемі CommentUpdate передано нове значення content або parent_id, відповідне поле оновлюється.
    Після commit і refresh повертається оновлений об’єкт.
    """
    if comment_in.content is not None:
        comment.content = comment_in.content
    if comment_in.parent_id is not None:
        comment.parent_id = comment_in.parent_id
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(db: Session, comment: models.Comment, current_user) -> None:
    """
    Видаляє коментар з бази даних.
    
    Перед видаленням можна перевірити права current_user (наприклад, щоб лише автор або адміністратор міг видаляти коментар).
    """
    db.delete(comment)
    db.commit()
