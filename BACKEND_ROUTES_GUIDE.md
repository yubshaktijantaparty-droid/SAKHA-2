# SAKHA AI PREMIUM - ENHANCED BACKEND ROUTES

This document outlines all the API routes needed for the premium ChatGPT-like platform.
Implement these routes in the respective router files.

## 1. CHAT ROUTES (backend/sakha/routes/chat.py)

```python
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json

from sakha.services.ai_service import AIService
from sakha.services.memory_service import MemoryService
from sakha.config import settings

router = APIRouter()
ai_service = AIService()
memory_service = MemoryService()

class ChatRequest(BaseModel):
    message: str
    chat_id: Optional[str] = None
    model: str = "gpt-4o"
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    include_memory: bool = True

@router.post("/chat")
async def chat(request: ChatRequest):
    """Send a message and get AI response"""
    try:
        # Validate input
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Get memory context if enabled
        memory_context = ""
        if request.include_memory:
            # Fetch from database in production
            pass
        
        # Prepare system prompt with memory
        full_system_prompt = request.system_prompt or ""
        if memory_context:
            full_system_prompt += f"\n\nUser Context:\n{memory_context}"
        
        # Get response
        response = await ai_service.get_response(
            message=request.message,
            model=request.model,
            system_prompt=full_system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        
        return {
            "chat_id": request.chat_id or "new_chat",
            "message": response,
            "model": request.model,
            "tokens_used": len(response.split()),  # Approximate
            "timestamp": datetime.utcnow(),
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Stream AI response"""
    async def generate():
        try:
            async for chunk in ai_service.stream_response(
                message=request.message,
                model=request.model,
                system_prompt=request.system_prompt,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            ):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@router.get("/chats")
async def get_chats(user_id: str):
    """List all chats for user"""
    # Fetch from database
    return {"chats": []}

@router.get("/chats/{chat_id}")
async def get_chat(chat_id: str, user_id: str):
    """Get specific chat"""
    # Fetch from database
    return {"chat": None}

@router.delete("/chats/{chat_id}")
async def delete_chat(chat_id: str, user_id: str):
    """Delete chat"""
    # Delete from database
    return {"success": True}

@router.put("/chats/{chat_id}")
async def update_chat(chat_id: str, user_id: str, title: Optional[str] = None):
    """Update chat title"""
    # Update in database
    return {"chat": None}

@router.post("/chats/{chat_id}/export")
async def export_chat(chat_id: str, user_id: str, format: str = "markdown"):
    """Export chat in various formats"""
    # Export chat
    return {"export": None}
```

## 2. MEMORY ROUTES (backend/sakha/routes/memories.py)

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

class MemoryRequest(BaseModel):
    name: str
    content: str
    memory_type: str = "custom"
    importance: int = 5

@router.get("/memories")
async def get_memories(user_id: str):
    """Get user memories"""
    # Fetch from database
    return {"memories": []}

@router.post("/memories")
async def create_memory(user_id: str, request: MemoryRequest):
    """Create new memory"""
    # Save to database
    return {"memory": None}

@router.put("/memories/{memory_id}")
async def update_memory(memory_id: str, user_id: str, request: MemoryRequest):
    """Update memory"""
    # Update in database
    return {"memory": None}

@router.delete("/memories/{memory_id}")
async def delete_memory(memory_id: str, user_id: str):
    """Delete memory"""
    # Delete from database
    return {"success": True}

@router.post("/memories/clear")
async def clear_memories(user_id: str):
    """Clear all memories"""
    # Clear from database
    return {"success": True}
```

## 3. MODELS ROUTES (backend/sakha/routes/models.py)

```python
from fastapi import APIRouter

router = APIRouter()

AI_MODELS = [
    {
        "id": "gpt-5",
        "name": "GPT-5",
        "provider": "openai",
        "speed": 3,
        "cost": 5,
        "intelligence": 5,
        "context_window": 128000,
    },
    {
        "id": "gpt-4o",
        "name": "GPT-4o",
        "provider": "openai",
        "speed": 4,
        "cost": 3,
        "intelligence": 5,
        "context_window": 128000,
    },
    {
        "id": "claude-opus-4",
        "name": "Claude Opus",
        "provider": "anthropic",
        "speed": 2,
        "cost": 5,
        "intelligence": 5,
        "context_window": 200000,
    },
    {
        "id": "claude-sonnet-4",
        "name": "Claude Sonnet",
        "provider": "anthropic",
        "speed": 4,
        "cost": 3,
        "intelligence": 5,
        "context_window": 200000,
    },
    {
        "id": "gemini-2.5-pro",
        "name": "Gemini 2.5 Pro",
        "provider": "google",
        "speed": 3,
        "cost": 2,
        "intelligence": 5,
        "context_window": 1000000,
    },
    {
        "id": "gemini-2.5-flash",
        "name": "Gemini 2.5 Flash",
        "provider": "google",
        "speed": 5,
        "cost": 1,
        "intelligence": 3,
        "context_window": 1000000,
    },
    {
        "id": "deepseek-chat",
        "name": "DeepSeek Chat",
        "provider": "deepseek",
        "speed": 5,
        "cost": 1,
        "intelligence": 3,
        "context_window": 64000,
    },
    {
        "id": "deepseek-reasoner",
        "name": "DeepSeek Reasoner",
        "provider": "deepseek",
        "speed": 2,
        "cost": 2,
        "intelligence": 4,
        "context_window": 64000,
    },
]

@router.get("/models")
async def get_models():
    """Get available AI models"""
    return {"models": AI_MODELS}

@router.get("/models/{model_id}")
async def get_model(model_id: str):
    """Get specific model"""
    model = next((m for m in AI_MODELS if m["id"] == model_id), None)
    if not model:
        return {"error": "Model not found"}
    return {"model": model}
```

## 4. SEARCH ROUTES (backend/sakha/routes/search.py)

```python
from fastapi import APIRouter
from pydantic import BaseModel
from sakha.services.search_service import SearchService

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    num_results: int = 5

@router.post("/search")
async def search(request: SearchRequest):
    """Perform web search"""
    search_service = SearchService()
    results = await search_service.search(request.query, request.num_results)
    return {"results": results}
```

## 5. VOICE ROUTES (backend/sakha/routes/voice.py)

```python
from fastapi import APIRouter, File, UploadFile
from sakha.services.voice_service import VoiceService

router = APIRouter()

@router.post("/voice/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """Convert speech to text"""
    voice_service = VoiceService()
    audio_content = await file.read()
    text = await voice_service.speech_to_text(audio_content)
    return {"text": text}

@router.post("/voice/synthesize")
async def synthesize(text: str, voice_id: str = "default"):
    """Convert text to speech"""
    voice_service = VoiceService()
    audio = await voice_service.text_to_speech(text, voice_id)
    return {"audio": audio.hex() if audio else None}
```

## 6. FILES ROUTES (backend/sakha/routes/files.py) - Enhanced

```python
from fastapi import APIRouter, File, UploadFile, HTTPException
from sakha.services.file_service import FileService

router = APIRouter()

@router.post("/files/upload")
async def upload_file(user_id: str, file: UploadFile = File(...)):
    """Upload file for analysis"""
    try:
        file_service = FileService()
        result = await file_service.upload_file(user_id, file)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/files")
async def list_files(user_id: str):
    """List user's files"""
    # Fetch from database
    return {"files": []}

@router.post("/files/{file_id}/analyze")
async def analyze_file(file_id: str, user_id: str):
    """Analyze uploaded file"""
    # Analyze and return results
    return {"analysis": None}

@router.delete("/files/{file_id}")
async def delete_file(file_id: str, user_id: str):
    """Delete file"""
    # Delete from database and storage
    return {"success": True}
```

## Implementation Notes

1. All routes should include proper:
   - Input validation
   - Error handling
   - Logging
   - Rate limiting
   - User authentication (use JWT tokens)

2. Database operations should use motor (async MongoDB driver)

3. All responses should follow consistent JSON format:
   ```json
   {
     "success": boolean,
     "data": {...},
     "error": "error message if any"
   }
   ```

4. Streaming responses should use Server-Sent Events (SSE) format

5. All file operations should validate:
   - File type
   - File size
   - User permissions

6. Memory operations should maintain:
   - User privacy
   - Data consistency
   - Proper indexing for searches

See IMPLEMENTATION_GUIDE.md for complete backend setup instructions.
