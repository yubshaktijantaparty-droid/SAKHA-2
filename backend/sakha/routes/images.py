"""Image Generation Endpoints - Production Ready"""

from fastapi import APIRouter, HTTPException, Header, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import logging

from sakha.services.image_service import ImageService
from sakha.services.database_service import db_service

logger = logging.getLogger(__name__)
router = APIRouter()
image_service = ImageService()


# ==================== MODELS ====================

class ImageGenerationRequest(BaseModel):
    """Image generation request"""
    prompt: str
    negative_prompt: Optional[str] = ""
    width: Optional[int] = 512
    height: Optional[int] = 512
    style: Optional[str] = "realistic"
    quality: Optional[str] = "standard"
    num_images: Optional[int] = 1
    enhance_prompt: Optional[bool] = True


class ImageResponse(BaseModel):
    """Image generation response"""
    image_url: str
    prompt: str
    timestamp: datetime


# ==================== ROUTES ====================

@router.post("/images/generate")
async def generate_image(
    request: ImageGenerationRequest,
    user_id: str = Header(default="anonymous")
):
    """Generate an image from text prompt"""
    try:
        if not request.prompt or len(request.prompt.strip()) == 0:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        # Validate prompt length
        if len(request.prompt) > 1000:
            raise HTTPException(status_code=400, detail="Prompt too long (max 1000 characters)")
        
        # Enhance prompt if requested
        prompt = request.prompt
        if request.enhance_prompt:
            logger.info("Enhancing prompt...")
            prompt = await image_service.enhance_prompt(prompt)
        
        # Generate image
        image_urls = await image_service.generate_image(
            prompt=prompt,
            negative_prompt=request.negative_prompt,
            width=request.width,
            height=request.height,
            style=request.style,
            user_id=user_id,
        )
        
        logger.info(f"Generated {len(image_urls)} image(s) for user {user_id}")
        
        return {
            "success": True,
            "images": [
                {"url": url, "prompt": prompt, "timestamp": datetime.utcnow().isoformat()}
                for url in image_urls
            ],
            "count": len(image_urls)
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Image generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")


@router.get("/images/enhance-prompt")
async def enhance_prompt(prompt: str = Query(..., min_length=1, max_length=1000)):
    """Enhance an image prompt for better results"""
    try:
        if not prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        enhanced = await image_service.enhance_prompt(prompt)
        logger.info(f"Prompt enhanced successfully")
        
        return {
            "original": prompt,
            "enhanced": enhanced,
        }
        
    except Exception as e:
        logger.error(f"Prompt enhancement error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/images/styles")
async def get_image_styles():
    """Get available image styles"""
    try:
        styles = ImageService.get_available_styles()
        return {
            "styles": styles,
            "count": len(styles)
        }
    except Exception as e:
        logger.error(f"Error fetching styles: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/images/providers")
async def get_image_providers():
    """Get available image generation providers and their status"""
    try:
        from sakha.config import settings
        import os
        
        providers = [
            {
                "name": "Stability AI",
                "id": "stability-ai",
                "quality": "excellent",
                "available": bool(settings.STABILITY_AI_API_KEY),
                "tier": "commercial"
            },
            {
                "name": "Hugging Face",
                "id": "huggingface",
                "quality": "good",
                "available": bool(os.getenv("HUGGINGFACE_API_KEY")),
                "tier": "free"
            },
            {
                "name": "Replicate",
                "id": "replicate",
                "quality": "good",
                "available": bool(os.getenv("REPLICATE_API_KEY")),
                "tier": "free-tier"
            },
        ]
        
        active_provider = next((p for p in providers if p["available"]), None)
        
        return {
            "providers": providers,
            "active_provider": active_provider.get("name") if active_provider else "Placeholder (Configure API keys)",
            "placeholder_fallback": "enabled"
        }
        
    except Exception as e:
        logger.error(f"Error fetching providers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/images/history/{user_id}")
async def get_image_history(
    user_id: str,
    limit: int = Query(20, ge=1, le=100)
):
    """Get user's image generation history"""
    try:
        images = await image_service.get_image_history(user_id, limit)
        logger.info(f"Retrieved {len(images)} images from history")
        
        return {
            "user_id": user_id,
            "images": images,
            "count": len(images)
        }
        
    except Exception as e:
        logger.error(f"Error retrieving image history: {e}")
        raise HTTPException(status_code=500, detail=str(e))
