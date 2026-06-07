"""Image Generation Endpoints"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from sakha.services.image_service import ImageService

router = APIRouter()
image_service = ImageService()


class ImageGenerationRequest(BaseModel):
    """Image generation request"""

    prompt: str
    negative_prompt: Optional[str] = ""
    width: Optional[int] = 512
    height: Optional[int] = 512
    aspect_ratio: Optional[str] = "1:1"  # 1:1, 16:9, 9:16, 4:3, 3:4
    style: Optional[str] = "realistic"
    quality: Optional[str] = "standard"  # standard, hd
    num_images: Optional[int] = 1


class ImageResponse(BaseModel):
    """Image generation response"""

    image_url: str
    prompt: str
    timestamp: datetime


@router.post("/images/generate")
async def generate_image(request: ImageGenerationRequest):
    """Generate an image from text prompt"""
    try:
        if not request.prompt:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")

        # Generate image
        image_urls = await image_service.generate_image(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            width=request.width,
            height=request.height,
            style=request.style,
            quality=request.quality,
        )

        return {
            "images": [
                {"url": url, "prompt": request.prompt, "timestamp": datetime.utcnow()}
                for url in image_urls
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/images/styles")
async def get_image_styles():
    """Get available image styles"""
    styles = [
        {"id": "realistic", "name": "Photorealistic"},
        {"id": "anime", "name": "Anime"},
        {"id": "ghibli", "name": "Studio Ghibli"},
        {"id": "fantasy", "name": "Fantasy Art"},
        {"id": "cyberpunk", "name": "Cyberpunk"},
        {"id": "cartoon", "name": "Cartoon"},
        {"id": "pixar", "name": "Pixar"},
        {"id": "watercolor", "name": "Watercolor"},
        {"id": "oil", "name": "Oil Painting"},
        {"id": "cinematic", "name": "Cinematic"},
    ]
    return {"styles": styles}


@router.get("/images/history/{user_id}")
async def get_image_history(user_id: str):
    """Get user's image generation history"""
    # TODO: Implement image history retrieval from database
    return {"user_id": user_id, "images": []}
