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
    """AI Service with OpenRouter multi-model support"""

    def __init__(self):
        self.openrouter_api_keys = settings.OPENROUTER_API_KEYS
        self.current_key_index = 0
        self.openai_api_key = settings.OPENAI_API_KEY
        self.gemini_api_key = settings.GEMINI_API_KEY
        self.deepseek_api_key = settings.DEEPSEEK_API_KEY
        self.timeout = settings.AI_TIMEOUT
        
        # Log available API keys on init
        logger.info(f"[OK] OpenRouter API Keys available: {len(self.openrouter_api_keys)} keys loaded")
        logger.info(f"[OK] OpenAI API Key available: {bool(self.openai_api_key)}")
        logger.info(f"[OK] Gemini API Key available: {bool(self.gemini_api_key)}")
        logger.info(f"[OK] DeepSeek API Key available: {bool(self.deepseek_api_key)}")
        
        # Model mappings for OpenRouter - Using openrouter/auto for reliable responses
        # openrouter/auto intelligently routes to the best available model
        self.model_mappings = {
            # ===== SAKHA-5.0 UNIFIED (Intelligent Router) =====
            "sakha-5.0": "openrouter/auto",
            
            # ===== NVIDIA NEMOTRON SERIES (Primary Text Generation) =====
            "nemotron-3-ultra": "openrouter/auto",
            "nemotron-3-ultra-550b": "openrouter/auto",
            "nemotron-3-super": "openrouter/auto",
            "nemotron-3-super-120b": "openrouter/auto",
            "nemotron-3-nano": "openrouter/auto",
            "nemotron-3-nano-omni": "openrouter/auto",
            "nemotron-3-nano-30b": "openrouter/auto",
            
            # ===== QWEN SERIES (Code Generation) =====
            "qwen-qwen3-coder": "openrouter/auto",
            "qwen3-coder": "openrouter/auto",
            "qwen-qwen3-plus": "openrouter/auto",
            "qwen3-plus": "openrouter/auto",
            
            # ===== POOLSIDE LAGUNA SERIES (Fast & Lightweight) =====
            "laguna-m": "openrouter/auto",
            "laguna-m-medium": "openrouter/auto",
            "laguna-xs": "openrouter/auto",
            "laguna-xs-extra-small": "openrouter/auto",
            
            # ===== MULTIMODAL MODELS =====
            # Video Processing
            "video-input-1": "openrouter/auto",
            "video-input-2": "openrouter/auto",
            "video-llava": "openrouter/auto",
            
            # Audio Processing
            "audio-input": "openrouter/auto",
            "audio-processing": "openrouter/auto",
            
            # Image Generation
            "image-output-1": "openrouter/auto",
            "image-output-2": "openrouter/auto",
            "image-generation": "openrouter/auto",
            
            # Embeddings
            "embed-output": "openrouter/auto",
            "embeddings": "openrouter/auto",
            
            # ===== LEGACY/FALLBACK MODELS =====
            "gpt-4o": "openrouter/auto",
            "gpt-4": "openrouter/auto",
            "gpt-3.5": "openrouter/auto",
            "deepseek": "openrouter/auto",
            "deepseek-chat": "openrouter/auto",
            "claude": "openrouter/auto",
            "claude-3.5-haiku": "openrouter/auto",
            "owl-alpha": "openrouter/auto",
            "openrouter-owl-alpha": "openrouter/auto",
        }

    def get_current_api_key(self) -> str:
        """Get current OpenRouter API key with rotation"""
        if not self.openrouter_api_keys:
            return ""
        key = self.openrouter_api_keys[self.current_key_index]
        return key
    
    def rotate_api_key(self):
        """Rotate to next API key when current one fails"""
        if self.openrouter_api_keys:
            self.current_key_index = (self.current_key_index + 1) % len(self.openrouter_api_keys)
            logger.info(f"Rotating API key to index {self.current_key_index}")
            return self.get_current_api_key()
        return ""

    async def get_response(
        self,
        message: str,
        model: str = "sakha-5.0",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,  # Optimized for free OpenRouter models
        chat_history: Optional[List[Dict[str, str]]] = None,
        response_length: str = "medium",
        deep_thinking: bool = False,
    ) -> str:
        """Get response from AI model using OpenRouter"""
        
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
        max_tokens: int = 500,  # Optimized for free OpenRouter models
        chat_history: Optional[List[Dict[str, str]]] = None,
        response_length: str = "medium",
        deep_thinking: bool = False,
    ) -> AsyncGenerator[str, None]:
        """Stream response from AI model using OpenRouter"""
        
        try:
            logger.info(f"stream_response called with model: {model}")
            
            # Check if we have OpenRouter API keys
            if not self.openrouter_api_keys:
                logger.warning(f"No OpenRouter API keys available, falling back to local AI stream")
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
        """Make request to OpenRouter API with automatic key rotation on 402 errors"""
        keys_tried = set()
        max_retries = len(self.openrouter_api_keys)
        
        for attempt in range(max_retries):
            try:
                current_key = self.get_current_api_key()
                
                # Avoid infinite loop if same key fails multiple times
                if current_key in keys_tried:
                    self.rotate_api_key()
                    continue
                
                keys_tried.add(current_key)
                logger.info(f"Attempt {attempt + 1}/{max_retries}: Using API key index {self.current_key_index}")
                
                async with aiohttp.ClientSession() as session:
                    headers = {
                        "Authorization": f"Bearer {current_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://sakha.ai",
                        "X-Title": "SAKHA AI Premium",
                    }

                    # Map model name to OpenRouter model ID (FREE tier models only)
                    openrouter_model = self.model_mappings.get(model.lower(), "openrouter/owl-alpha")  # Fallback to free OWL Alpha
                    
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
                        "max_tokens": min(max_tokens, 500),  # Optimized for free OpenRouter models
                    }

                    logger.info(f"Making OpenRouter request with model: {openrouter_model} using API key index {self.current_key_index}")
                    
                    async with session.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=data,
                        timeout=aiohttp.ClientTimeout(total=self.timeout),
                    ) as response:
                        if response.status == 402:
                            error_text = await response.text()
                            logger.warning(f"API key index {self.current_key_index} out of credits: {error_text}")
                            # Rotate to next key and retry
                            self.rotate_api_key()
                            continue
                        elif response.status != 200:
                            error_text = await response.text()
                            logger.error(f"OpenRouter API error: {response.status} - {error_text}")
                            self.rotate_api_key()
                            continue
                        
                        result = await response.json()
                        if "choices" not in result or len(result["choices"]) == 0:
                            logger.error(f"Invalid OpenRouter response: {result}")
                            self.rotate_api_key()
                            continue
                        
                        response_text = result["choices"][0]["message"]["content"]
                        logger.info(f"✓ Got response from OpenRouter ({len(response_text)} chars)")
                        return response_text
                        
            except Exception as e:
                logger.error(f"OpenRouter request attempt {attempt + 1} failed: {e}", exc_info=True)
                self.rotate_api_key()
                if attempt == max_retries - 1:
                    raise
        
        # If all keys fail, raise exception to trigger fallback
        raise Exception(f"All {max_retries} API keys failed")

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
        """Stream response from OpenRouter API with automatic key rotation on 402 errors"""
        keys_tried = set()
        max_retries = len(self.openrouter_api_keys)
        
        for attempt in range(max_retries):
            try:
                current_key = self.get_current_api_key()
                
                # Avoid infinite loop if same key fails multiple times
                if current_key in keys_tried:
                    self.rotate_api_key()
                    continue
                
                keys_tried.add(current_key)
                logger.info(f"Stream attempt {attempt + 1}/{max_retries}: Using API key index {self.current_key_index}")
                
                async with aiohttp.ClientSession() as session:
                    headers = {
                        "Authorization": f"Bearer {current_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://sakha.ai",
                        "X-Title": "SAKHA AI Premium",
                    }

                    # Map model name to OpenRouter model ID (FREE tier models only)
                    openrouter_model = self.model_mappings.get(model.lower(), "openrouter/owl-alpha")  # Fallback to free OWL Alpha
                    
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
                        "max_tokens": min(max_tokens, 500),  # Optimized for free OpenRouter models
                        "stream": True,
                    }

                    logger.info(f"Streaming OpenRouter with model: {openrouter_model} using API key index {self.current_key_index}")
                    
                    async with session.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=data,
                        timeout=aiohttp.ClientTimeout(total=self.timeout),
                    ) as response:
                        if response.status == 402:
                            error_text = await response.text()
                            logger.warning(f"Stream: API key index {self.current_key_index} out of credits: {error_text}")
                            self.rotate_api_key()
                            continue
                        elif response.status != 200:
                            error_text = await response.text()
                            logger.error(f"OpenRouter API stream error: {response.status} - {error_text}")
                            self.rotate_api_key()
                            continue
                        
                        async for line in response.content:
                            line = line.decode("utf-8").strip()
                            if not line or not line.startswith("data: "):
                                continue
                            
                            data_str = line[6:]
                            if data_str == "[DONE]":
                                return
                            
                            try:
                                json_data = json.loads(data_str)
                                if "choices" in json_data and len(json_data["choices"]) > 0:
                                    delta = json_data["choices"][0].get("delta", {})
                                    if "content" in delta and delta["content"]:
                                        yield delta["content"]
                            except json.JSONDecodeError:
                                continue
                        
                        # Stream completed successfully
                        return
                        
            except Exception as e:
                logger.error(f"OpenRouter stream attempt {attempt + 1} failed: {e}", exc_info=True)
                self.rotate_api_key()
                if attempt == max_retries - 1:
                    raise
        
        # If all keys fail, raise exception to trigger fallback
        raise Exception(f"All {max_retries} API keys failed for streaming")



# Create singleton instance
ai_service = AIService()

