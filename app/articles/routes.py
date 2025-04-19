from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.articles import schemas, crud
from app.db.database import get_db
from app.auth.dependencies import get_current_active_user
from app.authors.models import Author

router = APIRouter()

@router.get("/", response_model=list[schemas.ArticleOut])
def read_articles(
    skip: int = Query(0, ge=0, description="Кількість пропущених записів"),
    limit: int = Query(100, ge=1, le=100, description="Максимальна кількість записів"),
    db: Session = Depends(get_db)
):
    """
    Отримати список статей.
    
    Args:
        skip: Кількість пропущених записів.
        limit: Максимальна кількість записів для повернення.
        db: Сесія бази даних.
    
    Returns:
        list[schemas.ArticleOut]: Список статей.
    
    Raises:
        HTTPException: Якщо сталася помилка бази даних.
    """
    try:
        return crud.get_articles(db, skip=skip, limit=limit)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при отриманні статей")

@router.get("/{article_id}", response_model=schemas.ArticleOut)
def read_article(
    article_id: int = Path(..., ge=1, description="ID статті"),
    db: Session = Depends(get_db)
):
    """
    Отримати статтю за ID.
    
    Args:
        article_id: ID статті.
        db: Сесія бази даних.
    
    Returns:
        schemas.ArticleOut: Стаття.
    
    Raises:
        HTTPException: Якщо статтю не знайдено або сталася помилка бази даних.
    """
    try:
        article = crud.get_article(db, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Статтю не знайдено")
        article.view_count += 1
        db.commit()
        return article
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при отриманні статті")

@router.post("/", response_model=schemas.ArticleOut)
def create_article(
    article_in: schemas.ArticleCreate,
    db: Session = Depends(get_db),
    current_user: Author = Depends(get_current_active_user)
):
    """
    Створити нову статтю.
    
    Args:
        article_in: Дані для створення статті.
        db: Сесія бази даних.
        current_user: Аутентифікований користувач.
    
    Returns:
        schemas.ArticleOut: Створена стаття.
    
    Raises:
        HTTPException: Якщо автор не знайдений або сталася помилка бази даних.
    """
    try:
        author_id = article_in.author_id
        if current_user.role == "user":
            author_id = current_user.id
        else:
            # Перевіряємо, чи існує автор для admin/editor
            author = db.query(Author).filter(Author.id == author_id).first()
            if not author:
                raise HTTPException(status_code=400, detail="Автор не знайдений")
        return crud.create_article(db, article_in.copy(update={"author_id": author_id}))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при створенні статті")

@router.put("/{article_id}", response_model=schemas.ArticleOut)
def update_article(
    article_in: schemas.ArticleUpdate,
    article_id: int = Path(..., ge=1, description="ID статті"),
    db: Session = Depends(get_db),
    current_user: Author = Depends(get_current_active_user)
):
    """
    Оновити статтю.
    
    Args:
        article_in: Дані для оновлення статті.
        article_id: ID статті.
        db: Сесія бази даних.
        current_user: Аутентифікований користувач.
    
    Returns:
        schemas.ArticleOut: Оновлена стаття.
    
    Raises:
        HTTPException: Якщо статтю не знайдено, недостатньо прав або сталася помилка бази даних.
    """
    try:
        article = crud.get_article(db, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Статтю не знайдено")
        if current_user.role not in ("admin", "editor") and article.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Недостатньо прав для оновлення статті")
        return crud.update_article(db, article, article_in)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при оновленні статті")

@router.delete("/{article_id}", status_code=204)
def delete_article(
    article_id: int = Path(..., ge=1, description="ID статті"),
    db: Session = Depends(get_db),
    current_user: Author = Depends(get_current_active_user)
):
    """
    Видалити статтю.
    
    Args:
        article_id: ID статті.
        db: Сесія бази даних.
        current_user: Аутентифікований користувач.
    
    Returns:
        None: Статус 204 (No Content).
    
    Raises:
        HTTPException: Якщо статтю не знайдено, недостатньо прав або сталася помилка бази даних.
    """
    try:
        article = crud.get_article(db, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Статтю не знайдено")
        if current_user.role not in ("admin", "editor") and article.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Недостатньо прав для видалення статті")
        crud.delete_article(db, article)
        return None
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка бази даних при видаленні статті")