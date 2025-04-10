from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Імпорт конфігурації з файлу налаштувань (core/config.py має містити змінну ALLOWED_ORIGINS та інші параметри)
from app.core.config import settings

# Імпортуємо маршрути з окремих модулів
from app.auth.routes import router as auth_router
from app.articles.routes import router as articles_router
from app.categories.routes import router as categories_router
from app.tags.routes import router as tags_router
from app.authors.routes import router as authors_router
from app.comments.routes import router as comments_router
from app.media.routes import router as media_router
from app.content_types.routes import router as content_types_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(articles_router, prefix="/articles", tags=["articles"])

api.router.include_router(
    api_router,
    prefix="/api",
    tags=["api"]
)
from app.api.auth import auth_router
from app.api.articles import articles_router
from app.api.users import users_router


@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/health")
async def health():
    return {"status": "healthy"}
