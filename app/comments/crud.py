from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.comments import models, schemas

def get_comments_by_article(db: Session, article_id: int):
    """Повертає всі коментарі для статті за її ID."""
    return db.query(models.Comment).filter(models.Comment.article_id == article_id).all()

def create_comment(db: Session, comment_in: schemas.CommentCreate, current_user):
    """Створює новий коментар для статті від поточного користувача."""
    new_comment = models.Comment(
        content=comment_in.content,
        parent_id=comment_in.parent_id,
        article_id=comment_in.article_id,
        author_id=current_user.id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_comment(db: Session, comment_id: int):
    """Повертає коментар за заданим ID."""
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def update_comment(db: Session, comment: models.Comment, comment_in: schemas.CommentUpdate, current_user):
    """
    Оновлює коментар.
    Лише автор або користувач з роллю admin/editor має право редагувати.
    """
    if current_user.role not in ("admin", "editor") and comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостатньо прав для редагування коментаря")
    if comment_in.content is not None:
        comment.content = comment_in.content
    if comment_in.parent_id is not None:
        comment.parent_id = comment_in.parent_id
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(db: Session, comment: models.Comment, current_user) -> None:
    """
    Видаляє коментар.
    Лише автор або користувач з роллю admin/editor має право видаляти.
    """
    if current_user.role not in ("admin", "editor") and comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостатньо прав для видалення коментаря")
    db.delete(comment)
    db.commit()
