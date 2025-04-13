# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.auth.routes import router as auth_router
from app.articles.routes import router as articles_router
from app.authors.routes import router as authors_router
from app.categories.routes import router as categories_router
from app.tags.routes import router as tags_router
from app.comments.routes import router as comments_router
from app.content_types.routes import router as content_types_router
from app.media.routes import router as media_router
from app.article_history.routes_history import router as article_history_router
from app.logs.routes import router as logs_router
from app.metrics.routes import router as metrics_router
from app.social_integrations.routes import router as social_integrations_router
from app.roles.routes import router as roles_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(articles_router, prefix="/api/v1/articles", tags=["articles"])
app.include_router(authors_router, prefix="/api/v1/authors", tags=["authors"])
app.include_router(categories_router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(tags_router, prefix="/api/v1/tags", tags=["tags"])
app.include_router(comments_router, prefix="/api/v1/comments", tags=["comments"])
app.include_router(content_types_router, prefix="/api/v1/content-types", tags=["content_types"])
app.include_router(media_router, prefix="/api/v1/media", tags=["media"])
app.include_router(article_history_router, prefix="/api/v1/article-history", tags=["article_history"])
app.include_router(logs_router, prefix="/api/v1/logs", tags=["logs"])
app.include_router(metrics_router, prefix="/api/v1/metrics", tags=["metrics"])
app.include_router(social_integrations_router, prefix="/api/v1/social-integrations", tags=["social_integrations"])
app.include_router(roles_router, prefix="/api/v1/roles", tags=["roles"])

@app.get("/")
def root():
    return {"message": "Hello, world!"}
