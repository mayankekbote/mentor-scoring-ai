"""
config.py
---------
Centralised settings loaded from environment variables / .env file.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:admin@localhost:5432/interview_db"

    # JWT / Auth
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # File storage
    UPLOAD_DIR: str = "storage/uploads"

    # AI Engine (no imports — called as subprocess / imported at runtime)
    AI_ENGINE_ENABLED: bool = True

    # Email / SMTP
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: str = "no-reply@mentorai.com"
    EMAILS_FROM_NAME: str = "MentorAI"
    EMAILS_ENABLED: bool = False
    FRONTEND_HOST: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
