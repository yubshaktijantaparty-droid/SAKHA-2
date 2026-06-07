"""Memory model for SAKHA AI Premium"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List


class MemoryModel(BaseModel):
    """User memory model for maintaining context across conversations"""
    id: Optional[str] = None
    user_id: str
    
    # Basic info
    name: str  # e.g., "About You", "Work Context", "Preferences"
    description: Optional[str] = None
    
    # Memory content
    content: str
    
    # Types
    memory_type: str  # "personal", "work", "preferences", "custom"
    
    # Status
    is_active: bool = True
    importance: int = 5  # 1-10 scale, affects priority in context
    
    # Organization
    category: Optional[str] = None
    tags: List[str] = []
    
    # Usage tracking
    times_used: int = 0
    last_used: Optional[datetime] = None
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None  # Optional expiration
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "name": "About You",
                "content": "I am a software engineer with 5 years of experience in Python and JavaScript",
                "memory_type": "personal",
                "is_active": True
            }
        }
