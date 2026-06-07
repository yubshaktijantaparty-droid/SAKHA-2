"""Chat and Message models for SAKHA AI Premium"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class MessageModel(BaseModel):
    """Message model"""
    id: Optional[str] = None
    chat_id: str
    user_id: str
    role: str  # "user" or "assistant"
    content: str
    model: str  # Which model was used
    
    # Metadata
    tokens_used: Optional[int] = None
    tokens_prompt: Optional[int] = None
    tokens_completion: Optional[int] = None
    
    # Features
    edited_at: Optional[datetime] = None
    edited_content: Optional[str] = None
    
    # Reactions
    likes: int = 0
    dislikes: int = 0
    
    # Attachments
    attachments: List[Dict[str, Any]] = []
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "chat_id": "chat_123",
                "user_id": "user_123",
                "role": "user",
                "content": "What is the capital of France?",
                "model": "gpt-4o",
                "created_at": "2026-06-07T10:00:00Z"
            }
        }


class ChatModel(BaseModel):
    """Chat conversation model"""
    id: Optional[str] = None
    user_id: str
    title: str
    description: Optional[str] = None
    
    # Messages
    messages: List[MessageModel] = []
    
    # Configuration
    model: str = "gpt-4o"
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    
    # Memory
    memory_enabled: bool = True
    user_memory_context: Optional[str] = None
    
    # Metadata
    total_tokens: int = 0
    message_count: int = 0
    
    # Settings
    is_archived: bool = False
    is_pinned: bool = False
    is_shared: bool = False
    share_token: Optional[str] = None
    share_password: Optional[str] = None
    
    # Tags
    tags: List[str] = []
    
    # Folder organization
    folder: Optional[str] = None
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "title": "Python Development Help",
                "model": "gpt-4o",
                "messages": []
            }
        }
