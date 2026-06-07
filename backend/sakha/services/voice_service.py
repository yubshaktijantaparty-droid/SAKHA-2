"""Voice Service for SAKHA AI Premium"""

import aiohttp
import json
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class VoiceService:
    """Service for speech-to-text and text-to-speech"""
    
    def __init__(
        self, 
        elevenlabs_api_key: Optional[str] = None,
        google_api_key: Optional[str] = None
    ):
        self.elevenlabs_api_key = elevenlabs_api_key
        self.google_api_key = google_api_key
    
    async def text_to_speech(self, text: str, voice_id: str = "default") -> Optional[bytes]:
        """Convert text to speech using ElevenLabs"""
        try:
            if not self.elevenlabs_api_key:
                logger.warning("ElevenLabs API key not configured")
                return None
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "xi-api-key": self.elevenlabs_api_key,
                    "Content-Type": "application/json"
                }
                data = {
                    "text": text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.75
                    }
                }
                
                async with session.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                    headers=headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        return await response.read()
                    else:
                        logger.error(f"TTS failed: {await response.text()}")
                        return None
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            return None
    
    async def speech_to_text(self, audio_file: bytes) -> Optional[str]:
        """Convert speech to text using OpenAI Whisper"""
        try:
            async with aiohttp.ClientSession() as session:
                from sakha.config import settings
                
                headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
                
                # Create form data
                data = aiohttp.FormData()
                data.add_field("file", audio_file, filename="audio.wav")
                data.add_field("model", "whisper-1")
                
                async with session.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    headers=headers,
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("text")
                    else:
                        logger.error(f"STT failed: {await response.text()}")
                        return None
        except Exception as e:
            logger.error(f"Speech-to-text error: {e}")
            return None
