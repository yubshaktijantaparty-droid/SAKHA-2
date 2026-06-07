"""Enhanced AI Service with streaming and multi-model support for SAKHA AI Premium"""

import aiohttp
import json
from typing import Optional, AsyncGenerator, List, Dict, Any
from sakha.config import settings
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
    ) -> str:
        """Get response from AI model"""
        
        try:
            if "gpt" in model.lower():
                return await self._openai_request(message, model, system_prompt, temperature, max_tokens, chat_history)
            elif "claude" in model.lower():
                return await self._anthropic_request(message, model, system_prompt, temperature, max_tokens, chat_history)
            elif "gemini" in model.lower():
                return await self._gemini_request(message, model, system_prompt, temperature, max_tokens, chat_history)
            elif "deepseek" in model.lower():
                return await self._deepseek_request(message, model, system_prompt, temperature, max_tokens, chat_history)
            else:
                raise ValueError(f"Unsupported model: {model}")
        except Exception as e:
            logger.error(f"Error getting response from {model}: {e}")
            raise

    async def stream_response(
        self,
        message: str,
        model: str = "gpt-4o",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> AsyncGenerator[str, None]:
        """Stream response from AI model"""
        
        try:
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
        except Exception as e:
            logger.error(f"Error streaming response from {model}: {e}")
            yield f"Error: {str(e)}"

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
        """Make request to OpenAI"""
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

            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    raise Exception(f"OpenAI error: {error}")
                
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
        """Stream response from OpenAI"""
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

            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    raise Exception(f"OpenAI error: {error}")
                
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
        """Make request to Anthropic (Claude)"""
        async with aiohttp.ClientSession() as session:
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
        """Stream response from Anthropic (Claude)"""
        async with aiohttp.ClientSession() as session:
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
        """Make request to Google Gemini"""
        async with aiohttp.ClientSession() as session:
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
        """Stream response from Google Gemini"""
        async with aiohttp.ClientSession() as session:
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
        """Make request to DeepSeek"""
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

            async with session.post(
                "https://api.deepseek.com/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    raise Exception(f"DeepSeek error: {error}")
                
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
        """Stream response from DeepSeek"""
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

            async with session.post(
                "https://api.deepseek.com/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    raise Exception(f"DeepSeek error: {error}")
                
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
