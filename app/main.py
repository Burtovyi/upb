from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

# Імпорт налаштувань (наприклад, з файлу app/core/config.py)
from app.core.config import settings

# Імпорт маршрутів (routers)
from app.auth.routes import router as auth_router
from app.articles.routes import router as articles_router
from app.categories.routes import router as categories_router
from app.tags.routes import router as tags_router
from app.authors.routes import router as authors_router
from app.comments.routes import router as comments_router
from app.media.routes import router as media_router
from app.content_types.routes import router as content_types_router

# Ініціалізація FastAPI застосунку з основними метаданими
app = FastAPI(
    title="Новинний сайт API",
    description="API для управління новинами, користувачами, контентом, коментарями та мультимедіа",
    version="1.0.0"
)

# Налаштування CORS – використовуємо значення з settings.ALLOWED_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Створюємо загальний роутер з префіксом "/api/v1" та включаємо до нього підмаршрути
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(articles_router, prefix="/articles", tags=["Articles"])
api_router.include_router(categories_router, prefix="/categories", tags=["Categories"])
api_router.include_router(tags_router, prefix="/tags", tags=["Tags"])
api_router.include_router(authors_router, prefix="/authors", tags=["Authors"])
api_router.include_router(comments_router, prefix="/comments", tags=["Comments"])
api_router.include_router(media_router, prefix="/media", tags=["Media"])
api_router.include_router(content_types_router, prefix="/content-types", tags=["ContentTypes"])

# Підключаємо загальний API роутер до застосунку
app.include_router(api_router)

# Кореневий endpoint
@app.get("/")
async def root():
    return {"message": "Вітаємо на API новинного сайту!"}

# Endpoint для моніторингу стану API
@app.get("/health")
async def health():
    return {"status": "healthy"}

# Запуск застосунку (для локального запуску через Uvicorn)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
