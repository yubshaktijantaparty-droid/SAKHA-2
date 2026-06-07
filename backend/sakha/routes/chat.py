"""Chat Endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import asyncio

from sakha.services.ai_service import AIService
from sakha.config import settings

router = APIRouter()
ai_service = AIService()


class ChatMessage(BaseModel):
    """Chat message model"""

    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Chat request model"""

    message: str
    chat_id: Optional[str] = None
    model: Optional[str] = None  # openai, deepseek, gemini, openrouter
    system_prompt: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2000


class ChatResponse(BaseModel):
    """Chat response model"""

    chat_id: str
    message: str
    model: str
    timestamp: datetime


@router.post("/chat")
async def chat(request: ChatRequest):
    """Send a chat message and get AI response"""
    try:
        if not request.message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        model = request.model or settings.DEFAULT_AI_PROVIDER

        # Get AI response
        response = await ai_service.get_response(
            message=request.message,
            model=model,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        return ChatResponse(
            chat_id=request.chat_id or "new_chat",
            message=response,
            model=model,
            timestamp=datetime.utcnow(),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Stream chat response"""
    try:
        if not request.message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        model = request.model or settings.DEFAULT_AI_PROVIDER

        # Stream response from AI service
        return await ai_service.stream_response(
            message=request.message,
            model=model,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/models")
async def get_available_models():
    """Get list of available AI models"""
    return {
        "models": [
            {"id": "openai", "name": "OpenAI GPT-4", "provider": "OpenAI"},
            {"id": "deepseek", "name": "DeepSeek Chat", "provider": "DeepSeek"},
            {"id": "gemini", "name": "Google Gemini", "provider": "Google"},
            {"id": "openrouter", "name": "OpenRouter", "provider": "OpenRouter"},
        ]
    }


@router.get("/chat/history/{chat_id}")
async def get_chat_history(chat_id: str):
    """Get chat history"""
    # TODO: Implement chat history retrieval from database
    return {"chat_id": chat_id, "messages": []}


@router.post("/chat/{chat_id}/delete")
async def delete_chat(chat_id: str):
    """Delete a chat"""
    # TODO: Implement chat deletion
    return {"status": "deleted", "chat_id": chat_id}
