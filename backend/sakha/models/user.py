"""User model for SAKHA AI Premium"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class ThemeType(str, Enum):
    """Theme options"""
    DARK = "dark"
    LIGHT = "light"
    AUTO = "auto"


class LanguageType(str, Enum):
    """Language options"""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    CHINESE = "zh"
    JAPANESE = "ja"
    RUSSIAN = "ru"
    ARABIC = "ar"


class UserPreferences(BaseModel):
    """User preferences"""
    theme: ThemeType = ThemeType.DARK
    language: LanguageType = LanguageType.ENGLISH
    default_model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 2048
    enable_memory: bool = True
    enable_voice: bool = True
    enable_notifications: bool = True
    auto_save_chats: bool = True
    send_usage_data: bool = False


class UserModel(BaseModel):
    """User model"""
    id: Optional[str] = None
    email: EmailStr
    username: str
    password_hash: str
    full_name: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    
    # Preferences
    preferences: UserPreferences = UserPreferences()
    
    # Stats
    total_messages: int = 0
    total_chats: int = 0
    total_tokens_used: int = 0
    total_images_generated: int = 0
    
    # Limits
    monthly_tokens_limit: int = 10000000  # 10M tokens
    monthly_api_calls_limit: int = 100000
    
    # Account
    is_active: bool = True
    is_premium: bool = False
    premium_until: Optional[datetime] = None
    
    # API Keys
    api_keys: Dict[str, str] = {}  # User's API keys for integrations
    
    # Metadata
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password_hash": "hashed_password",
                "full_name": "John Doe",
                "preferences": {
                    "theme": "dark",
                    "language": "en",
                    "default_model": "gpt-4o"
                }
            }
        }
