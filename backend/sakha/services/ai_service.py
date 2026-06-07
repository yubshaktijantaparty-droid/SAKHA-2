"""AI Service - Multi-model support"""

import aiohttp
import json
from typing import Optional, AsyncGenerator
from sakha.config import settings
import logging

logger = logging.getLogger(__name__)


class AIService:
    """AI Service with support for multiple providers"""

    def __init__(self):
        self.openai_api_key = settings.OPENAI_API_KEY
        self.deepseek_api_key = settings.DEEPSEEK_API_KEY
        self.gemini_api_key = settings.GEMINI_API_KEY
        self.timeout = settings.AI_TIMEOUT

    async def get_response(
        self,
        message: str,
        model: str = "openai",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Get response from AI model"""

        if model == "openai":
            return await self._openai_request(
                message, system_prompt, temperature, max_tokens
            )
        elif model == "deepseek":
            return await self._deepseek_request(
                message, system_prompt, temperature, max_tokens
            )
        elif model == "gemini":
            return await self._gemini_request(
                message, system_prompt, temperature, max_tokens
            )
        else:
            raise ValueError(f"Unsupported model: {model}")

    async def stream_response(
        self,
        message: str,
        model: str = "openai",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> AsyncGenerator[str, None]:
        """Stream response from AI model"""

        if model == "openai":
            async for chunk in self._openai_stream(
                message, system_prompt, temperature, max_tokens
            ):
                yield chunk
        elif model == "deepseek":
            async for chunk in self._deepseek_stream(
                message, system_prompt, temperature, max_tokens
            ):
                yield chunk
        elif model == "gemini":
            async for chunk in self._gemini_stream(
                message, system_prompt, temperature, max_tokens
            ):
                yield chunk

    async def _openai_request(
        self,
        message: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Make request to OpenAI"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json",
                }

                data = {
                    "model": settings.OPENAI_MODEL,
                    "messages": [
                        *([{"role": "system", "content": system_prompt}] if system_prompt else []),
                        {"role": "user", "content": message},
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }

                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=self.timeout,
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        return result["choices"][0]["message"]["content"]
                    else:
                        error = await resp.text()
                        raise Exception(f"OpenAI API error: {error}")
        except Exception as e:
            logger.error(f"OpenAI request failed: {e}")
            raise

    async def _openai_stream(
        self,
        message: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> AsyncGenerator[str, None]:
        """Stream from OpenAI"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json",
                }

                data = {
                    "model": settings.OPENAI_MODEL,
                    "messages": [
                        *([{"role": "system", "content": system_prompt}] if system_prompt else []),
                        {"role": "user", "content": message},
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": True,
                }

                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=self.timeout,
                ) as resp:
                    async for line in resp.content:
                        line = line.decode("utf-8").strip()
                        if line.startswith("data: "):
                            try:
                                chunk_data = json.loads(line[6:])
                                if chunk_data["choices"][0].get("delta", {}).get("content"):
                                    yield chunk_data["choices"][0]["delta"]["content"]
                            except json.JSONDecodeError:
                                pass
        except Exception as e:
            logger.error(f"OpenAI stream failed: {e}")
            raise

    async def _deepseek_request(
        self,
        message: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Make request to DeepSeek"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.deepseek_api_key}",
                    "Content-Type": "application/json",
                }

                data = {
                    "model": settings.DEEPSEEK_MODEL,
                    "messages": [
                        *([{"role": "system", "content": system_prompt}] if system_prompt else []),
                        {"role": "user", "content": message},
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }

                async with session.post(
                    "https://api.deepseek.com/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=self.timeout,
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        return result["choices"][0]["message"]["content"]
                    else:
                        error = await resp.text()
                        raise Exception(f"DeepSeek API error: {error}")
        except Exception as e:
            logger.error(f"DeepSeek request failed: {e}")
            raise

    async def _deepseek_stream(
        self,
        message: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> AsyncGenerator[str, None]:
        """Stream from DeepSeek"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.deepseek_api_key}",
                    "Content-Type": "application/json",
                }

                data = {
                    "model": settings.DEEPSEEK_MODEL,
                    "messages": [
                        *([{"role": "system", "content": system_prompt}] if system_prompt else []),
                        {"role": "user", "content": message},
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": True,
                }

                async with session.post(
                    "https://api.deepseek.com/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=self.timeout,
                ) as resp:
                    async for line in resp.content:
                        line = line.decode("utf-8").strip()
                        if line.startswith("data: "):
                            try:
                                chunk_data = json.loads(line[6:])
                                if chunk_data["choices"][0].get("delta", {}).get("content"):
                                    yield chunk_data["choices"][0]["delta"]["content"]
                            except json.JSONDecodeError:
                                pass
        except Exception as e:
            logger.error(f"DeepSeek stream failed: {e}")
            raise

    async def _gemini_request(
        self,
        message: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Make request to Google Gemini"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Content-Type": "application/json"}

                data = {
                    "contents": [
                        {
                            "parts": [{"text": message}],
                        }
                    ],
                    "generationConfig": {
                        "temperature": temperature,
                        "maxOutputTokens": max_tokens,
                    },
                }

                url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={self.gemini_api_key}"

                async with session.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=self.timeout,
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        return result["candidates"][0]["content"]["parts"][0]["text"]
                    else:
                        error = await resp.text()
                        raise Exception(f"Gemini API error: {error}")
        except Exception as e:
            logger.error(f"Gemini request failed: {e}")
            raise

    async def _gemini_stream(
        self,
        message: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> AsyncGenerator[str, None]:
        """Stream from Google Gemini"""
        # Gemini doesn't support streaming in the same way, so we'll return the full response
        response = await self._gemini_request(message, system_prompt, temperature, max_tokens)
        # Simulate streaming by yielding chunks
        for word in response.split(" "):
            yield word + " "
