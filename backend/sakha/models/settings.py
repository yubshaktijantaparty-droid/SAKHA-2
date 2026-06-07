"""Settings model for SAKHA AI Premium"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List


class SettingsModel(BaseModel):
    """User settings model"""
    id: Optional[str] = None
    user_id: str
    
    # UI Settings
    theme: str = "dark"
    language: str = "en"
    sidebar_collapsed: bool = False
    auto_expand_code: bool = True
    
    # Chat Settings
    default_model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 2048
    system_prompt: Optional[str] = None
    
    # Feature Toggles
    enable_memory: bool = True
    enable_web_search: bool = True
    enable_voice: bool = True
    enable_image_generation: bool = True
    enable_file_upload: bool = True
    
    # Privacy
    save_chat_history: bool = True
    allow_data_analysis: bool = False
    delete_chats_after_days: Optional[int] = None  # Auto-delete after N days
    
    # Notifications
    enable_notifications: bool = True
    notify_on_chat_ready: bool = True
    notify_on_image_ready: bool = True
    
    # Keyboard Shortcuts
    shortcuts: Dict[str, str] = {
        "new_chat": "Ctrl+N",
        "search": "Ctrl+K",
        "settings": "Ctrl+,",
    }
    
    # API Settings
    rate_limit_requests: int = 100
    rate_limit_tokens: int = 10000000
    
    # Advanced
    advanced_settings: Dict[str, Any] = {}
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "theme": "dark",
                "language": "en",
                "default_model": "gpt-4o"
            }
        }
