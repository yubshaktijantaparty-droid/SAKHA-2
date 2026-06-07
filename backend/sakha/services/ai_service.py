"""Enhanced AI Service with OpenRouter multi-model support for SAKHA AI Premium"""

import aiohttp
import json
from typing import Optional, AsyncGenerator, List, Dict, Any
from sakha.config import settings
from sakha.services.local_ai import local_ai_service
import logging
import os

logger = logging.getLogger(__name__)


class AIService:
    """AI Service with OpenRouter multi-model support and key rotation"""

    def __init__(self):
        self.openrouter_api_keys = settings.OPENROUTER_API_KEYS  # List of available keys
        self.openrouter_api_key = settings.OPENROUTER_API_KEY  # Current/default key
        self.openai_api_key = settings.OPENAI_API_KEY
        self.gemini_api_key = settings.GEMINI_API_KEY
        self.deepseek_api_key = settings.DEEPSEEK_API_KEY
        self.timeout = settings.AI_TIMEOUT
        self.current_key_index = 0  # Track which key we're currently using
        
        # Log available API keys on init
        logger.info(f"✓ OpenRouter API Keys available: {len(self.openrouter_api_keys)} keys")
        for i, key in enumerate(self.openrouter_api_keys):
            key_preview = key[:20] + "..." if len(key) > 20 else key
            logger.info(f"  Key {i+1}: {key_preview}")
        logger.info(f"✓ OpenAI API Key available: {bool(self.openai_api_key)}")
        logger.info(f"✓ Gemini API Key available: {bool(self.gemini_api_key)}")
        logger.info(f"✓ DeepSeek API Key available: {bool(self.deepseek_api_key)}")
        
        # Model mappings for OpenRouter (using real available models)
        self.model_mappings = {
            "sakha-5.0": "openai/gpt-4-turbo",  # Best quality model
            "nemotron-3-ultra": "openai/gpt-4-turbo",
            "nemotron-3-super": "openai/gpt-4-turbo",
            "nemotron-3-nano": "openai/gpt-3.5-turbo",
            "qwen3-coder": "openai/gpt-4-turbo",  # Code generation
            "gpt-4o": "openai/gpt-4-turbo",
            "gpt-4": "openai/gpt-4-turbo",
            "gpt-3.5": "openai/gpt-3.5-turbo",
            "deepseek": "openai/gpt-3.5-turbo",
            "claude": "anthropic/claude-opus-4",  # Claude model
        }

    async def get_response(
        self,
        message: str,
        model: str = "sakha-5.0",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,  # Reduced from 2048 to stay within OpenRouter credit limits
        chat_history: Optional[List[Dict[str, str]]] = None,
        response_length: str = "medium",
        deep_thinking: bool = False,
    ) -> str:
        """Get response from AI model using OpenRouter with key rotation"""
        
        try:
            logger.info(f"get_response called with model: {model}, response_length: {response_length}, deep_thinking: {deep_thinking}")
            
            # Check if we have OpenRouter API keys
            if not self.openrouter_api_keys:
                logger.warning(f"No OpenRouter API keys available, falling back to local AI")
                length_map = {"short": "short", "medium": "medium", "long": "long", "variable": "medium"}
                return await local_ai_service.get_response(
                    message,
                    response_length=length_map.get(response_length, "medium"),
                    deep_thinking=deep_thinking
                )
            
            logger.info(f"Using OpenRouter API for model: {model}")
            return await self._openrouter_request(
                message, 
                model, 
                system_prompt, 
                temperature, 
                max_tokens, 
                chat_history,
                deep_thinking
            )
            
        except Exception as e:
            logger.error(f"Error getting response from {model}: {e}", exc_info=True)
            # Fallback to local AI on error
            length_map = {"short": "short", "medium": "medium", "long": "long", "variable": "medium"}
            return await local_ai_service.get_response(
                message,
                response_length=length_map.get(response_length, "medium"),
                deep_thinking=deep_thinking
            )

    async def stream_response(
        self,
        message: str,
        model: str = "sakha-5.0",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,  # Reduced from 2048 to stay within OpenRouter credit limits
        chat_history: Optional[List[Dict[str, str]]] = None,
        response_length: str = "medium",
        deep_thinking: bool = False,
    ) -> AsyncGenerator[str, None]:
        """Stream response from AI model using OpenRouter"""
        
        try:
            logger.info(f"stream_response called with model: {model}")
            
            # Check if we have OpenRouter API key
            if not self.openrouter_api_key:
                logger.warning(f"No OpenRouter API key available, falling back to local AI stream")
                length_map = {"short": "short", "medium": "medium", "long": "long", "variable": "medium"}
                async for chunk in local_ai_service.stream_response(
                    message,
                    response_length=length_map.get(response_length, "medium"),
                    deep_thinking=deep_thinking
                ):
                    yield chunk
                return
            
            logger.info(f"Streaming OpenRouter with model: {model}")
            async for chunk in self._openrouter_stream(
                message, 
                model, 
                system_prompt, 
                temperature, 
                max_tokens, 
                chat_history,
                deep_thinking
            ):
                yield chunk
                    
        except Exception as e:
            logger.error(f"Error streaming response from {model}: {e}", exc_info=True)
            # Fallback to local AI stream on error
            length_map = {"short": "short", "medium": "medium", "long": "long", "variable": "medium"}
            async for chunk in local_ai_service.stream_response(
                message,
                response_length=length_map.get(response_length, "medium"),
                deep_thinking=deep_thinking
            ):
                yield chunk

    async def _openrouter_request(
        self,
        message: str,
        model: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        chat_history: Optional[List[Dict[str, str]]] = None,
        deep_thinking: bool = False,
    ) -> str:
        """Make request to OpenRouter API with key rotation on 402 errors"""
        
        # Try each available key
        for key_index, api_key in enumerate(self.openrouter_api_keys):
            try:
                async with aiohttp.ClientSession() as session:
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://sakha.ai",
                        "X-Title": "SAKHA AI Premium",
                    }

                    # Map model name to OpenRouter model ID
                    openrouter_model = self.model_mappings.get(model.lower(), "openai/gpt-3.5-turbo")
                    
                    # Build messages
                    messages = []
                    
                    # Add system prompt with deep thinking if enabled
                    if system_prompt:
                        messages.append({"role": "system", "content": system_prompt})
                    elif deep_thinking:
                        dt_prompt = "You are an expert AI assistant. Think deeply and thoroughly about the question. Provide comprehensive, nuanced, and insightful responses. Consider multiple perspectives and implications."
                        messages.append({"role": "system", "content": dt_prompt})
                    else:
                        messages.append({"role": "system", "content": "You are SAKHA AI, a helpful and knowledgeable assistant. Provide clear, accurate, and helpful responses."})
                    
                    if chat_history:
                        messages.extend(chat_history)
                    
                    messages.append({"role": "user", "content": message})

                    data = {
                        "model": openrouter_model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": min(max_tokens, 1000),  # Cap at 1000 to stay within OpenRouter credits
                    }

                    logger.info(f"Trying OpenRouter request with key {key_index + 1}/{len(self.openrouter_api_keys)} - model: {openrouter_model}")
                    
                    async with session.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=data,
                        timeout=aiohttp.ClientTimeout(total=self.timeout),
                    ) as response:
                        if response.status == 402:
                            # Insufficient credits - try next key
                            error_text = await response.text()
                            logger.warning(f"Key {key_index + 1} insufficient credits: {error_text}")
                            if key_index < len(self.openrouter_api_keys) - 1:
                                logger.info(f"Rotating to next API key...")
                                continue
                            else:
                                # No more keys to try
                                logger.error(f"All API keys exhausted (insufficient credits)")
                                raise Exception(f"All OpenRouter API keys exhausted")
                        
                        if response.status != 200:
                            error_text = await response.text()
                            logger.error(f"OpenRouter API error: {response.status} - {error_text}")
                            raise Exception(f"OpenRouter error: {error_text}")
                        
                        result = await response.json()
                        if "choices" not in result or len(result["choices"]) == 0:
                            logger.error(f"Invalid OpenRouter response: {result}")
                            raise Exception("Invalid response from OpenRouter")
                        
                        response_text = result["choices"][0]["message"]["content"]
                        logger.info(f"✓ Got response from OpenRouter with key {key_index + 1} ({len(response_text)} chars)")
                        self.current_key_index = key_index  # Update current key index
                        return response_text
                    
            except Exception as e:
                logger.error(f"OpenRouter request with key {key_index + 1} failed: {e}")
                if key_index < len(self.openrouter_api_keys) - 1:
                    logger.info(f"Trying next API key...")
                    continue
                else:
                    logger.error(f"All OpenRouter API keys failed")
                    raise

    async def _openrouter_stream(
        self,
        message: str,
        model: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        chat_history: Optional[List[Dict[str, str]]] = None,
        deep_thinking: bool = False,
    ) -> AsyncGenerator[str, None]:
        """Stream response from OpenRouter API with key rotation on 402 errors"""
        
        # Try each available key
        for key_index, api_key in enumerate(self.openrouter_api_keys):
            try:
                async with aiohttp.ClientSession() as session:
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://sakha.ai",
                        "X-Title": "SAKHA AI Premium",
                    }

                    # Map model name to OpenRouter model ID
                    openrouter_model = self.model_mappings.get(model.lower(), "openai/gpt-3.5-turbo")
                    
                    # Build messages
                    messages = []
                    
                    # Add system prompt with deep thinking if enabled
                    if system_prompt:
                        messages.append({"role": "system", "content": system_prompt})
                    elif deep_thinking:
                        dt_prompt = "You are an expert AI assistant. Think deeply and thoroughly about the question. Provide comprehensive, nuanced, and insightful responses. Consider multiple perspectives and implications."
                        messages.append({"role": "system", "content": dt_prompt})
                    else:
                        messages.append({"role": "system", "content": "You are SAKHA AI, a helpful and knowledgeable assistant. Provide clear, accurate, and helpful responses."})
                    
                    if chat_history:
                        messages.extend(chat_history)
                    
                    messages.append({"role": "user", "content": message})

                    data = {
                        "model": openrouter_model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": min(max_tokens, 1000),  # Cap at 1000 to stay within OpenRouter credits
                        "stream": True,
                    }

                    logger.info(f"Streaming OpenRouter with key {key_index + 1}/{len(self.openrouter_api_keys)} - model: {openrouter_model}")
                    
                    async with session.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=data,
                        timeout=aiohttp.ClientTimeout(total=self.timeout),
                    ) as response:
                        if response.status == 402:
                            # Insufficient credits - try next key
                            error_text = await response.text()
                            logger.warning(f"Key {key_index + 1} insufficient credits: {error_text}")
                            if key_index < len(self.openrouter_api_keys) - 1:
                                logger.info(f"Rotating to next API key...")
                                continue
                            else:
                                # No more keys to try
                                logger.error(f"All API keys exhausted (insufficient credits)")
                                raise Exception(f"All OpenRouter API keys exhausted")
                        
                        if response.status != 200:
                            error_text = await response.text()
                            logger.error(f"OpenRouter API error: {response.status} - {error_text}")
                            raise Exception(f"OpenRouter error: {error_text}")
                        
                        async for line in response.content:
                            line = line.decode("utf-8").strip()
                            if not line or not line.startswith("data: "):
                                continue
                            
                            data_str = line[6:]
                            if data_str == "[DONE]":
                                break
                            
                            try:
                                json_data = json.loads(data_str)
                                if "choices" in json_data and len(json_data["choices"]) > 0:
                                    delta = json_data["choices"][0].get("delta", {})
                                    if "content" in delta and delta["content"]:
                                        yield delta["content"]
                            except json.JSONDecodeError:
                                continue
                        
                        # Successfully completed stream
                        self.current_key_index = key_index  # Update current key index
                        return
                        
            except Exception as e:
                logger.error(f"OpenRouter stream with key {key_index + 1} failed: {e}")
                if key_index < len(self.openrouter_api_keys) - 1:
                    logger.info(f"Trying next API key for stream...")
                    continue
                else:
                    logger.error(f"All OpenRouter API keys failed for stream")
                    raise



# Create singleton instance
ai_service = AIService()

