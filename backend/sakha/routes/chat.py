"""Chat Endpoints - With Database Persistence"""

from fastapi import APIRouter, HTTPException, Header, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import asyncio
import json

from sakha.services.ai_service import AIService
from sakha.services.database_service import db_service
from sakha.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
ai_service = AIService()


# ==================== MODELS ====================

class ChatMessage(BaseModel):
    """Chat message model"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    chat_id: Optional[str] = None
    user_id: Optional[str] = None
    model: Optional[str] = None
    system_prompt: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2000


class ChatResponse(BaseModel):
    """Chat response model"""
    chat_id: str
    message: str
    model: str
    timestamp: datetime


class CreateChatRequest(BaseModel):
    """Request to create new chat"""
    title: str
    user_id: str
    model: Optional[str] = "gpt-4o"


# ==================== ROUTES ====================

@router.post("/chat")
async def chat(request: ChatRequest, user_id: str = Header(None)):
    """Send a chat message with database persistence"""
    try:
        if not request.message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        user_id = user_id or request.user_id or "anonymous"
        model = request.model or settings.DEFAULT_AI_PROVIDER
        
        # Create chat if doesn't exist
        chat_id = request.chat_id
        if not chat_id:
            chat = await db_service.save_chat(user_id, "New Chat", model)
            chat_id = chat["_id"]
        
        # Save user message
        await db_service.save_message(
            chat_id=chat_id,
            user_id=user_id,
            role="user",
            content=request.message,
            model=model
        )
        
        # Get AI response
        response = await ai_service.get_response(
            message=request.message,
            model=model,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        
        # Save assistant message
        await db_service.save_message(
            chat_id=chat_id,
            user_id=user_id,
            role="assistant",
            content=response,
            model=model
        )
        
        logger.info(f"Chat message processed for user {user_id}")
        
        return ChatResponse(
            chat_id=chat_id,
            message=response,
            model=model,
            timestamp=datetime.utcnow(),
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest, user_id: str = Header(None)):
    """Stream chat response with database persistence"""
    try:
        if not request.message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        user_id = user_id or request.user_id or "anonymous"
        model = request.model or settings.DEFAULT_AI_PROVIDER
        
        # Create chat if doesn't exist
        chat_id = request.chat_id
        if not chat_id:
            chat = await db_service.save_chat(user_id, "New Chat", model)
            chat_id = chat["_id"]
        
        # Save user message
        await db_service.save_message(
            chat_id=chat_id,
            user_id=user_id,
            role="user",
            content=request.message,
            model=model
        )
        
        # Stream response from AI service
        async def response_generator():
            full_response = ""
            async for chunk in ai_service.stream_response(
                message=request.message,
                model=model,
                system_prompt=request.system_prompt,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            ):
                full_response += chunk
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            
            # Save complete assistant message
            await db_service.save_message(
                chat_id=chat_id,
                user_id=user_id,
                role="assistant",
                content=full_response,
                model=model
            )
        
        return StreamingResponse(response_generator(), media_type="text/event-stream")
        
    except Exception as e:
        logger.error(f"Error in chat stream endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/new")
async def create_new_chat(request: CreateChatRequest):
    """Create a new chat session"""
    try:
        chat = await db_service.save_chat(request.user_id, request.title, request.model)
        logger.info(f"New chat created: {chat['_id']}")
        return chat
        
    except Exception as e:
        logger.error(f"Error creating chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/{chat_id}/history")
async def get_chat_history(chat_id: str, limit: int = Query(100, ge=1, le=500)):
    """Get chat history with messages"""
    try:
        messages = await db_service.get_chat_messages(chat_id, limit)
        logger.info(f"Chat history retrieved: {len(messages)} messages")
        return {
            "chat_id": chat_id,
            "messages": messages,
            "count": len(messages)
        }
        
    except Exception as e:
        logger.error(f"Error retrieving chat history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/user/{user_id}")
async def get_user_chats(user_id: str, limit: int = Query(50, ge=1, le=100)):
    """Get all chats for a user"""
    try:
        chats = await db_service.get_user_chats(user_id, limit)
        logger.info(f"User chats retrieved for {user_id}: {len(chats)} chats")
        return {
            "user_id": user_id,
            "chats": chats,
            "count": len(chats)
        }
        
    except Exception as e:
        logger.error(f"Error retrieving user chats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/chat/{chat_id}/title")
async def update_chat_title(chat_id: str, new_title: str):
    """Update chat title"""
    try:
        if not new_title or len(new_title) < 1:
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        
        success = await db_service.update_chat_title(chat_id, new_title)
        return {"success": success, "chat_id": chat_id, "new_title": new_title}
        
    except Exception as e:
        logger.error(f"Error updating chat title: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/{chat_id}/delete")
async def delete_chat(chat_id: str):
    """Delete a chat and all messages"""
    try:
        success = await db_service.delete_chat(chat_id)
        return {"success": success, "status": "deleted", "chat_id": chat_id}
        
    except Exception as e:
        logger.error(f"Error deleting chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/{chat_id}/archive")
async def archive_chat(chat_id: str):
    """Archive a chat"""
    try:
        success = await db_service.archive_chat(chat_id)
        return {"success": success, "status": "archived", "chat_id": chat_id}
        
    except Exception as e:
        logger.error(f"Error archiving chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/models")
async def get_available_models():
    """Get list of available AI models"""
    return {
        "models": [
            {"id": "gpt-4o", "name": "OpenAI GPT-4o", "provider": "OpenAI", "available": bool(settings.OPENAI_API_KEY)},
            {"id": "deepseek-chat", "name": "DeepSeek Chat", "provider": "DeepSeek", "available": bool(settings.DEEPSEEK_API_KEY)},
            {"id": "gemini-2.5-flash", "name": "Google Gemini 2.5 Flash", "provider": "Google", "available": bool(settings.GEMINI_API_KEY)},
        ]
    }
