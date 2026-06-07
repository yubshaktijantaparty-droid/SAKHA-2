"""Configuration for SAKHA AI Backend"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings from environment variables"""

    # Application
    APP_NAME: str = "SAKHA AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG_MODE", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Database
    DATABASE_TYPE: str = os.getenv("DATABASE_TYPE", "mongodb")
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "sakha_db")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "jwt-secret-key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION: int = int(os.getenv("JWT_EXPIRATION", "86400"))

    # AI Services
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo")

    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-pro")

    DEFAULT_AI_PROVIDER: str = os.getenv("DEFAULT_AI_PROVIDER", "openai")
    AI_TIMEOUT: int = int(os.getenv("AI_TIMEOUT", "30"))

    # Image Generation
    STABILITY_AI_API_KEY: Optional[str] = os.getenv("STABILITY_AI_API_KEY")

    # Server
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    SERVER_URL: str = os.getenv("SERVER_URL", "http://localhost:8000")

    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    ALLOW_ORIGINS: list = ["localhost", "127.0.0.1"]

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))

    # Storage
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    UPLOAD_DIR: str = os.path.join(os.path.dirname(__file__), "uploads")

    # Features
    ENABLE_CHAT: bool = True
    ENABLE_IMAGE_GENERATION: bool = True
    ENABLE_FILE_ANALYSIS: bool = True
    ENABLE_ADMIN: bool = True


settings = Settings()
