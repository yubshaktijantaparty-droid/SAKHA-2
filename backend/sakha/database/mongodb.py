"""MongoDB database connection and setup"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING, TEXT
import logging
from sakha.config import settings

logger = logging.getLogger(__name__)


class MongoDB:
    """MongoDB database handler"""
    
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None
    
    @classmethod
    async def connect_db(cls):
        """Connect to MongoDB"""
        try:
            cls.client = AsyncIOMotorClient(settings.MONGODB_URI)
            cls.db = cls.client[settings.MONGODB_DB_NAME]
            
            # Verify connection
            await cls.db.command('ping')
            logger.info("✓ Connected to MongoDB")
            
            # Create indexes
            await cls._create_indexes()
            
        except Exception as e:
            logger.warning(f"⚠ MongoDB connection failed: {e}")
            logger.warning("Running in demo mode without persistence")
            cls.client = None
            cls.db = None
    
    @classmethod
    async def close_db(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()
            logger.info("✓ Disconnected from MongoDB")
    
    @classmethod
    async def _create_indexes(cls):
        """Create database indexes for performance"""
        
        # Users collection
        await cls.db.users.create_index([("email", ASCENDING)], unique=True)
        await cls.db.users.create_index([("username", ASCENDING)], unique=True)
        
        # Chats collection
        await cls.db.chats.create_index([("user_id", ASCENDING)])
        await cls.db.chats.create_index([("created_at", DESCENDING)])
        await cls.db.chats.create_index([("updated_at", DESCENDING)])
        await cls.db.chats.create_index([("title", TEXT), ("description", TEXT)])  # Full-text search
        
        # Messages collection
        await cls.db.messages.create_index([("chat_id", ASCENDING)])
        await cls.db.messages.create_index([("user_id", ASCENDING)])
        await cls.db.messages.create_index([("created_at", DESCENDING)])
        
        # Memories collection
        await cls.db.memories.create_index([("user_id", ASCENDING)])
        await cls.db.memories.create_index([("memory_type", ASCENDING)])
        
        # Files collection
        await cls.db.files.create_index([("user_id", ASCENDING)])
        await cls.db.files.create_index([("created_at", DESCENDING)])
        
        # Settings collection
        await cls.db.settings.create_index([("user_id", ASCENDING)], unique=True)
        
        logger.info("✓ Database indexes created")


# Global instance
mongodb = MongoDB()
