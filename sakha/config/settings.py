"""
SAKHA Bot Configuration Settings
"""
from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache


class Settings(BaseSettings):
    """Application Settings"""
    
    # Bot Settings
    bot_name: str = "SAKHA"
    bot_owner: str = "Pranab Goswami"
    bot_owner_id: str = "919999999999"
    bot_prefix: str = "."
    debug_mode: bool = False
    log_level: str = "INFO"
    
    # Database
    database_type: str = "mongodb"
    mongodb_uri: str = "mongodb+srv://username:password@cluster.mongodb.net/sakha"
    mongodb_db_name: str = "sakha_db"
    postgresql_uri: str = "postgresql://user:password@localhost:5432/sakha_db"
    
    # AI Services
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo"
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-chat"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-pro"
    default_ai_provider: str = "openai"
    ai_timeout: int = 30
    
    # WhatsApp
    whatsapp_auth_path: str = "./whatsapp_auth"
    whatsapp_session_name: str = "SAKHA_SESSION"
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""
    whatsapp_business_account_id: str = ""
    whatsapp_business_phone_number_id: str = ""
    whatsapp_business_access_token: str = ""
    
    # Server
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    server_url: str = "http://localhost:8000"
    environment: str = "development"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    jwt_secret: str = "your-jwt-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 86400
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600
    
    # Features
    enable_study_assistant: bool = True
    enable_business_assistant: bool = True
    enable_productivity: bool = True
    enable_admin_commands: bool = True
    enable_broadcast: bool = True
    enable_auto_moderation: bool = True
    enable_anti_spam: bool = True
    enable_anti_link: bool = False
    enable_analytics: bool = True
    
    # Moderation
    max_message_length: int = 1000
    max_messages_per_minute: int = 10
    spam_threshold: int = 5
    ban_duration: int = 86400
    allowed_domains: List[str] = ["youtube.com", "github.com", "linkedin.com"]
    block_shortened_urls: bool = True
    warn_before_block: bool = True
    
    # Notifications
    enable_reminders: bool = True
    enable_notifications: bool = True
    notification_check_interval: int = 300
    
    # Storage
    max_storage_per_user: int = 100
    notes_retention_days: int = 365
    archive_old_messages: bool = True
    message_retention_days: int = 90
    
    # External Services
    weather_api_key: str = ""
    news_api_key: str = ""
    
    # Logging
    log_file: str = "logs/sakha.log"
    log_max_bytes: int = 10485760
    log_backup_count: int = 5
    
    # Development
    reload_on_change: bool = True
    cors_origins: str = "*"
    
    # Sentry
    sentry_dsn: str = ""
    enable_monitoring: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Export settings instance
settings = get_settings()
