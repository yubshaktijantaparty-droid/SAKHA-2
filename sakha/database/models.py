"""
Database Models for SAKHA Bot
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, Float, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field

Base = declarative_base()


class User(Base):
    """User Model"""
    __tablename__ = "users"
    
    id = Column(String(50), primary_key=True, unique=True)
    name = Column(String(100))
    phone_number = Column(String(20), unique=True)
    language = Column(String(10), default="en")
    is_banned = Column(Boolean, default=False)
    ban_reason = Column(String(500), nullable=True)
    ban_until = Column(DateTime, nullable=True)
    total_messages = Column(Integer, default=0)
    total_commands = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    preferences = Column(JSON, default={})
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user")
    notes = relationship("Note", back_populates="user")
    reminders = relationship("Reminder", back_populates="user")
    todos = relationship("Todo", back_populates="user")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "language": self.language,
            "is_banned": self.is_banned,
            "ban_reason": self.ban_reason,
            "ban_until": self.ban_until,
            "total_messages": self.total_messages,
            "total_commands": self.total_commands,
            "created_at": self.created_at,
            "last_seen": self.last_seen,
            "preferences": self.preferences
        }


class Conversation(Base):
    """Conversation/Chat History Model"""
    __tablename__ = "conversations"
    
    id = Column(String(50), primary_key=True, unique=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    message_text = Column(Text)
    response_text = Column(Text)
    command_used = Column(String(100), nullable=True)
    context = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    is_pinned = Column(Boolean, default=False)
    
    # Relationship
    user = relationship("User", back_populates="conversations")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "message_text": self.message_text,
            "response_text": self.response_text,
            "command_used": self.command_used,
            "context": self.context,
            "created_at": self.created_at,
            "is_pinned": self.is_pinned
        }


class Note(Base):
    """User Notes Model"""
    __tablename__ = "notes"
    
    id = Column(String(50), primary_key=True, unique=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    title = Column(String(200))
    content = Column(Text)
    category = Column(String(50), default="general")
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="notes")


class Reminder(Base):
    """Reminders Model"""
    __tablename__ = "reminders"
    
    id = Column(String(50), primary_key=True, unique=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    title = Column(String(200))
    description = Column(Text, nullable=True)
    scheduled_time = Column(DateTime)
    is_completed = Column(Boolean, default=False)
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="reminders")


class Todo(Base):
    """To-Do List Model"""
    __tablename__ = "todos"
    
    id = Column(String(50), primary_key=True, unique=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    title = Column(String(200))
    description = Column(Text, nullable=True)
    priority = Column(String(20), default="medium")
    is_completed = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=True)
    category = Column(String(50), default="general")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="todos")


class AdminLog(Base):
    """Admin Actions Log"""
    __tablename__ = "admin_logs"
    
    id = Column(String(50), primary_key=True, unique=True)
    admin_id = Column(String(50))
    action = Column(String(100))
    target_user_id = Column(String(50), nullable=True)
    details = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Analytics(Base):
    """Analytics Data"""
    __tablename__ = "analytics"
    
    id = Column(String(50), primary_key=True, unique=True)
    date = Column(DateTime, default=datetime.utcnow)
    total_users = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    total_messages = Column(Integer, default=0)
    total_commands = Column(Integer, default=0)
    avg_response_time = Column(Float, default=0)
    error_count = Column(Integer, default=0)
    command_stats = Column(JSON, default={})


# Pydantic Models for Request/Response

class UserResponse(BaseModel):
    """User Response Schema"""
    id: str
    name: str
    phone_number: str
    language: str
    is_banned: bool
    total_messages: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationCreate(BaseModel):
    """Create Conversation Schema"""
    user_id: str
    message_text: str
    command_used: Optional[str] = None
    context: Optional[Dict[str, Any]] = {}


class NoteCreate(BaseModel):
    """Create Note Schema"""
    title: str
    content: str
    category: str = "general"


class ReminderCreate(BaseModel):
    """Create Reminder Schema"""
    title: str
    description: Optional[str] = None
    scheduled_time: datetime
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None


class TodoCreate(BaseModel):
    """Create Todo Schema"""
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None
    category: str = "general"
