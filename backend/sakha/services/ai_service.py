"""Enhanced AI Service with streaming and multi-model support for SAKHA AI Premium"""

import aiohttp
import json
from typing import Optional, AsyncGenerator, List, Dict, Any
from sakha.config import settings
from sakha.services.local_ai import local_ai_service
import logging

logger = logging.getLogger(__name__)


class AIService:
    """AI Service with support for multiple providers and streaming"""

    def __init__(self):
        self.openai_api_key = settings.OPENAI_API_KEY
        self.anthropic_api_key = settings.ANTHROPIC_API_KEY
        self.gemini_api_key = settings.GEMINI_API_KEY
        self.deepseek_api_key = settings.DEEPSEEK_API_KEY
        self.openrouter_api_key = settings.OPENROUTER_API_KEY
        self.timeout = settings.AI_TIMEOUT

    async def get_response(
        self,
        message: str,
        model: str = "gpt-4o",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        chat_history: Optional[List[Dict[str, str]]] = None,
        response_length: str = "medium",
        deep_thinking: bool = False,
    ) -> str:
        """Get response from AI model"""
        
        try:
            logger.info(f"get_response called with model: {model}, response_length: {response_length}, deep_thinking: {deep_thinking}")
            
            # Check if any API keys are available
            has_any_key = self.openai_api_key or self.anthropic_api_key or self.gemini_api_key or self.deepseek_api_key or self.openrouter_api_key
            
            # Use local AI if no real API keys available
            if not has_any_key:
                logger.info(f"No API keys available, using local AI service")
                # Convert response_length to expected format
                length_map = {"short": "short", "medium": "medium", "long": "long", "variable": "medium"}
                return await local_ai_service.get_response(
                    message,
                    response_length=length_map.get(response_length, "medium"),
                    deep_thinking=deep_thinking
                )
            
            if "gpt" in model.lower():
                logger.info(f"OpenAI API key available, making request")
                return await self._openai_request(message, model, system_prompt, temperature, max_tokens, chat_history)
            elif "claude" in model.lower():
                return await self._anthropic_request(message, model, system_prompt, temperature, max_tokens, chat_history)
            elif "gemini" in model.lower():
                return await self._gemini_request(message, model, system_prompt, temperature, max_tokens, chat_history)
            elif "deepseek" in model.lower():
                return await self._deepseek_request(message, model, system_prompt, temperature, max_tokens, chat_history)
            else:
                # Fallback to local AI
                logger.warning(f"Unsupported model: {model}, using local AI")
                length_map = {"short": "short", "medium": "medium", "long": "long", "variable": "medium"}
                return await local_ai_service.get_response(
                    message,
                    response_length=length_map.get(response_length, "medium"),
                    deep_thinking=deep_thinking
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
        model: str = "gpt-4o",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        chat_history: Optional[List[Dict[str, str]]] = None,
        response_length: str = "medium",
        deep_thinking: bool = False,
    ) -> AsyncGenerator[str, None]:
        """Stream response from AI model"""
        
        try:
            # Check if any API keys are available
            has_any_key = self.openai_api_key or self.anthropic_api_key or self.gemini_api_key or self.deepseek_api_key or self.openrouter_api_key
            
            # Use local AI if no real API keys available
            if not has_any_key:
                logger.info(f"No API keys available, using local AI stream service")
                length_map = {"short": "short", "medium": "medium", "long": "long", "variable": "medium"}
                async for chunk in local_ai_service.stream_response(
                    message,
                    response_length=length_map.get(response_length, "medium"),
                    deep_thinking=deep_thinking
                ):
                    yield chunk
                return
            
            if "gpt" in model.lower():
                async for chunk in self._openai_stream(message, model, system_prompt, temperature, max_tokens, chat_history):
                    yield chunk
            elif "claude" in model.lower():
                async for chunk in self._anthropic_stream(message, model, system_prompt, temperature, max_tokens, chat_history):
                    yield chunk
            elif "gemini" in model.lower():
                async for chunk in self._gemini_stream(message, model, system_prompt, temperature, max_tokens, chat_history):
                    yield chunk
            elif "deepseek" in model.lower():
                async for chunk in self._deepseek_stream(message, model, system_prompt, temperature, max_tokens, chat_history):
                    yield chunk
            else:
                # Fallback to local AI
                logger.warning(f"Unsupported model: {model}, using local AI stream")
                length_map = {"short": "short", "medium": "medium", "long": "long", "variable": "medium"}
                async for chunk in local_ai_service.stream_response(
                    message,
                    response_length=length_map.get(response_length, "medium"),
                    deep_thinking=deep_thinking
                ):
                    yield chunk
        except Exception as e:
            logger.error(f"Error streaming response from {model}: {e}")
            # Fallback to local AI stream on error
            length_map = {"short": "short", "medium": "medium", "long": "long", "variable": "medium"}
            async for chunk in local_ai_service.stream_response(
                message,
                response_length=length_map.get(response_length, "medium"),
                deep_thinking=deep_thinking
            ):
                yield chunk

    # OpenAI Methods
    async def _openai_request(
        self,
        message: str,
        model: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """Make request to OpenAI or OpenRouter"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json",
            }

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            if chat_history:
                messages.extend(chat_history)
            
            messages.append({"role": "user", "content": message})

            data = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }

            # Detect if using OpenRouter (keys start with "sk-or-v1-")
            is_openrouter = self.openai_api_key.startswith("sk-or-v1-")
            api_url = "https://openrouter.ai/api/v1/chat/completions" if is_openrouter else "https://api.openai.com/v1/chat/completions"
            
            if is_openrouter:
                headers["HTTP-Referer"] = "https://sakha.ai"
                headers["X-Title"] = "SAKHA AI"

            async with session.post(
                api_url,
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    raise Exception(f"OpenAI/OpenRouter error: {error}")
                
                result = await response.json()
                return result["choices"][0]["message"]["content"]

    async def _openai_stream(
        self,
        message: str,
        model: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> AsyncGenerator[str, None]:
        """Stream response from OpenAI or OpenRouter"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json",
            }

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            if chat_history:
                messages.extend(chat_history)
            
            messages.append({"role": "user", "content": message})

            data = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True,
            }

            # Detect if using OpenRouter (keys start with "sk-or-v1-")
            is_openrouter = self.openai_api_key.startswith("sk-or-v1-")
            api_url = "https://openrouter.ai/api/v1/chat/completions" if is_openrouter else "https://api.openai.com/v1/chat/completions"
            
            if is_openrouter:
                headers["HTTP-Referer"] = "https://sakha.ai"
                headers["X-Title"] = "SAKHA AI"

            async with session.post(
                api_url,
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    raise Exception(f"OpenAI/OpenRouter error: {error}")
                
                async for line in response.content:
                    line = line.decode("utf-8").strip()
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            json_data = json.loads(data)
                            if "choices" in json_data:
                                delta = json_data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                        except json.JSONDecodeError:
                            continue

    # Anthropic/Claude Methods
    async def _anthropic_request(
        self,
        message: str,
        model: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """Make request to Anthropic (Claude) or OpenRouter"""
        async with aiohttp.ClientSession() as session:
            # Detect if using OpenRouter (keys start with "sk-or-v1-")
            is_openrouter = self.anthropic_api_key.startswith("sk-or-v1-")
            
            if is_openrouter:
                # Use OpenAI-compatible format for OpenRouter
                headers = {
                    "Authorization": f"Bearer {self.anthropic_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://sakha.ai",
                    "X-Title": "SAKHA AI",
                }

                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                
                if chat_history:
                    messages.extend(chat_history)
                
                messages.append({"role": "user", "content": message})

                data = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }

                url = "https://openrouter.ai/api/v1/chat/completions"
                
                async with session.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as response:
                    if response.status != 200:
                        error = await response.text()
                        raise Exception(f"OpenRouter error: {error}")
                    
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
            else:
                # Use official Anthropic API
                headers = {
                    "x-api-key": self.anthropic_api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                }

                messages = []
                if chat_history:
                    messages.extend(chat_history)
                
                messages.append({"role": "user", "content": message})

                data = {
                    "model": model,
                    "max_tokens": max_tokens,
                    "messages": messages,
                    "temperature": temperature,
                }
                
                if system_prompt:
                    data["system"] = system_prompt

                async with session.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as response:
                    if response.status != 200:
                        error = await response.text()
                        raise Exception(f"Anthropic error: {error}")
                    
                    result = await response.json()
                    return result["content"][0]["text"]

    async def _anthropic_stream(
        self,
        message: str,
        model: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> AsyncGenerator[str, None]:
        """Stream response from Anthropic (Claude) or OpenRouter"""
        async with aiohttp.ClientSession() as session:
            # Detect if using OpenRouter (keys start with "sk-or-v1-")
            is_openrouter = self.anthropic_api_key.startswith("sk-or-v1-")
            
            if is_openrouter:
                # Use OpenAI-compatible format for OpenRouter
                headers = {
                    "Authorization": f"Bearer {self.anthropic_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://sakha.ai",
                    "X-Title": "SAKHA AI",
                }

                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                
                if chat_history:
                    messages.extend(chat_history)
                
                messages.append({"role": "user", "content": message})

                data = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": True,
                }

                url = "https://openrouter.ai/api/v1/chat/completions"
                
                async with session.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as response:
                    if response.status != 200:
                        error = await response.text()
                        raise Exception(f"OpenRouter error: {error}")
                    
                    async for line in response.content:
                        line = line.decode("utf-8").strip()
                        if line.startswith("data: "):
                            data = line[6:]
                            if data == "[DONE]":
                                break
                            try:
                                json_data = json.loads(data)
                                if "choices" in json_data:
                                    delta = json_data["choices"][0].get("delta", {})
                                    if "content" in delta:
                                        yield delta["content"]
                            except json.JSONDecodeError:
                                continue
            else:
                # Use official Anthropic API
                headers = {
                    "x-api-key": self.anthropic_api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                }

                messages = []
                if chat_history:
                    messages.extend(chat_history)
                
                messages.append({"role": "user", "content": message})

                data = {
                    "model": model,
                    "max_tokens": max_tokens,
                    "messages": messages,
                    "temperature": temperature,
                    "stream": True,
                }
                
                if system_prompt:
                    data["system"] = system_prompt

                async with session.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as response:
                    if response.status != 200:
                        error = await response.text()
                        raise Exception(f"Anthropic error: {error}")
                    
                    async for line in response.content:
                        line = line.decode("utf-8").strip()
                        if line.startswith("data: "):
                            data = line[6:]
                            try:
                                json_data = json.loads(data)
                                if json_data.get("type") == "content_block_delta":
                                    delta = json_data.get("delta", {})
                                    if delta.get("type") == "text_delta":
                                        yield delta.get("text", "")
                            except json.JSONDecodeError:
                                continue

    # Google Gemini Methods
    async def _gemini_request(
        self,
        message: str,
        model: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """Make request to Google Gemini or OpenRouter"""
        async with aiohttp.ClientSession() as session:
            # Detect if using OpenRouter (keys start with "sk-or-v1-")
            is_openrouter = self.gemini_api_key.startswith("sk-or-v1-")
            
            if is_openrouter:
                # Use OpenAI-compatible format for OpenRouter
                headers = {
                    "Authorization": f"Bearer {self.gemini_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://sakha.ai",
                    "X-Title": "SAKHA AI",
                }

                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                
                if chat_history:
                    messages.extend(chat_history)
                
                messages.append({"role": "user", "content": message})

                data = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }

                url = "https://openrouter.ai/api/v1/chat/completions"
                
                async with session.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as response:
                    if response.status != 200:
                        error = await response.text()
                        raise Exception(f"OpenRouter error: {error}")
                    
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
            else:
                # Use official Google API
                headers = {
                    "Content-Type": "application/json",
                }

                contents = []
                
                if chat_history:
                    for msg in chat_history:
                        contents.append({
                            "role": msg["role"],
                            "parts": [{"text": msg["content"]}]
                        })
                
                contents.append({
                    "role": "user",
                    "parts": [{"text": message}]
                })

                data = {
                    "contents": contents,
                    "generationConfig": {
                        "temperature": temperature,
                        "maxOutputTokens": max_tokens,
                    }
                }
                
                if system_prompt:
                    data["systemInstruction"] = {"parts": [{"text": system_prompt}]}

                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.gemini_api_key}"
                
                async with session.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as response:
                    if response.status != 200:
                        error = await response.text()
                        raise Exception(f"Gemini error: {error}")
                    
                    result = await response.json()
                    return result["candidates"][0]["content"]["parts"][0]["text"]

    async def _gemini_stream(
        self,
        message: str,
        model: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> AsyncGenerator[str, None]:
        """Stream response from Google Gemini or OpenRouter"""
        async with aiohttp.ClientSession() as session:
            # Detect if using OpenRouter (keys start with "sk-or-v1-")
            is_openrouter = self.gemini_api_key.startswith("sk-or-v1-")
            
            if is_openrouter:
                # Use OpenAI-compatible format for OpenRouter
                headers = {
                    "Authorization": f"Bearer {self.gemini_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://sakha.ai",
                    "X-Title": "SAKHA AI",
                }

                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                
                if chat_history:
                    messages.extend(chat_history)
                
                messages.append({"role": "user", "content": message})

                data = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": True,
                }

                url = "https://openrouter.ai/api/v1/chat/completions"
                
                async with session.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as response:
                    if response.status != 200:
                        error = await response.text()
                        raise Exception(f"OpenRouter error: {error}")
                    
                    async for line in response.content:
                        line = line.decode("utf-8").strip()
                        if line.startswith("data: "):
                            data = line[6:]
                            if data == "[DONE]":
                                break
                            try:
                                json_data = json.loads(data)
                                if "choices" in json_data:
                                    delta = json_data["choices"][0].get("delta", {})
                                    if "content" in delta:
                                        yield delta["content"]
                            except json.JSONDecodeError:
                                continue
            else:
                # Use official Google API
                headers = {
                    "Content-Type": "application/json",
                }

                contents = []
                
                if chat_history:
                    for msg in chat_history:
                        contents.append({
                            "role": msg["role"],
                            "parts": [{"text": msg["content"]}]
                        })
                
                contents.append({
                    "role": "user",
                    "parts": [{"text": message}]
                })

                data = {
                    "contents": contents,
                    "generationConfig": {
                        "temperature": temperature,
                        "maxOutputTokens": max_tokens,
                    }
                }
                
                if system_prompt:
                    data["systemInstruction"] = {"parts": [{"text": system_prompt}]}

                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:streamGenerateContent?alt=sse&key={self.gemini_api_key}"
                
                async with session.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as response:
                    if response.status != 200:
                        error = await response.text()
                        raise Exception(f"Gemini error: {error}")
                    
                    async for line in response.content:
                        line = line.decode("utf-8").strip()
                        if line.startswith("data: "):
                            data = line[6:]
                            try:
                                json_data = json.loads(data)
                                if "candidates" in json_data:
                                    candidate = json_data["candidates"][0]
                                    if "content" in candidate:
                                        for part in candidate["content"]["parts"]:
                                            if "text" in part:
                                                yield part["text"]
                            except json.JSONDecodeError:
                                continue

    # DeepSeek Methods
    async def _deepseek_request(
        self,
        message: str,
        model: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """Make request to DeepSeek or OpenRouter"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json",
            }

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            if chat_history:
                messages.extend(chat_history)
            
            messages.append({"role": "user", "content": message})

            data = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }

            # Detect if using OpenRouter (keys start with "sk-or-v1-")
            is_openrouter = self.deepseek_api_key.startswith("sk-or-v1-")
            api_url = "https://openrouter.ai/api/v1/chat/completions" if is_openrouter else "https://api.deepseek.com/chat/completions"
            
            if is_openrouter:
                headers["HTTP-Referer"] = "https://sakha.ai"
                headers["X-Title"] = "SAKHA AI"

            async with session.post(
                api_url,
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    raise Exception(f"DeepSeek/OpenRouter error: {error}")
                
                result = await response.json()
                return result["choices"][0]["message"]["content"]

    async def _deepseek_stream(
        self,
        message: str,
        model: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> AsyncGenerator[str, None]:
        """Stream response from DeepSeek or OpenRouter"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json",
            }

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            if chat_history:
                messages.extend(chat_history)
            
            messages.append({"role": "user", "content": message})

            data = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True,
            }

            # Detect if using OpenRouter (keys start with "sk-or-v1-")
            is_openrouter = self.deepseek_api_key.startswith("sk-or-v1-")
            api_url = "https://openrouter.ai/api/v1/chat/completions" if is_openrouter else "https://api.deepseek.com/chat/completions"
            
            if is_openrouter:
                headers["HTTP-Referer"] = "https://sakha.ai"
                headers["X-Title"] = "SAKHA AI"

            async with session.post(
                api_url,
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    raise Exception(f"DeepSeek/OpenRouter error: {error}")
                
                async for line in response.content:
                    line = line.decode("utf-8").strip()
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            json_data = json.loads(data)
                            if "choices" in json_data:
                                delta = json_data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                        except json.JSONDecodeError:
                            continue

    def _get_demo_response(self, message: str) -> str:
        """Return a demo response when API keys are not configured"""
        responses = {
            "hi": "Hello! I'm SakhaAI, your premium AI assistant. How can I help you today?",
            "hello": "Hi there! Welcome to SakhaAI. What would you like to chat about?",
            "how are you": "I'm doing great! Thanks for asking. I'm ready to help with whatever you need.",
            "thanks": "You're welcome! Feel free to ask me anything.",
            "bye": "Goodbye! Thanks for using SakhaAI. See you soon!",
        }
        
        lower_msg = message.lower().strip()
        if lower_msg in responses:
            return responses[lower_msg]
        
        return f"Thanks for your message: '{message}'. I'm currently in demo mode. To use real AI, configure API keys (OpenAI, Gemini, DeepSeek, etc)."
