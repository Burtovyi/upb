from fastapi import FastAPI
# ... імпорт інших роутерів ...
from app.auth.routes import router as auth_router
from app.articles.routes import router as articles_router
from app.categories.routes import router as categories_router
from app.tags.routes import router as tags_router
from app.comments.routes import router as comments_router
from app.content_types.routes import router as content_types_router
from app.media.routes import router as media_router

app = FastAPI()

# Підключення необхідних роутерів:
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(articles_router, prefix="/api/v1/articles", tags=["articles"])
app.include_router(categories_router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(tags_router, prefix="/api/v1/tags", tags=["tags"])
app.include_router(comments_router, prefix="/api/v1/comments", tags=["comments"])
app.include_router(content_types_router, prefix="/api/v1/content-types", tags=["content_types"])
app.include_router(media_router, prefix="/api/v1/media", tags=["media"])

@app.get("/")
def root():
    return {"message": "UPB API"}
