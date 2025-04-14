from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.auth.routes import router as auth_router
from app.articles.routes import router as articles_router
from app.categories.routes import router as categories_router
from app.tags.routes import router as tags_router
from app.comments.routes import router as comments_router
from app.content_types.routes import router as content_types_router
from app.media.routes import router as media_router
from app.core.config import settings  # Має містити налаштування (SECRET_KEY, DATABASE_URL тощо)

app = FastAPI(
    title="UPB API",
    description="Бекенд для новинного ресурсу",
    version="1.0.0"
)

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

# Налаштування CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # Додайте інші дозволені домени за потреби
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення роутерів
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(articles_router, prefix="/api/v1/articles", tags=["articles"])
app.include_router(categories_router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(tags_router, prefix="/api/v1/tags", tags=["tags"])
app.include_router(comments_router, prefix="/api/v1/comments", tags=["comments"])
app.include_router(content_types_router, prefix="/api/v1/content-types", tags=["content_types"])
app.include_router(media_router, prefix="/api/v1/media", tags=["media"])

# Middleware для логування запитів та відповідей
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Запит: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Відповідь: {response.status_code}")
    return response

@app.get("/")
def root():
    return {"message": "UPB API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
