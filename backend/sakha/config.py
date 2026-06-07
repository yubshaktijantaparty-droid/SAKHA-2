"""Configuration for SAKHA AI Backend - Premium Edition"""

import os
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings from environment variables"""

    # Application
    APP_NAME: str = "SAKHA AI Premium"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = os.getenv("DEBUG_MODE", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Database
    DATABASE_TYPE: str = os.getenv("DATABASE_TYPE", "mongodb")
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "sakha_premium_db")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "jwt-secret-key")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = int(os.getenv("JWT_EXPIRATION", "86400"))
    JWT_REFRESH_EXPIRATION: int = int(os.getenv("JWT_REFRESH_EXPIRATION", "604800"))

    # AI Services - OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODELS: List[str] = ["gpt-5", "gpt-4o", "gpt-4-turbo", "gpt-4"]

    # AI Services - Anthropic (Claude)
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODELS: List[str] = ["claude-opus-4", "claude-sonnet-4"]

    # AI Services - Google Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODELS: List[str] = ["gemini-2.5-pro", "gemini-2.5-flash"]

    # AI Services - DeepSeek
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_MODELS: List[str] = ["deepseek-chat", "deepseek-reasoner"]

    # AI Services - OpenRouter (Multi-model support)
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")

    # AI Services - General
    DEFAULT_AI_PROVIDER: str = os.getenv("DEFAULT_AI_PROVIDER", "openai")
    DEFAULT_AI_MODEL: str = os.getenv("DEFAULT_AI_MODEL", "gpt-4o")
    AI_TIMEOUT: int = int(os.getenv("AI_TIMEOUT", "60"))
    AI_MAX_TOKENS: int = 4096
    AI_TEMPERATURE: float = 0.7

    # Image Generation
    STABILITY_AI_API_KEY: Optional[str] = os.getenv("STABILITY_AI_API_KEY")

    # Voice Services
    ELEVENLABS_API_KEY: Optional[str] = os.getenv("ELEVENLABS_API_KEY")
    GOOGLE_SPEECH_API_KEY: Optional[str] = os.getenv("GOOGLE_SPEECH_API_KEY")

    # Search Services
    PERPLEXITY_API_KEY: Optional[str] = os.getenv("PERPLEXITY_API_KEY")
    TAVILY_API_KEY: Optional[str] = os.getenv("TAVILY_API_KEY")
    GOOGLE_SEARCH_API_KEY: Optional[str] = os.getenv("GOOGLE_SEARCH_API_KEY")

    # Server
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    SERVER_URL: str = os.getenv("SERVER_URL", "http://localhost:8000")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        os.getenv("FRONTEND_URL", "").rstrip("/"),
    ]

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))

    # Storage
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    UPLOAD_DIR: str = os.path.join(os.path.dirname(__file__), "uploads")
    ALLOWED_UPLOAD_TYPES: List[str] = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
        "text/csv",
        "application/json",
        "image/png",
        "image/jpeg",
        "image/webp",
    ]

    # Features
    ENABLE_CHAT: bool = True
    ENABLE_STREAMING: bool = True
    ENABLE_IMAGE_GENERATION: bool = True
    ENABLE_FILE_ANALYSIS: bool = True
    ENABLE_WEB_SEARCH: bool = True
    ENABLE_VOICE: bool = True
    ENABLE_MEMORY: bool = True
    ENABLE_SHARING: bool = True
    ENABLE_EXPORT: bool = True
    ENABLE_ADMIN: bool = True

    # Cache
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
    CACHE_TTL: int = 3600  # 1 hour

    # Monitoring & Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN")


# Create singleton instance
settings = Settings()
