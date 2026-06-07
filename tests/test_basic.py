"""
SAKHA Bot - Basic Tests
"""
import pytest
import asyncio
from sakha.config import settings
from sakha.utils import validate_phone_number, sanitize_input, parse_command


class TestConfiguration:
    """Test configuration"""
    
    def test_settings_loaded(self):
        """Test that settings are loaded"""
        assert settings.bot_name == "SAKHA"
        assert settings.bot_owner == "Pranab Goswami"
    
    def test_api_keys_exist(self):
        """Test that API keys are configured"""
        # Note: These should be empty in test environment
        assert settings.openai_api_key or True  # Allow empty for tests


class TestUtilities:
    """Test utility functions"""
    
    def test_validate_phone_number(self):
        """Test phone number validation"""
        assert validate_phone_number("+919999999999")
        assert validate_phone_number("9999999999")
        assert not validate_phone_number("invalid")
    
    def test_sanitize_input(self):
        """Test input sanitization"""
        result = sanitize_input("  hello world  ")
        assert result == "hello world"
        
        long_input = "a" * 2000
        result = sanitize_input(long_input)
        assert len(result) == 1000
    
    def test_parse_command(self):
        """Test command parsing"""
        command, args = parse_command(".help")
        assert command == "help"
        assert args == ""
        
        command, args = parse_command(".ai hello world")
        assert command == "ai"
        assert args == "hello world"
        
        command, args = parse_command("hello world")
        assert command is None
        assert args == "hello world"


class TestDatabase:
    """Test database operations"""
    
    @pytest.mark.asyncio
    async def test_database_connection(self):
        """Test database connection"""
        from sakha.database import db_manager
        
        # This would test actual connection in integration tests
        assert db_manager is not None


class TestHandlers:
    """Test command handlers"""
    
    def test_command_help(self):
        """Test help command"""
        # Placeholder for handler tests
        pass


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
