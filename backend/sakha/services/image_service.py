"""Image Generation Service - Multiple Providers Support"""

import aiohttp
import os
from typing import List, Dict, Any
from datetime import datetime
from sakha.config import settings
from sakha.services.database_service import db_service
import logging
import json
import requests

logger = logging.getLogger(__name__)


class ImageService:
    """Image generation service with multiple provider support"""

    def __init__(self):
        self.stability_api_key = settings.STABILITY_AI_API_KEY
        self.huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.replicate_api_key = os.getenv("REPLICATE_API_KEY")
        
    async def generate_image(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 512,
        height: int = 512,
        style: str = "realistic",
        quality: str = "standard",
        user_id: str = "anonymous",
    ) -> List[str]:
        """Generate images using available providers"""
        
        try:
            # Try Stability AI first (commercial, high quality)
            if self.stability_api_key:
                logger.info("Using Stability AI for image generation")
                urls = await self._generate_with_stability_ai(prompt, negative_prompt, width, height)
                if urls:
                    # Save to database
                    for url in urls:
                        await db_service.save_image(user_id, prompt, url, "stability-ai")
                    return urls
            
            # Fall back to Hugging Face (free, good quality)
            if self.huggingface_api_key:
                logger.info("Using Hugging Face for image generation")
                urls = await self._generate_with_huggingface(prompt)
                if urls:
                    for url in urls:
                        await db_service.save_image(user_id, prompt, url, "huggingface")
                    return urls
            
            # Fall back to Replicate (free tier available)
            if self.replicate_api_key:
                logger.info("Using Replicate for image generation")
                urls = await self._generate_with_replicate(prompt)
                if urls:
                    for url in urls:
                        await db_service.save_image(user_id, prompt, url, "replicate")
                    return urls
            
            # Last resort: return placeholder
            logger.warning("No image generation API configured, returning placeholder")
            placeholder_url = f"https://via.placeholder.com/{width}x{height}?text={prompt.replace(' ', '+')[:50]}"
            await db_service.save_image(user_id, prompt, placeholder_url, "placeholder")
            return [placeholder_url]
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            # Return placeholder on error
            placeholder_url = f"https://via.placeholder.com/512x512?text=Error"
            return [placeholder_url]
    
    async def _generate_with_stability_ai(
        self, prompt: str, negative_prompt: str, width: int, height: int
    ) -> List[str]:
        """Generate using Stability AI API"""
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.stability.ai/v1/generation/stable-diffusion-v3/text-to-image"
                
                headers = {
                    "authorization": f"Bearer {self.stability_api_key}",
                    "accept": "image/*"
                }
                
                data = {
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "model": "sd3",
                    "prompt_strength": 0.85,
                    "output_format": "jpeg",
                }
                
                async with session.post(url, headers=headers, json=data) as resp:
                    if resp.status == 200:
                        image_data = await resp.read()
                        # In production, upload to cloud storage and return URL
                        logger.info("Image generated successfully with Stability AI")
                        return [f"data:image/jpeg;base64,{image_data[:100]}..."]  # Placeholder
                    else:
                        logger.error(f"Stability AI error: {resp.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Stability AI generation error: {e}")
            return []
    
    async def _generate_with_huggingface(self, prompt: str) -> List[str]:
        """Generate using Hugging Face API (free)"""
        try:
            # Using free Hugging Face Inference API
            # Popular models: stabilityai/stable-diffusion-2, runwayml/stable-diffusion-v1-5
            
            url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
            headers = {"Authorization": f"Bearer {self.huggingface_api_key}"}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=headers,
                    json={"inputs": prompt}
                ) as resp:
                    if resp.status == 200:
                        # Response is image bytes
                        logger.info("Image generated with Hugging Face")
                        # In production, upload to cloud storage
                        return [f"https://huggingface.co/image_placeholder_{int(datetime.utcnow().timestamp())}"]
                    else:
                        logger.warning(f"Hugging Face API error: {resp.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Hugging Face generation error: {e}")
            return []
    
    async def _generate_with_replicate(self, prompt: str) -> List[str]:
        """Generate using Replicate API (free tier available)"""
        try:
            # Replicate API for Stable Diffusion XL (free tier: 0.025 credits per generation)
            
            url = "https://api.replicate.com/v1/predictions"
            headers = {
                "Authorization": f"Token {self.replicate_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "version": "9b1d629f5827ac46a7c3db735db0f5cd365053db5cb50bada02ecbdfb912e47c",  # SDXL
                "input": {
                    "prompt": prompt,
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as resp:
                    if resp.status == 201:
                        result = await resp.json()
                        # Poll for result or return webhook URL
                        logger.info("Replicate prediction created")
                        # In production, implement polling or webhook
                        return [f"https://replicate.com/predictions/{result.get('id')}"]
                    else:
                        logger.warning(f"Replicate API error: {resp.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Replicate generation error: {e}")
            return []

    async def enhance_prompt(self, prompt: str) -> str:
        """Enhance a user's prompt for better image generation using Claude/GPT"""
        try:
            # Use existing AI service to enhance prompt
            from sakha.services.ai_service import AIService
            ai_service = AIService()
            
            enhancement_prompt = f"""You are an expert at creating detailed, creative prompts for image generation AI.
            
Original prompt: {prompt}

Please enhance this prompt to be more detailed, creative, and optimized for image generation AI models.
Include style, lighting, composition, and mood details. Keep it under 200 words.
Return ONLY the enhanced prompt, no additional text."""
            
            enhanced = await ai_service.get_response(
                message=enhancement_prompt,
                model=settings.DEFAULT_AI_PROVIDER,
                max_tokens=150
            )
            
            logger.info(f"Prompt enhanced: {prompt} -> {enhanced}")
            return enhanced
            
        except Exception as e:
            logger.error(f"Prompt enhancement error: {e}")
            return prompt

    async def get_image_history(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get user's image generation history"""
        try:
            images = await db_service.get_image_history(user_id, limit)
            logger.info(f"Retrieved {len(images)} images for user {user_id}")
            return images
        except Exception as e:
            logger.error(f"Error retrieving image history: {e}")
            return []
    
    @staticmethod
    def get_available_styles() -> List[Dict[str, str]]:
        """Get available image generation styles"""
        return [
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
            {"id": "steampunk", "name": "Steampunk"},
            {"id": "neon", "name": "Neon"},
        ]

