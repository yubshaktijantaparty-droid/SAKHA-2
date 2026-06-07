"""
WhatsApp Integration for SAKHA Bot
"""
from typing import Optional, Dict, Any, Callable
from abc import ABC, abstractmethod
from datetime import datetime
import json
from sakha.config import settings
from sakha.utils import logger


class WhatsAppMessage:
    """WhatsApp Message Model"""
    
    def __init__(self, sender_id: str, text: str, message_type: str = "text", 
                 timestamp: Optional[datetime] = None, media_url: str = None):
        self.sender_id = sender_id
        self.text = text
        self.message_type = message_type  # text, image, document, audio, video
        self.timestamp = timestamp or datetime.utcnow()
        self.media_url = media_url
        self.is_command = text.startswith(settings.bot_prefix) if text else False
        
        if self.is_command:
            parts = text.split(maxsplit=1)
            self.command = parts[0][1:]  # Remove prefix
            self.args = parts[1] if len(parts) > 1 else ""
        else:
            self.command = None
            self.args = None


class WhatsAppProvider(ABC):
    """Abstract WhatsApp Provider"""
    
    @abstractmethod
    async def send_message(self, to: str, message: str) -> bool:
        pass
    
    @abstractmethod
    async def send_media(self, to: str, media_url: str, caption: str = None) -> bool:
        pass
    
    @abstractmethod
    async def mark_as_read(self, message_id: str) -> bool:
        pass
    
    @abstractmethod
    async def start_listening(self) -> None:
        pass


class BaileysProvider(WhatsAppProvider):
    """Baileys (WhatsApp Web) Provider"""
    
    def __init__(self):
        self.is_connected = False
        self.session_name = settings.whatsapp_session_name
        logger.info(f"Baileys provider initialized with session: {self.session_name}")
    
    async def connect(self) -> bool:
        """Connect to WhatsApp via Baileys"""
        try:
            # This would normally connect via Node.js backend
            logger.info("Connecting to WhatsApp via Baileys...")
            self.is_connected = True
            logger.info("✓ Connected to WhatsApp")
            return True
        except Exception as e:
            logger.error(f"Baileys connection error: {e}")
            return False
    
    async def send_message(self, to: str, message: str) -> bool:
        """Send message via Baileys"""
        try:
            if not self.is_connected:
                logger.error("Not connected to WhatsApp")
                return False
            
            logger.info(f"Sending message to {to}: {message[:50]}...")
            # Actual send logic would go here
            return True
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    async def send_media(self, to: str, media_url: str, caption: str = None) -> bool:
        """Send media via Baileys"""
        try:
            if not self.is_connected:
                return False
            
            logger.info(f"Sending media to {to}: {media_url}")
            return True
        except Exception as e:
            logger.error(f"Error sending media: {e}")
            return False
    
    async def mark_as_read(self, message_id: str) -> bool:
        """Mark message as read"""
        try:
            logger.debug(f"Marking message {message_id} as read")
            return True
        except Exception as e:
            logger.error(f"Error marking message as read: {e}")
            return False
    
    async def start_listening(self) -> None:
        """Start listening for messages"""
        try:
            logger.info("Starting WhatsApp message listener...")
            # Actual listening logic would go here
        except Exception as e:
            logger.error(f"Error in message listener: {e}")


class TwilioProvider(WhatsAppProvider):
    """Twilio WhatsApp Provider"""
    
    def __init__(self):
        self.account_sid = settings.twilio_account_sid
        self.auth_token = settings.twilio_auth_token
        self.phone_number = settings.twilio_phone_number
        logger.info("Twilio provider initialized")
    
    async def send_message(self, to: str, message: str) -> bool:
        """Send message via Twilio"""
        try:
            # Twilio API call would go here
            logger.info(f"Sending Twilio message to {to}")
            return True
        except Exception as e:
            logger.error(f"Twilio error: {e}")
            return False
    
    async def send_media(self, to: str, media_url: str, caption: str = None) -> bool:
        """Send media via Twilio"""
        try:
            logger.info(f"Sending Twilio media to {to}")
            return True
        except Exception as e:
            logger.error(f"Twilio media error: {e}")
            return False
    
    async def mark_as_read(self, message_id: str) -> bool:
        """Mark message as read"""
        return True
    
    async def start_listening(self) -> None:
        """Start listening for Twilio messages"""
        logger.info("Twilio message listener started")


class WhatsAppBusinessProvider(WhatsAppProvider):
    """WhatsApp Business API Provider"""
    
    def __init__(self):
        self.account_id = settings.whatsapp_business_account_id
        self.phone_number_id = settings.whatsapp_business_phone_number_id
        self.access_token = settings.whatsapp_business_access_token
        logger.info("WhatsApp Business API provider initialized")
    
    async def send_message(self, to: str, message: str) -> bool:
        """Send message via WhatsApp Business API"""
        try:
            logger.info(f"Sending WhatsApp Business message to {to}")
            return True
        except Exception as e:
            logger.error(f"WhatsApp Business error: {e}")
            return False
    
    async def send_media(self, to: str, media_url: str, caption: str = None) -> bool:
        """Send media via WhatsApp Business API"""
        try:
            logger.info(f"Sending WhatsApp Business media to {to}")
            return True
        except Exception as e:
            logger.error(f"WhatsApp Business media error: {e}")
            return False
    
    async def mark_as_read(self, message_id: str) -> bool:
        """Mark message as read"""
        return True
    
    async def start_listening(self) -> None:
        """Start listening for messages"""
        logger.info("WhatsApp Business message listener started")


class WhatsAppManager:
    """WhatsApp Manager"""
    
    def __init__(self):
        self.provider = self._initialize_provider()
        self.message_handlers: Dict[str, Callable] = {}
    
    def _initialize_provider(self) -> WhatsAppProvider:
        """Initialize WhatsApp provider"""
        # Default to Baileys
        return BaileysProvider()
    
    def register_handler(self, command: str, handler: Callable) -> None:
        """Register command handler"""
        self.message_handlers[command] = handler
    
    async def start(self) -> None:
        """Start WhatsApp manager"""
        try:
            if isinstance(self.provider, BaileysProvider):
                await self.provider.connect()
            
            await self.provider.start_listening()
            logger.info("✓ WhatsApp manager started")
        except Exception as e:
            logger.error(f"Error starting WhatsApp manager: {e}")
    
    async def send_text(self, to: str, message: str) -> bool:
        """Send text message"""
        return await self.provider.send_message(to, message)
    
    async def send_media(self, to: str, media_url: str, caption: str = None) -> bool:
        """Send media"""
        return await self.provider.send_media(to, media_url, caption)
    
    async def handle_message(self, message: WhatsAppMessage) -> None:
        """Handle incoming message"""
        try:
            if message.is_command:
                handler = self.message_handlers.get(message.command)
                if handler:
                    await handler(message)
            else:
                # Regular message handler
                logger.info(f"Message from {message.sender_id}: {message.text}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")


# Global WhatsApp manager
whatsapp_manager = WhatsAppManager()
