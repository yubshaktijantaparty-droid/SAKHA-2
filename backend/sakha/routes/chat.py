"""Chat Endpoints - With Database Persistence and Sakha-5.0 Integration"""

from fastapi import APIRouter, HTTPException, Header, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import asyncio
import json

from sakha.services.ai_service import AIService
from sakha.services.database_service import db_service
from sakha.services.model_router import get_model_selector
from sakha.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
ai_service = AIService()
model_selector = get_model_selector()


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
    deep_thinking: Optional[bool] = False  # Enable deep thinking mode


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
    """Send a chat message with Sakha-5.0 intelligent routing and failover"""
    try:
        if not request.message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        user_id = user_id or request.user_id or "anonymous"
        
        # Use model router with failover to select best model for this message
        try:
            model_profile, task_type, routing_reason, response_length = await model_selector.get_model_with_failover(
                request.message,
                user_preference=request.model,
                priority="quality",
                deep_thinking=request.deep_thinking or False
            )
        except Exception as e:
            logger.error(f"Error in model selection: {e}")
            model_profile, task_type, routing_reason, response_length = model_selector.get_model_for_message(
                request.message,
                user_preference=request.model,
                priority="quality",
                deep_thinking=request.deep_thinking or False
            )
        
        if not model_profile:
            # Fallback if no model available
            logger.warning("No suitable model found, using fallback response")
            return ChatResponse(
                chat_id="fallback",
                message="System: All AI models are currently unavailable. Please try again later.",
                model="sakha-5.0",
                timestamp=datetime.utcnow(),
            )
        
        model_id = model_profile.model_id
        
        # Create chat if doesn't exist
        chat_id = request.chat_id
        if not chat_id:
            chat = await db_service.save_chat(user_id, "New Chat", "sakha-5.0")
            chat_id = chat["_id"]
        
        # Save user message
        await db_service.save_message(
            chat_id=chat_id,
            user_id=user_id,
            role="user",
            content=request.message,
            model="sakha-5.0"
        )
        
        # Prepare system prompt for deep thinking if enabled
        system_prompt = request.system_prompt
        if request.deep_thinking:
            system_prompt = (system_prompt or "") + "\n\nIMPORTANT: Think deeply about this question. Consider multiple perspectives, provide detailed reasoning, and give a comprehensive answer."
        
        # Get AI response using selected model with error handling
        try:
            response = await ai_service.get_response(
                message=request.message,
                model=model_id,
                system_prompt=system_prompt,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                response_length=response_length.value,
                deep_thinking=request.deep_thinking or False,
            )
            # Mark model as successful
            model_selector.reset_model_status(model_id, success=True)
        except Exception as e:
            logger.error(f"Error getting response from model {model_id}: {e}")
            # Mark model as failed and try fallback
            model_selector.reset_model_status(model_id, success=False)
            response = f"Model {model_profile.name} temporarily unavailable. Attempting alternative... (Error: {str(e)[:100]})"
        
        # Save assistant message
        await db_service.save_message(
            chat_id=chat_id,
            user_id=user_id,
            role="assistant",
            content=response,
            model="sakha-5.0"
        )
        
        logger.info(f"Chat: user={user_id}, task={task_type.value}, model={model_profile.name}, deep_thinking={request.deep_thinking}, response_length={response_length.value}")
        logger.info(f"Routing: {routing_reason}")
        
        return ChatResponse(
            chat_id=chat_id,
            message=response,
            model="sakha-5.0",
            timestamp=datetime.utcnow(),
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest, user_id: str = Header(None)):
    """Stream chat response with Sakha-5.0 intelligent routing and failover"""
    try:
        if not request.message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        user_id = user_id or request.user_id or "anonymous"
        
        # Use model router with failover to select best model for this message
        try:
            model_profile, task_type, routing_reason, response_length = await model_selector.get_model_with_failover(
                request.message,
                user_preference=request.model,
                priority="quality",
                deep_thinking=request.deep_thinking or False
            )
        except Exception as e:
            logger.error(f"Error in model selection: {e}")
            model_profile, task_type, routing_reason, response_length = model_selector.get_model_for_message(
                request.message,
                user_preference=request.model,
                priority="quality",
                deep_thinking=request.deep_thinking or False
            )
        
        if not model_profile:
            # Fallback if no model available
            async def error_generator():
                yield f"data: {json.dumps({'chunk': 'System: All AI models are currently unavailable. Please try again later.'})}\n\n"
            return StreamingResponse(error_generator(), media_type="text/event-stream")
        
        model_id = model_profile.model_id
        
        # Create chat if doesn't exist
        chat_id = request.chat_id
        if not chat_id:
            chat = await db_service.save_chat(user_id, "New Chat", "sakha-5.0")
            chat_id = chat["_id"]
        
        # Save user message
        await db_service.save_message(
            chat_id=chat_id,
            user_id=user_id,
            role="user",
            content=request.message,
            model="sakha-5.0"
        )
        
        logger.info(f"Stream: user={user_id}, task={task_type.value}, model={model_profile.name}, deep_thinking={request.deep_thinking}")
        logger.info(f"Routing: {routing_reason}")
        
        # Prepare system prompt for deep thinking if enabled
        system_prompt = request.system_prompt
        if request.deep_thinking:
            system_prompt = (system_prompt or "") + "\n\nIMPORTANT: Think deeply about this question. Consider multiple perspectives, provide detailed reasoning, and give a comprehensive answer."
        
        # Stream response from AI service
        async def response_generator():
            full_response = ""
            try:
                async for chunk in ai_service.stream_response(
                    message=request.message,
                    model=model_id,
                    system_prompt=system_prompt,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens,
                    response_length=response_length.value,
                    deep_thinking=request.deep_thinking or False,
                ):
                    full_response += chunk
                    yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                
                # Mark model as successful
                model_selector.reset_model_status(model_id, success=True)
            except Exception as e:
                logger.error(f"Error streaming from model {model_id}: {e}")
                # Mark model as failed
                model_selector.reset_model_status(model_id, success=False)
                error_msg = f"Model {model_profile.name} error: {str(e)[:100]}"
                full_response += error_msg
                yield f"data: {json.dumps({'chunk': error_msg})}\n\n"
            finally:
                # Save complete assistant message
                await db_service.save_message(
                    chat_id=chat_id,
                    user_id=user_id,
                    role="assistant",
                    content=full_response,
                    model="sakha-5.0"
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
    """Get list of all available AI models with standardized naming format"""
    
    # Capability mapping for standardized display
    capability_map = {
        "text_generation": "Text Generation",
        "code_generation": "Code Generation",
        "creative_writing": "Creative Writing",
        "analysis": "Analysis",
        "summary": "Summary",
        "question_answer": "Q&A",
        "video_processing": "Video Processing",
        "audio_processing": "Audio Processing",
        "image_generation": "Image Generation",
        "embedding": "Embeddings",
        "deep_thinking": "Deep Thinking",
        "general": "General Purpose",
    }
    
    # Provider mapping for standardized display
    provider_map = {
        "nemotron": "NVIDIA",
        "qwen": "Qwen",
        "laguna": "Poolside",
        "video": "OpenRouter",
        "audio": "OpenRouter",
        "image": "OpenRouter",
        "embed": "OpenRouter",
    }
    
    models = []
    
    # Add SAKHA-5.0 Unified Model first
    underlying_count = 0
    underlying_models_list = []
    for model in model_selector.get_available_models():
        underlying_count += 1
        underlying_models_list.append({
            "id": model.model_id,
            "name": model.name,
        })
    
    models.append({
        "id": "sakha-5.0",
        "name": "SAKHA-5.0 Unified AI",
        "provider": "Multi-Model",
        "description": "Intelligent unified model that automatically selects the best AI model based on task requirements",
        "available": True,
        "enabled": True,
        "speed": 7,
        "quality": 9,
        "capabilities": ["Text Generation", "Code Generation", "Creative Writing", "Analysis", "Q&A", "Deep Thinking"],
        "underlying_model_count": underlying_count,
    })
    
    # Add all individual models
    for model in model_selector.get_available_models():
        # Determine provider
        provider = "OpenRouter"
        for key, prov in provider_map.items():
            if key in model.model_id.lower():
                provider = prov
                break
        
        # Format capabilities
        capabilities = []
        for cap in model.capabilities:
            cap_key = cap.lower().replace(" ", "_").replace("-", "_")
            for old, new in [
                ("long_form_generation", "text_generation"),
                ("fast_response", "general"),
                ("balanced_performance", "general"),
                ("code", "code_generation"),
                ("debugging", "code_generation"),
                ("technical", "code_generation"),
            ]:
                cap = cap.replace(old, new)
            if cap in capability_map:
                if capability_map[cap] not in capabilities:
                    capabilities.append(capability_map[cap])
        
        if not capabilities:
            capabilities = ["General Purpose"]
        
        models.append({
            "id": model.model_id,
            "name": model.name,
            "provider": provider,
            "description": f"Optimized for: {', '.join([t.value.replace('_', ' ').title() for t in model.best_for[:2]])}",
            "available": model.available,
            "enabled": model.available,
            "speed": model.speed,
            "quality": model.quality,
            "cost": model.cost,
            "token_limit": model.token_limit,
            "capabilities": capabilities,
            "best_for": [t.value for t in model.best_for],
            "short_answer_score": model.short_answer_score,
            "long_answer_score": model.long_answer_score,
            "deep_thinking_capable": model.deep_thinking_capable,
        })
    
    return {
        "models": models,
        "total_count": len(models),
        "available_count": sum(1 for m in models if m["available"]),
    }
