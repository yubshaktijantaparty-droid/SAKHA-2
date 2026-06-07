"""
Database Connection & Operations
"""
from typing import Optional, List, Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from pymongo import MongoClient
from pymongo.database import Database
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import asyncio
from datetime import datetime

from sakha.config import settings
from .models import Base


class DatabaseManager:
    """Database Management"""
    
    def __init__(self):
        self.db_type = settings.database_type
        self.engine = None
        self.async_engine = None
        self.SessionLocal = None
        self.async_session = None
        self.mongodb_client = None
        self.mongodb_db = None
        self.motor_client = None
        self.motor_db = None
    
    async def connect(self):
        """Connect to database"""
        if self.db_type == "mongodb":
            await self._connect_mongodb()
        elif self.db_type == "postgresql":
            await self._connect_postgresql()
    
    async def disconnect(self):
        """Disconnect from database"""
        if self.db_type == "mongodb":
            if self.motor_client:
                self.motor_client.close()
        elif self.db_type == "postgresql":
            if self.async_engine:
                await self.async_engine.dispose()
    
    async def _connect_mongodb(self):
        """Connect to MongoDB"""
        try:
            self.motor_client = AsyncIOMotorClient(settings.mongodb_uri)
            self.motor_db = self.motor_client[settings.mongodb_db_name]
            # Test connection
            await self.motor_client.admin.command('ping')
            print("✓ Connected to MongoDB")
        except Exception as e:
            print(f"✗ MongoDB Connection Error: {e}")
            raise
    
    async def _connect_postgresql(self):
        """Connect to PostgreSQL"""
        try:
            # Async engine
            self.async_engine = create_async_engine(
                settings.postgresql_uri,
                echo=settings.debug_mode,
                future=True
            )
            
            # Create tables
            async with self.async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            
            # Session factory
            self.async_session = async_sessionmaker(
                self.async_engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            print("✓ Connected to PostgreSQL")
        except Exception as e:
            print(f"✗ PostgreSQL Connection Error: {e}")
            raise
    
    def get_mongodb_db(self) -> AsyncIOMotorDatabase:
        """Get MongoDB database instance"""
        if not self.motor_db:
            raise RuntimeError("MongoDB not connected")
        return self.motor_db
    
    async def get_db_session(self) -> AsyncSession:
        """Get PostgreSQL session"""
        if not self.async_session:
            raise RuntimeError("PostgreSQL not connected")
        async with self.async_session() as session:
            yield session


# Global database manager
db_manager = DatabaseManager()


# MongoDB Collection Helpers
class MongoDBOperations:
    """MongoDB Operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def create_user(self, user_id: str, data: Dict[str, Any]) -> bool:
        """Create new user"""
        try:
            user = {
                "_id": user_id,
                "name": data.get("name", "User"),
                "phone_number": data.get("phone_number"),
                "language": data.get("language", "en"),
                "is_banned": False,
                "total_messages": 0,
                "total_commands": 0,
                "created_at": datetime.utcnow(),
                "last_seen": datetime.utcnow(),
                "preferences": data.get("preferences", {})
            }
            await self.db.users.insert_one(user)
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    async def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        return await self.db.users.find_one({"_id": user_id})
    
    async def update_user(self, user_id: str, data: Dict[str, Any]) -> bool:
        """Update user"""
        try:
            data["last_seen"] = datetime.utcnow()
            await self.db.users.update_one(
                {"_id": user_id},
                {"$set": data}
            )
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    async def ban_user(self, user_id: str, reason: str, duration: int) -> bool:
        """Ban user"""
        try:
            ban_until = datetime.utcnow() + timedelta(seconds=duration)
            await self.db.users.update_one(
                {"_id": user_id},
                {
                    "$set": {
                        "is_banned": True,
                        "ban_reason": reason,
                        "ban_until": ban_until
                    }
                }
            )
            return True
        except Exception as e:
            print(f"Error banning user: {e}")
            return False
    
    async def save_conversation(self, conv_id: str, data: Dict[str, Any]) -> bool:
        """Save conversation"""
        try:
            data["_id"] = conv_id
            data["created_at"] = datetime.utcnow()
            await self.db.conversations.insert_one(data)
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False
    
    async def get_user_conversations(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user conversations"""
        try:
            conversations = await self.db.conversations.find(
                {"user_id": user_id}
            ).sort("created_at", -1).limit(limit).to_list(length=limit)
            return conversations
        except Exception as e:
            print(f"Error getting conversations: {e}")
            return []
    
    async def create_note(self, note_id: str, data: Dict[str, Any]) -> bool:
        """Create note"""
        try:
            note = {
                "_id": note_id,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                **data
            }
            await self.db.notes.insert_one(note)
            return True
        except Exception as e:
            print(f"Error creating note: {e}")
            return False
    
    async def get_user_notes(self, user_id: str, limit: int = 100) -> List[Dict]:
        """Get user notes"""
        try:
            notes = await self.db.notes.find(
                {"user_id": user_id, "is_archived": False}
            ).sort("updated_at", -1).limit(limit).to_list(length=limit)
            return notes
        except Exception as e:
            print(f"Error getting notes: {e}")
            return []
    
    async def create_reminder(self, reminder_id: str, data: Dict[str, Any]) -> bool:
        """Create reminder"""
        try:
            reminder = {
                "_id": reminder_id,
                "created_at": datetime.utcnow(),
                "is_completed": False,
                **data
            }
            await self.db.reminders.insert_one(reminder)
            return True
        except Exception as e:
            print(f"Error creating reminder: {e}")
            return False
    
    async def get_pending_reminders(self, user_id: str = None) -> List[Dict]:
        """Get pending reminders"""
        try:
            query = {"is_completed": False}
            if user_id:
                query["user_id"] = user_id
            
            reminders = await self.db.reminders.find(query).to_list(length=None)
            return reminders
        except Exception as e:
            print(f"Error getting reminders: {e}")
            return []
    
    async def get_analytics(self, date_from: datetime = None) -> Dict[str, Any]:
        """Get analytics"""
        try:
            query = {}
            if date_from:
                query["timestamp"] = {"$gte": date_from}
            
            analytics = await self.db.analytics.find_one(query, sort=[("timestamp", -1)])
            return analytics or {}
        except Exception as e:
            print(f"Error getting analytics: {e}")
            return {}


async def get_mongodb_ops() -> MongoDBOperations:
    """Get MongoDB operations instance"""
    db = db_manager.get_mongodb_db()
    return MongoDBOperations(db)
