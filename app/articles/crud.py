from sqlalchemy.orm import Session
from typing import List, Optional
from app.articles import models, schemas

def get_articles(db: Session, skip: int = 0, limit: int = 100) -> List[models.Article]:
    return db.query(models.Article).offset(skip).limit(limit).all()

def get_article(db: Session, article_id: int) -> Optional[models.Article]:
    return db.query(models.Article).filter(models.Article.id == article_id).first()

def create_article(db: Session, article_in: schemas.ArticleCreate) -> models.Article:
    new_article = models.Article(
        title=article_in.title,
        description=article_in.description,
        content=article_in.content,
        view_count=article_in.view_count,
        author_id=article_in.author_id,
        category_id=article_in.category_id
    )
    if article_in.tag_ids:
        from app.tags.models import Tag
        tags = db.query(Tag).filter(Tag.id.in_(article_in.tag_ids)).all()
        new_article.tags = tags
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

def update_article(db: Session, article: models.Article, article_in: schemas.ArticleUpdate) -> models.Article:
    update_data = article_in.dict(exclude_unset=True, exclude={"tag_ids"})
    for key, value in update_data.items():
        setattr(article, key, value)
    if "tag_ids" in article_in.dict():
        if article_in.tag_ids is not None:
            from app.tags.models import Tag
            tags = db.query(Tag).filter(Tag.id.in_(article_in.tag_ids)).all()
            article.tags = tags
    db.commit()
    db.refresh(article)
    return article

def delete_article(db: Session, article: models.Article) -> None:
    db.delete(article)
    db.commit()
