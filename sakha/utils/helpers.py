"""
Utility Functions for SAKHA Bot
"""
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from functools import wraps
import asyncio
from enum import Enum


# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SAKHA")


class Language(str, Enum):
    """Supported Languages"""
    EN = "en"
    BN = "bn"
    HI = "hi"
    HINGLISH = "hinglish"


async def async_timer(func):
    """Decorator to measure async function execution time"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = datetime.utcnow()
        result = await func(*args, **kwargs)
        duration = (datetime.utcnow() - start).total_seconds()
        logger.debug(f"{func.__name__} took {duration:.2f}s")
        return result
    return wrapper


def detect_language(text: str) -> Language:
    """Detect language from text"""
    try:
        # Simple detection based on script
        if any('\u0981' <= char <= '\u09FF' for char in text):
            return Language.BN
        elif any('\u0900' <= char <= '\u097F' for char in text):
            return Language.HI
        else:
            return Language.EN
    except Exception:
        return Language.EN


async def translate_text(text: str, target_lang: str) -> str:
    """Translate text to target language"""
    try:
        # This would use Google Translate API or similar
        logger.info(f"Translating text to {target_lang}")
        return f"[Translation to {target_lang}]: {text}"
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return text


def validate_phone_number(phone: str) -> bool:
    """Validate phone number"""
    import re
    pattern = r'^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$'
    return bool(re.match(pattern, phone))


def sanitize_input(user_input: str, max_length: int = 1000) -> str:
    """Sanitize user input"""
    if not user_input:
        return ""
    
    # Remove leading/trailing whitespace
    sanitized = user_input.strip()
    
    # Limit length
    sanitized = sanitized[:max_length]
    
    return sanitized


def parse_command(text: str, prefix: str = ".") -> tuple[Optional[str], str]:
    """Parse command from text"""
    if not text.startswith(prefix):
        return None, text
    
    parts = text.split(maxsplit=1)
    command = parts[0][1:]  # Remove prefix
    args = parts[1] if len(parts) > 1 else ""
    
    return command, args


async def rate_limit(user_id: str, max_requests: int = 10, time_window: int = 60) -> bool:
    """Check rate limit for user"""
    # This would use Redis in production
    logger.debug(f"Rate limit check for {user_id}: {max_requests}/{time_window}s")
    return True


async def cache_result(key: str, value: Any, ttl: int = 300) -> None:
    """Cache result"""
    logger.debug(f"Caching result for key: {key}")


async def get_cached_result(key: str) -> Optional[Any]:
    """Get cached result"""
    logger.debug(f"Looking for cached result: {key}")
    return None


class ResponseFormatter:
    """Format responses for WhatsApp"""
    
    @staticmethod
    def bold(text: str) -> str:
        """Make text bold"""
        return f"*{text}*"
    
    @staticmethod
    def italic(text: str) -> str:
        """Make text italic"""
        return f"_{text}_"
    
    @staticmethod
    def code(text: str) -> str:
        """Format as code"""
        return f"```{text}```"
    
    @staticmethod
    def quote(text: str) -> str:
        """Format as quote"""
        return f"> {text}"
    
    @staticmethod
    def list_items(items: list) -> str:
        """Format list"""
        return "\n".join(f"• {item}" for item in items)
    
    @staticmethod
    def numbered_list(items: list) -> str:
        """Format numbered list"""
        return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))
    
    @staticmethod
    def success(message: str) -> str:
        """Format success message"""
        return f"✅ {message}"
    
    @staticmethod
    def error(message: str) -> str:
        """Format error message"""
        return f"❌ {message}"
    
    @staticmethod
    def warning(message: str) -> str:
        """Format warning message"""
        return f"⚠️ {message}"
    
    @staticmethod
    def info(message: str) -> str:
        """Format info message"""
        return f"ℹ️ {message}"


class ErrorHandler:
    """Error handling utilities"""
    
    @staticmethod
    async def handle_error(error: Exception, context: Dict[str, Any] = None) -> str:
        """Handle error and return user-friendly message"""
        logger.error(f"Error: {error}", exc_info=True)
        
        error_messages = {
            "timeout": "⏱️ Request timed out. Please try again.",
            "network": "🌐 Network error. Please check your connection.",
            "permission": "🔒 Permission denied.",
            "validation": "❌ Invalid input. Please check and try again.",
        }
        
        error_type = type(error).__name__.lower()
        
        for key, message in error_messages.items():
            if key in error_type:
                return message
        
        return "❌ An error occurred. Please try again later."
    
    @staticmethod
    async def handle_command_error(command: str, error: Exception) -> str:
        """Handle command execution error"""
        logger.error(f"Command '{command}' error: {error}")
        return ResponseFormatter.error(f"Error executing {command}: {str(error)[:100]}")


# Export utilities
__all__ = [
    "logger", "Language", "detect_language", "translate_text",
    "validate_phone_number", "sanitize_input", "parse_command",
    "rate_limit", "cache_result", "get_cached_result",
    "ResponseFormatter", "ErrorHandler"
]
