# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., description="PostgreSQL connection URL")
    SECRET_KEY: str = Field(..., description="JWT secret key")
    ALGORITHM: str = Field(..., description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., description="Access token expiration (minutes)")
    ALLOWED_ORIGINS: List[str] = Field(..., description="List of allowed CORS origins")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

settings = Settings()
