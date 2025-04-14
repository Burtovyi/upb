from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field, field_validator
from typing import List

class Settings(BaseSettings):
    """
    Налаштування додатку, завантажені з .env файлу.
    Містить конфігурацію для бази даних, JWT, CORS тощо.
    """
    DATABASE_URL: str = Field(description="PostgreSQL connection URL")
    SECRET_KEY: str = Field(description="JWT secret key")
    ALGORITHM: str = Field(description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Access token expiration (minutes)")
    ALLOWED_ORIGINS: List[str] = Field(default=["http://localhost:8000"], description="List of allowed CORS origins")

    @field_validator("DATABASE_URL")
    def validate_database_url(self, v):
        if not v.startswith(("postgresql://", "sqlite://", "mysql://")):
            raise ValueError("Некоректний формат DATABASE_URL")
        return v

    @field_validator("SECRET_KEY")
    def validate_secret_key(self, v):
        if len(v) < 32:
            raise ValueError("SECRET_KEY має бути щонайменше 32 символи")
        return v

    @field_validator("ALGORITHM")
    def validate_algorithm(self, v):
        valid_algorithms = {"HS256", "HS512", "RS256"}
        if v not in valid_algorithms:
            raise ValueError(f"Алгоритм має бути одним із: {valid_algorithms}")
        return v

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()