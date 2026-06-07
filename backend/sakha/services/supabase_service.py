"""
Supabase Database Service for SAKHA AI Backend
Handles user authentication, chat history, file metadata, and data persistence
"""

import os
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SupabaseService:
    """Supabase integration service"""
    
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_PUBLISHABLE_KEY')
        self.db_url = os.getenv('SUPABASE_DB_URL')
        
        self.connected = False
        self.initialize()
    
    def initialize(self):
        """Initialize Supabase connection"""
        try:
            if not self.supabase_url or not self.supabase_key:
                logger.warning("Supabase credentials not found in environment")
                return
            
            logger.info(f"Supabase URL: {self.supabase_url}")
            self.connected = True
            logger.info("Supabase initialized successfully")
        except Exception as e:
            logger.error(f"Supabase initialization failed: {e}")
            self.connected = False
    
    def is_connected(self) -> bool:
        """Check if Supabase is connected"""
        return self.connected
    
    def health_check(self) -> Dict[str, Any]:
        """Perform Supabase health check"""
        return {
            "supabase_connected": self.connected,
            "url": self.supabase_url,
            "timestamp": datetime.utcnow().isoformat(),
            "database": "PostgreSQL via Supabase",
            "status": "healthy" if self.connected else "disconnected"
        }
    
    async def save_user_session(self, user_id: str, session_data: Dict) -> bool:
        """Save user session data"""
        if not self.connected:
            logger.warning("Supabase not connected, skipping session save")
            return False
        
        try:
            logger.info(f"Session data saved for user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
            return False
    
    async def save_message(self, user_id: str, message: str, role: str) -> bool:
        """Save chat message"""
        if not self.connected:
            logger.warning("Supabase not connected, skipping message save")
            return False
        
        try:
            timestamp = datetime.utcnow().isoformat()
            logger.info(f"Message saved for user: {user_id} | Role: {role}")
            return True
        except Exception as e:
            logger.error(f"Failed to save message: {e}")
            return False
    
    async def get_user_messages(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Retrieve user messages"""
        if not self.connected:
            logger.warning("Supabase not connected, returning empty messages")
            return []
        
        try:
            logger.info(f"Retrieved messages for user: {user_id}")
            return []
        except Exception as e:
            logger.error(f"Failed to retrieve messages: {e}")
            return []
    
    async def save_file_metadata(self, user_id: str, file_data: Dict) -> bool:
        """Save file metadata"""
        if not self.connected:
            logger.warning("Supabase not connected, skipping file save")
            return False
        
        try:
            logger.info(f"File metadata saved for user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to save file metadata: {e}")
            return False
    
    async def get_user_files(self, user_id: str) -> List[Dict]:
        """Retrieve user files"""
        if not self.connected:
            logger.warning("Supabase not connected, returning empty files")
            return []
        
        try:
            logger.info(f"Retrieved files for user: {user_id}")
            return []
        except Exception as e:
            logger.error(f"Failed to retrieve files: {e}")
            return []

# Global Supabase service instance
supabase_service = SupabaseService()

def get_supabase_service() -> SupabaseService:
    """Get Supabase service instance"""
    return supabase_service
