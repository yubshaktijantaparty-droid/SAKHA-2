"""Database Service for SAKHA AI - Chat History and User Data Persistence"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from bson.objectid import ObjectId
import logging

from sakha.database.mongodb import mongodb

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for handling all database operations"""
    
    @staticmethod
    async def save_chat(user_id: str, title: str, model: str = "gpt-4o") -> Dict[str, Any]:
        """Create a new chat session"""
        try:
            # Check if MongoDB is available
            if mongodb.db is None:
                logger.warning("MongoDB not available - chat not persisted")
                return {"_id": "demo-" + str(datetime.utcnow().timestamp()), "user_id": user_id, "title": title, "model": model}
            
            chat_doc = {
                "user_id": user_id,
                "title": title,
                "model": model,
                "messages": [],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "message_count": 0,
                "is_archived": False,
                "is_pinned": False,
            }
            
            result = await mongodb.db.chats.insert_one(chat_doc)
            chat_doc["_id"] = str(result.inserted_id)
            logger.info(f"Chat created for user {user_id}: {result.inserted_id}")
            return chat_doc
            
        except Exception as e:
            logger.error(f"Error creating chat: {e}")
            raise
    
    @staticmethod
    async def save_message(
        chat_id: str,
        user_id: str,
        role: str,
        content: str,
        model: str = "gpt-4o",
        tokens_used: Optional[int] = None
    ) -> Dict[str, Any]:
        """Save a message to chat history"""
        try:
            message_doc = {
                "chat_id": chat_id,
                "user_id": user_id,
                "role": role,
                "content": content,
                "model": model,
                "tokens_used": tokens_used,
                "created_at": datetime.utcnow(),
                "likes": 0,
                "dislikes": 0,
            }
            
            # Check if MongoDB is available
            if mongodb.db is None:
                logger.warning("MongoDB not available - message not persisted")
                message_doc["_id"] = "demo-" + str(datetime.utcnow().timestamp())
                return message_doc
            
            result = await mongodb.db.messages.insert_one(message_doc)
            message_doc["_id"] = str(result.inserted_id)
            
            # Update chat with new message count and timestamp
            await mongodb.db.chats.update_one(
                {"_id": ObjectId(chat_id)},
                {
                    "$inc": {"message_count": 1},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            
            logger.info(f"Message saved to chat {chat_id}")
            return message_doc
            
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            raise
    
    @staticmethod
    async def get_chat_messages(chat_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve all messages from a chat"""
        try:
            messages = await mongodb.db.messages.find(
                {"chat_id": chat_id}
            ).sort("created_at", 1).limit(limit).to_list(limit)
            
            # Convert ObjectId to string
            for msg in messages:
                msg["_id"] = str(msg["_id"])
                msg["created_at"] = msg["created_at"].isoformat()
            
            logger.info(f"Retrieved {len(messages)} messages from chat {chat_id}")
            return messages
            
        except Exception as e:
            logger.error(f"Error retrieving messages: {e}")
            return []
    
    @staticmethod
    async def get_user_chats(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all chats for a user"""
        try:
            chats = await mongodb.db.chats.find(
                {"user_id": user_id, "is_archived": False}
            ).sort("updated_at", -1).limit(limit).to_list(limit)
            
            # Convert ObjectId to string and ISO format dates
            for chat in chats:
                chat["_id"] = str(chat["_id"])
                chat["created_at"] = chat["created_at"].isoformat()
                chat["updated_at"] = chat["updated_at"].isoformat()
            
            logger.info(f"Retrieved {len(chats)} chats for user {user_id}")
            return chats
            
        except Exception as e:
            logger.error(f"Error retrieving chats: {e}")
            return []
    
    @staticmethod
    async def update_chat_title(chat_id: str, new_title: str) -> bool:
        """Update chat title"""
        try:
            result = await mongodb.db.chats.update_one(
                {"_id": ObjectId(chat_id)},
                {"$set": {"title": new_title, "updated_at": datetime.utcnow()}}
            )
            
            logger.info(f"Chat {chat_id} title updated")
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating chat title: {e}")
            return False
    
    @staticmethod
    async def delete_chat(chat_id: str) -> bool:
        """Delete a chat and its messages"""
        try:
            # Delete all messages in the chat
            await mongodb.db.messages.delete_many({"chat_id": chat_id})
            
            # Delete the chat
            result = await mongodb.db.chats.delete_one({"_id": ObjectId(chat_id)})
            
            logger.info(f"Chat {chat_id} and its messages deleted")
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error deleting chat: {e}")
            return False
    
    @staticmethod
    async def archive_chat(chat_id: str) -> bool:
        """Archive a chat"""
        try:
            result = await mongodb.db.chats.update_one(
                {"_id": ObjectId(chat_id)},
                {"$set": {"is_archived": True, "updated_at": datetime.utcnow()}}
            )
            
            logger.info(f"Chat {chat_id} archived")
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error archiving chat: {e}")
            return False
    
    @staticmethod
    async def save_user_settings(user_id: str, settings: Dict[str, Any]) -> bool:
        """Save user preferences and settings"""
        try:
            settings_doc = {
                "user_id": user_id,
                "model": settings.get("model", "gpt-4o"),
                "temperature": settings.get("temperature", 0.7),
                "theme": settings.get("theme", "dark"),
                "language": settings.get("language", "en"),
                "updated_at": datetime.utcnow(),
            }
            
            result = await mongodb.db.settings.update_one(
                {"user_id": user_id},
                {"$set": settings_doc},
                upsert=True
            )
            
            logger.info(f"Settings saved for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving user settings: {e}")
            return False
    
    @staticmethod
    async def get_user_settings(user_id: str) -> Dict[str, Any]:
        """Get user settings"""
        try:
            settings = await mongodb.db.settings.find_one({"user_id": user_id})
            
            if settings:
                settings["_id"] = str(settings["_id"])
                logger.info(f"Settings retrieved for user {user_id}")
                return settings
            
            # Return defaults if not found
            return {
                "model": "gpt-4o",
                "temperature": 0.7,
                "theme": "dark",
                "language": "en",
            }
            
        except Exception as e:
            logger.error(f"Error retrieving user settings: {e}")
            return {}
    
    @staticmethod
    async def save_memory(user_id: str, memory_type: str, content: str) -> bool:
        """Save user memory (context for AI)"""
        try:
            memory_doc = {
                "user_id": user_id,
                "memory_type": memory_type,
                "content": content,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
            
            await mongodb.db.memories.insert_one(memory_doc)
            logger.info(f"Memory saved for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
            return False
    
    @staticmethod
    async def get_user_memory(user_id: str, memory_type: str = "general") -> Optional[str]:
        """Get user memory"""
        try:
            memory = await mongodb.db.memories.find_one(
                {"user_id": user_id, "memory_type": memory_type}
            )
            
            if memory:
                return memory["content"]
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving memory: {e}")
            return None
    
    @staticmethod
    async def save_image(
        user_id: str,
        prompt: str,
        image_url: str,
        provider: str = "unknown"
    ) -> bool:
        """Save generated image metadata"""
        try:
            image_doc = {
                "user_id": user_id,
                "prompt": prompt,
                "image_url": image_url,
                "provider": provider,
                "created_at": datetime.utcnow(),
            }
            
            await mongodb.db.images.insert_one(image_doc)
            logger.info(f"Image saved for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving image: {e}")
            return False
    
    @staticmethod
    async def get_image_history(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get user's image generation history"""
        try:
            images = await mongodb.db.images.find(
                {"user_id": user_id}
            ).sort("created_at", -1).limit(limit).to_list(limit)
            
            # Convert ObjectId to string
            for img in images:
                img["_id"] = str(img["_id"])
                img["created_at"] = img["created_at"].isoformat()
            
            logger.info(f"Retrieved {len(images)} images for user {user_id}")
            return images
            
        except Exception as e:
            logger.error(f"Error retrieving image history: {e}")
            return []
    
    @staticmethod
    async def health_check() -> Dict[str, Any]:
        """Check database health"""
        try:
            await mongodb.db.command('ping')
            
            # Get collection stats
            chats_count = await mongodb.db.chats.count_documents({})
            messages_count = await mongodb.db.messages.count_documents({})
            users_count = await mongodb.db.settings.count_documents({})
            
            return {
                "status": "healthy",
                "database": "MongoDB",
                "chats": chats_count,
                "messages": messages_count,
                "users": users_count,
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
            }


# Global instance
db_service = DatabaseService()
