"""
SAKHA-5.0: Unified AI Model with Intelligent Routing System
This service automatically selects the best model based on task requirements
Features:
  - Intelligent task detection
  - Short/Long answer optimization
  - Deep thinking capability
  - Automatic failover when models are busy
"""

import os
from typing import Optional, Dict, List, Tuple
from enum import Enum
import logging
import aiohttp
import asyncio

logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Task classification for intelligent model routing"""
    TEXT_GENERATION = "text_generation"
    CODE_GENERATION = "code_generation"
    CREATIVE_WRITING = "creative_writing"
    ANALYSIS = "analysis"
    SUMMARY = "summary"
    QUESTION_ANSWER = "question_answer"
    VIDEO_PROCESSING = "video_processing"
    AUDIO_PROCESSING = "audio_processing"
    IMAGE_GENERATION = "image_generation"
    EMBEDDING = "embedding"
    DEEP_THINKING = "deep_thinking"
    GENERAL = "general"


class ResponseLength(Enum):
    """Response length preference"""
    SHORT = "short"  # < 100 tokens
    MEDIUM = "medium"  # 100-500 tokens
    LONG = "long"  # 500+ tokens
    VARIABLE = "variable"  # Auto-detect


class ModelProfile:
    """Profile for each model with capabilities and characteristics"""
    
    def __init__(
        self,
        model_id: str,
        name: str,
        api_key: Optional[str],
        capabilities: List[str],
        speed: int,  # 1-10 (10 = fastest)
        quality: int,  # 1-10 (10 = highest quality)
        cost: int,  # 1-10 (10 = most expensive)
        token_limit: int,
        best_for: List[TaskType],
        short_answer_score: int = 5,  # How good for short answers (1-10)
        long_answer_score: int = 5,  # How good for long answers (1-10)
        deep_thinking_capable: bool = False,
    ):
        self.model_id = model_id
        self.name = name
        self.api_key = api_key
        self.capabilities = capabilities
        self.speed = speed
        self.quality = quality
        self.cost = cost
        self.token_limit = token_limit
        self.best_for = best_for
        self.short_answer_score = short_answer_score
        self.long_answer_score = long_answer_score
        self.deep_thinking_capable = deep_thinking_capable
        self.available = bool(api_key)
        self.is_busy = False  # Track if model is currently busy
        self.failure_count = 0  # Track consecutive failures
        self.last_error = None  # Track last error


class ModelSelector:
    """Intelligent model selector for Sakha-5.0 with failover"""
    
    def __init__(self):
        """Initialize all available models with their profiles"""
        self.models: Dict[str, ModelProfile] = {}
        self._initialize_models()
        self.max_retries = 3
        self.timeout = 30
    
    def _initialize_models(self):
        """Initialize all available models"""
        
        # Primary Long-form Text Generation Model
        self.models["nemotron-3-ultra"] = ModelProfile(
            model_id="nemotron-3-ultra",
            name="NVIDIA Nemotron-3 Ultra 550B",
            api_key=os.getenv("NEMOTRON_3_ULTRA_550B_API_KEY"),
            capabilities=["long-form generation", "complex reasoning", "nuanced understanding", "deep thinking"],
            speed=6,
            quality=10,
            cost=9,
            token_limit=32000,
            best_for=[
                TaskType.TEXT_GENERATION,
                TaskType.ANALYSIS,
                TaskType.CREATIVE_WRITING,
                TaskType.QUESTION_ANSWER,
                TaskType.DEEP_THINKING,
            ],
            short_answer_score=6,
            long_answer_score=10,
            deep_thinking_capable=True,
        )
        
        # Fast Medium-size Model
        self.models["nemotron-3-super"] = ModelProfile(
            model_id="nemotron-3-super",
            name="NVIDIA Nemotron-3 Super 120B",
            api_key=os.getenv("NEMOTRON_3_SUPER_120B_API_KEY"),
            capabilities=["balanced performance", "fast response", "good quality", "reasoning"],
            speed=8,
            quality=9,
            cost=7,
            token_limit=16000,
            best_for=[
                TaskType.TEXT_GENERATION,
                TaskType.QUESTION_ANSWER,
                TaskType.SUMMARY,
                TaskType.GENERAL,
                TaskType.DEEP_THINKING,
            ],
            short_answer_score=8,
            long_answer_score=9,
            deep_thinking_capable=True,
        )
        
        # Nano Omni Model (Multimodal)
        self.models["nemotron-3-nano-omni"] = ModelProfile(
            model_id="nemotron-3-nano-omni",
            name="NVIDIA Nemotron-3 Nano Omni",
            api_key=os.getenv("NEMOTRON_3_NANO_OMNI_API_KEY"),
            capabilities=["fast processing", "audio input", "multimodal", "quick answers"],
            speed=10,
            quality=7,
            cost=3,
            token_limit=8000,
            best_for=[
                TaskType.AUDIO_PROCESSING,
                TaskType.GENERAL,
                TaskType.QUESTION_ANSWER,
            ],
            short_answer_score=10,
            long_answer_score=5,
        )
        
        # Code Generation Specialist
        self.models["qwen-qwen3-coder"] = ModelProfile(
            model_id="qwen-qwen3-coder",
            name="Qwen Qwen3 Coder",
            api_key=os.getenv("QWEN_QWEN3_CODER_API_KEY"),
            capabilities=["code generation", "debugging", "technical writing", "explanations"],
            speed=9,
            quality=9,
            cost=4,
            token_limit=12000,
            best_for=[
                TaskType.CODE_GENERATION,
                TaskType.ANALYSIS,
            ],
            short_answer_score=9,
            long_answer_score=8,
        )
        
        # Fast Lightweight Models
        self.models["laguna-m"] = ModelProfile(
            model_id="laguna-m",
            name="Poolside Laguna M (Medium)",
            api_key=os.getenv("LAGUNA_M_API_KEY"),
            capabilities=["fast inference", "lightweight", "efficient", "responsive"],
            speed=10,
            quality=7,
            cost=2,
            token_limit=4096,
            best_for=[
                TaskType.GENERAL,
                TaskType.QUESTION_ANSWER,
                TaskType.SUMMARY,
            ],
            short_answer_score=10,
            long_answer_score=6,
        )
        
        self.models["laguna-xs"] = ModelProfile(
            model_id="laguna-xs",
            name="Poolside Laguna XS (Extra Small)",
            api_key=os.getenv("LAGUNA_XS_API_KEY"),
            capabilities=["ultra-fast", "minimal latency", "instant responses"],
            speed=10,
            quality=6,
            cost=1,
            token_limit=2048,
            best_for=[
                TaskType.GENERAL,
                TaskType.SUMMARY,
            ],
            short_answer_score=10,
            long_answer_score=4,
        )
        
        # Multimodal Models
        self.models["video-input-1"] = ModelProfile(
            model_id="video-input-1",
            name="Video Analysis Model 1",
            api_key=os.getenv("VIDEO_INPUT_1_API_KEY"),
            capabilities=["video processing", "frame extraction", "video understanding"],
            speed=5,
            quality=9,
            cost=8,
            token_limit=100000,
            best_for=[TaskType.VIDEO_PROCESSING]
        )
        
        self.models["video-input-2"] = ModelProfile(
            model_id="video-input-2",
            name="Video Analysis Model 2",
            api_key=os.getenv("VIDEO_INPUT_2_API_KEY"),
            capabilities=["video processing", "scene detection", "video analysis"],
            speed=6,
            quality=9,
            cost=8,
            token_limit=100000,
            best_for=[TaskType.VIDEO_PROCESSING]
        )
        
        self.models["audio-input"] = ModelProfile(
            model_id="audio-input",
            name="Audio Processing Model",
            api_key=os.getenv("AUDIO_INPUT_API_KEY"),
            capabilities=["audio processing", "speech recognition", "audio analysis"],
            speed=7,
            quality=8,
            cost=5,
            token_limit=50000,
            best_for=[TaskType.AUDIO_PROCESSING]
        )
        
        self.models["image-output-1"] = ModelProfile(
            model_id="image-output-1",
            name="Image Generation Model 1",
            api_key=os.getenv("IMAGE_OUTPUT_1_API_KEY"),
            capabilities=["image generation", "visual creation", "diffusion"],
            speed=4,
            quality=9,
            cost=8,
            token_limit=0,
            best_for=[TaskType.IMAGE_GENERATION]
        )
        
        self.models["image-output-2"] = ModelProfile(
            model_id="image-output-2",
            name="Image Generation Model 2",
            api_key=os.getenv("IMAGE_OUTPUT_2_API_KEY"),
            capabilities=["image generation", "style transfer", "upscaling"],
            speed=5,
            quality=8,
            cost=7,
            token_limit=0,
            best_for=[TaskType.IMAGE_GENERATION]
        )
        
        self.models["embed-output"] = ModelProfile(
            model_id="embed-output",
            name="Embedding/Vector Model",
            api_key=os.getenv("EMBED_OUTPUT_API_KEY"),
            capabilities=["embeddings", "vector generation", "semantic search"],
            speed=9,
            quality=8,
            cost=3,
            token_limit=0,
            best_for=[TaskType.EMBEDDING]
        )
        
        logger.info(f"Initialized {len(self.models)} models for Sakha-5.0")
    
    def get_available_models(self) -> List[ModelProfile]:
        """Get all available models that are not busy"""
        return [m for m in self.models.values() if m.available and not m.is_busy]
    
    def detect_task_type(self, message: str) -> TaskType:
        """Detect task type from user message"""
        message_lower = message.lower()
        
        # Deep thinking keywords
        if any(keyword in message_lower for keyword in ["think deeply", "deep thinking", "profound", "analyze thoroughly", "detailed analysis"]):
            return TaskType.DEEP_THINKING
        
        # Code generation keywords
        if any(keyword in message_lower for keyword in ["code", "function", "script", "program", "debug", "implement", "write code"]):
            return TaskType.CODE_GENERATION
        
        # Video processing keywords
        if any(keyword in message_lower for keyword in ["video", "video analysis", "frame", "scene"]):
            return TaskType.VIDEO_PROCESSING
        
        # Audio processing keywords
        if any(keyword in message_lower for keyword in ["audio", "sound", "speech", "music"]):
            return TaskType.AUDIO_PROCESSING
        
        # Image generation keywords
        if any(keyword in message_lower for keyword in ["image", "generate image", "picture", "draw", "create image"]):
            return TaskType.IMAGE_GENERATION
        
        # Creative writing keywords
        if any(keyword in message_lower for keyword in ["story", "poem", "creative", "write", "article"]):
            return TaskType.CREATIVE_WRITING
        
        # Summary keywords
        if any(keyword in message_lower for keyword in ["summarize", "summary", "brief", "tldr", "recap"]):
            return TaskType.SUMMARY
        
        # Analysis keywords
        if any(keyword in message_lower for keyword in ["analyze", "analysis", "explain", "compare", "contrast"]):
            return TaskType.ANALYSIS
        
        # Question answering
        if message_lower.endswith("?"):
            return TaskType.QUESTION_ANSWER
        
        return TaskType.GENERAL
    
    def detect_response_length(self, message: str) -> ResponseLength:
        """Detect desired response length from message"""
        message_lower = message.lower()
        
        # Long answer keywords
        if any(keyword in message_lower for keyword in ["explain", "detailed", "comprehensive", "thorough", "full explanation", "in depth", "elaborate"]):
            return ResponseLength.LONG
        
        # Short answer keywords
        if any(keyword in message_lower for keyword in ["brief", "short", "quick", "tldr", "summary", "concise", "one word", "one line"]):
            return ResponseLength.SHORT
        
        # Variable (user hasn't specified)
        return ResponseLength.VARIABLE
    
    def select_best_model(
        self,
        task_type: TaskType,
        response_length: ResponseLength = ResponseLength.VARIABLE,
        priority: str = "quality",  # "quality", "speed", "cost", "balanced"
        max_tokens: Optional[int] = None,
        deep_thinking: bool = False,
    ) -> Tuple[Optional[ModelProfile], str]:
        """
        Select the best model for the task with failover support
        
        Args:
            task_type: Type of task
            response_length: Desired response length
            priority: Optimization priority
            max_tokens: Maximum tokens needed
            deep_thinking: Enable deep thinking
            
        Returns:
            Tuple of (ModelProfile, reason)
        """
        
        # Filter models that can handle this task
        suitable_models = [
            m for m in self.get_available_models()
            if task_type in m.best_for and (max_tokens is None or m.token_limit >= max_tokens)
        ]
        
        # If deep thinking requested, filter for capable models
        if deep_thinking and task_type != TaskType.DEEP_THINKING:
            deep_thinking_models = [m for m in suitable_models if m.deep_thinking_capable]
            if deep_thinking_models:
                suitable_models = deep_thinking_models
                task_type = TaskType.DEEP_THINKING
        
        if not suitable_models:
            # Fallback to general models
            logger.warning(f"No suitable models for {task_type}, using fallback")
            suitable_models = [
                m for m in self.get_available_models()
                if m.token_limit >= (max_tokens or 4000) and m.failure_count < 3
            ]
        
        if not suitable_models:
            return None, "No available models"
        
        # Score models based on response length preference
        if response_length == ResponseLength.SHORT:
            suitable_models.sort(key=lambda m: m.short_answer_score, reverse=True)
        elif response_length == ResponseLength.LONG:
            suitable_models.sort(key=lambda m: m.long_answer_score, reverse=True)
        
        # Sort based on priority
        if priority == "speed":
            best = max(suitable_models, key=lambda m: (m.speed, m.short_answer_score if response_length == ResponseLength.SHORT else m.long_answer_score))
            reason = f"Selected for fastest response ({best.speed}/10 speed) with {response_length.value} answer"
        elif priority == "cost":
            best = min(suitable_models, key=lambda m: m.cost)
            reason = f"Selected for lowest cost ({best.cost}/10 cost)"
        elif priority == "balanced":
            # Balanced = (quality + speed) - cost, adjusted for response length
            if response_length == ResponseLength.SHORT:
                best = max(suitable_models, key=lambda m: ((m.quality + m.speed) / 2) * (m.short_answer_score / 10) - m.cost)
            else:
                best = max(suitable_models, key=lambda m: ((m.quality + m.speed) / 2) * (m.long_answer_score / 10) - m.cost)
            reason = f"Selected for balanced performance with {response_length.value} answer"
        else:  # quality
            best = max(suitable_models, key=lambda m: (m.quality, m.long_answer_score if response_length == ResponseLength.LONG else m.short_answer_score))
            reason = f"Selected for highest quality ({best.quality}/10 quality) with {response_length.value} answer"
        
        return best, reason
    
    def get_model_for_message(
        self,
        message: str,
        user_preference: Optional[str] = None,
        priority: str = "quality",
        deep_thinking: bool = False,
    ) -> Tuple[Optional[ModelProfile], TaskType, str, ResponseLength]:
        """
        Get the best model for a user message with failover support
        
        Args:
            message: User message
            user_preference: User's model preference (if any)
            priority: Optimization priority
            deep_thinking: Enable deep thinking
            
        Returns:
            Tuple of (ModelProfile, TaskType, reason, ResponseLength)
        """
        
        # If user specified a model, use it if available
        if user_preference and user_preference in self.models:
            model = self.models[user_preference]
            if model.available and not model.is_busy:
                return model, TaskType.GENERAL, "Using user preference", ResponseLength.VARIABLE
        
        # Detect task type and response length
        task_type = self.detect_task_type(message)
        response_length = self.detect_response_length(message)
        
        # Check if user explicitly wants deep thinking
        if deep_thinking or task_type == TaskType.DEEP_THINKING:
            response_length = ResponseLength.LONG  # Deep thinking requires longer responses
        
        # Select best model
        model, reason = self.select_best_model(
            task_type,
            response_length=response_length,
            priority=priority,
            deep_thinking=deep_thinking or task_type == TaskType.DEEP_THINKING
        )
        
        if model:
            logger.info(f"Selected model: {model.name} for task: {task_type.value}. {reason}")
        
        return model, task_type, reason, response_length
    
    async def get_model_with_failover(
        self,
        message: str,
        user_preference: Optional[str] = None,
        priority: str = "quality",
        deep_thinking: bool = False,
    ) -> Tuple[Optional[ModelProfile], TaskType, str, ResponseLength]:
        """
        Get model with automatic failover to alternative models if primary fails
        
        This method will retry with different models if the primary selection fails
        """
        
        primary_model, task_type, reason, response_length = self.get_model_for_message(
            message, user_preference, priority, deep_thinking
        )
        
        if not primary_model:
            return None, task_type, "No available models", response_length
        
        # Mark model as being attempted
        primary_model.is_busy = True
        
        try:
            # Try to use the primary model (actual API call would happen in ai_service)
            return primary_model, task_type, reason, response_length
        except Exception as e:
            logger.error(f"Primary model {primary_model.model_id} failed: {e}")
            primary_model.failure_count += 1
            primary_model.last_error = str(e)
            
            # If primary fails, try alternative models
            if primary_model.failure_count < 3:
                logger.info(f"Attempting failover from {primary_model.name}")
                alternative_model, task_type, alt_reason, response_length = self.get_model_for_message(
                    message, user_preference=None, priority="balanced", deep_thinking=deep_thinking
                )
                
                if alternative_model and alternative_model.model_id != primary_model.model_id:
                    logger.info(f"Failover successful: using {alternative_model.name}")
                    return alternative_model, task_type, f"Failover: {alt_reason}", response_length
            
            # If all else fails, return None
            return None, task_type, f"Model failed with error: {str(e)}", response_length
        finally:
            # Release busy state
            primary_model.is_busy = False
    
    def reset_model_status(self, model_id: str, success: bool = True):
        """Reset model status after successful/failed request"""
        if model_id in self.models:
            model = self.models[model_id]
            if success:
                model.failure_count = max(0, model.failure_count - 1)
                model.last_error = None
                logger.info(f"Model {model.name} recovered (failures: {model.failure_count})")
            else:
                model.failure_count += 1
                logger.warning(f"Model {model.name} failure count: {model.failure_count}")


# Global instance
model_selector = ModelSelector()


def get_model_selector() -> ModelSelector:
    """Get the global model selector instance"""
    return model_selector

    """Profile for each model with capabilities and characteristics"""
    
    def __init__(
        self,
        model_id: str,
        name: str,
        api_key: Optional[str],
        capabilities: List[str],
        speed: int,  # 1-10 (10 = fastest)
        quality: int,  # 1-10 (10 = highest quality)
        cost: int,  # 1-10 (10 = most expensive)
        token_limit: int,
        best_for: List[TaskType],
    ):
        self.model_id = model_id
        self.name = name
        self.api_key = api_key
        self.capabilities = capabilities
        self.speed = speed
        self.quality = quality
        self.cost = cost
        self.token_limit = token_limit
        self.best_for = best_for
        self.available = bool(api_key)


class ModelSelector:
    """Intelligent model selector for Sakha-5.0"""
    
    def __init__(self):
        """Initialize all available models with their profiles"""
        self.models: Dict[str, ModelProfile] = {}
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all available models"""
        
        # Primary Long-form Text Generation Model
        self.models["nemotron-3-ultra"] = ModelProfile(
            model_id="nemotron-3-ultra",
            name="NVIDIA Nemotron-3 Ultra 550B",
            api_key=os.getenv("NEMOTRON_3_ULTRA_550B_API_KEY"),
            capabilities=["long-form generation", "complex reasoning", "nuanced understanding"],
            speed=6,
            quality=10,
            cost=9,
            token_limit=32000,
            best_for=[
                TaskType.TEXT_GENERATION,
                TaskType.ANALYSIS,
                TaskType.CREATIVE_WRITING,
                TaskType.QUESTION_ANSWER,
            ]
        )
        
        # Fast Medium-size Model
        self.models["nemotron-3-super"] = ModelProfile(
            model_id="nemotron-3-super",
            name="NVIDIA Nemotron-3 Super 120B",
            api_key=os.getenv("NEMOTRON_3_SUPER_120B_API_KEY"),
            capabilities=["balanced performance", "fast response", "good quality"],
            speed=8,
            quality=9,
            cost=7,
            token_limit=16000,
            best_for=[
                TaskType.TEXT_GENERATION,
                TaskType.QUESTION_ANSWER,
                TaskType.SUMMARY,
                TaskType.GENERAL,
            ]
        )
        
        # Nano Omni Model (Multimodal)
        self.models["nemotron-3-nano-omni"] = ModelProfile(
            model_id="nemotron-3-nano-omni",
            name="NVIDIA Nemotron-3 Nano Omni",
            api_key=os.getenv("NEMOTRON_3_NANO_OMNI_API_KEY"),
            capabilities=["fast processing", "audio input", "multimodal"],
            speed=10,
            quality=7,
            cost=3,
            token_limit=8000,
            best_for=[
                TaskType.AUDIO_PROCESSING,
                TaskType.GENERAL,
                TaskType.QUESTION_ANSWER,
            ]
        )
        
        # Code Generation Specialist
        self.models["qwen-qwen3-coder"] = ModelProfile(
            model_id="qwen-qwen3-coder",
            name="Qwen Qwen3 Coder",
            api_key=os.getenv("QWEN_QWEN3_CODER_API_KEY"),
            capabilities=["code generation", "debugging", "technical writing"],
            speed=9,
            quality=9,
            cost=4,
            token_limit=12000,
            best_for=[
                TaskType.CODE_GENERATION,
                TaskType.ANALYSIS,
            ]
        )
        
        # Fast Lightweight Models
        self.models["laguna-m"] = ModelProfile(
            model_id="laguna-m",
            name="Poolside Laguna M (Medium)",
            api_key=os.getenv("LAGUNA_M_API_KEY"),
            capabilities=["fast inference", "lightweight", "efficient"],
            speed=10,
            quality=7,
            cost=2,
            token_limit=4096,
            best_for=[
                TaskType.GENERAL,
                TaskType.QUESTION_ANSWER,
                TaskType.SUMMARY,
            ]
        )
        
        self.models["laguna-xs"] = ModelProfile(
            model_id="laguna-xs",
            name="Poolside Laguna XS (Extra Small)",
            api_key=os.getenv("LAGUNA_XS_API_KEY"),
            capabilities=["ultra-fast", "minimal latency"],
            speed=10,
            quality=6,
            cost=1,
            token_limit=2048,
            best_for=[
                TaskType.GENERAL,
                TaskType.SUMMARY,
            ]
        )
        
        # Multimodal Models
        self.models["video-input-1"] = ModelProfile(
            model_id="video-input-1",
            name="Video Analysis Model 1",
            api_key=os.getenv("VIDEO_INPUT_1_API_KEY"),
            capabilities=["video processing", "frame extraction", "video understanding"],
            speed=5,
            quality=9,
            cost=8,
            token_limit=100000,
            best_for=[TaskType.VIDEO_PROCESSING]
        )
        
        self.models["video-input-2"] = ModelProfile(
            model_id="video-input-2",
            name="Video Analysis Model 2",
            api_key=os.getenv("VIDEO_INPUT_2_API_KEY"),
            capabilities=["video processing", "scene detection", "video analysis"],
            speed=6,
            quality=9,
            cost=8,
            token_limit=100000,
            best_for=[TaskType.VIDEO_PROCESSING]
        )
        
        self.models["audio-input"] = ModelProfile(
            model_id="audio-input",
            name="Audio Processing Model",
            api_key=os.getenv("AUDIO_INPUT_API_KEY"),
            capabilities=["audio processing", "speech recognition", "audio analysis"],
            speed=7,
            quality=8,
            cost=5,
            token_limit=50000,
            best_for=[TaskType.AUDIO_PROCESSING]
        )
        
        self.models["image-output-1"] = ModelProfile(
            model_id="image-output-1",
            name="Image Generation Model 1",
            api_key=os.getenv("IMAGE_OUTPUT_1_API_KEY"),
            capabilities=["image generation", "visual creation", "diffusion"],
            speed=4,
            quality=9,
            cost=8,
            token_limit=0,
            best_for=[TaskType.IMAGE_GENERATION]
        )
        
        self.models["image-output-2"] = ModelProfile(
            model_id="image-output-2",
            name="Image Generation Model 2",
            api_key=os.getenv("IMAGE_OUTPUT_2_API_KEY"),
            capabilities=["image generation", "style transfer", "upscaling"],
            speed=5,
            quality=8,
            cost=7,
            token_limit=0,
            best_for=[TaskType.IMAGE_GENERATION]
        )
        
        self.models["embed-output"] = ModelProfile(
            model_id="embed-output",
            name="Embedding/Vector Model",
            api_key=os.getenv("EMBED_OUTPUT_API_KEY"),
            capabilities=["embeddings", "vector generation", "semantic search"],
            speed=9,
            quality=8,
            cost=3,
            token_limit=0,
            best_for=[TaskType.EMBEDDING]
        )
        
        logger.info(f"Initialized {len(self.models)} models for Sakha-5.0")
    
    def get_available_models(self) -> List[ModelProfile]:
        """Get all available models"""
        return [m for m in self.models.values() if m.available]
    
    def detect_task_type(self, message: str) -> TaskType:
        """Detect task type from user message"""
        message_lower = message.lower()
        
        # Code generation keywords
        if any(keyword in message_lower for keyword in ["code", "function", "script", "program", "debug"]):
            return TaskType.CODE_GENERATION
        
        # Video processing keywords
        if any(keyword in message_lower for keyword in ["video", "video analysis", "frame", "scene"]):
            return TaskType.VIDEO_PROCESSING
        
        # Audio processing keywords
        if any(keyword in message_lower for keyword in ["audio", "sound", "speech", "music"]):
            return TaskType.AUDIO_PROCESSING
        
        # Image generation keywords
        if any(keyword in message_lower for keyword in ["image", "generate image", "picture", "draw", "create image"]):
            return TaskType.IMAGE_GENERATION
        
        # Creative writing keywords
        if any(keyword in message_lower for keyword in ["story", "poem", "creative", "write", "article"]):
            return TaskType.CREATIVE_WRITING
        
        # Summary keywords
        if any(keyword in message_lower for keyword in ["summarize", "summary", "brief", "tldr", "recap"]):
            return TaskType.SUMMARY
        
        # Analysis keywords
        if any(keyword in message_lower for keyword in ["analyze", "analysis", "explain", "compare", "contrast"]):
            return TaskType.ANALYSIS
        
        # Question answering
        if message_lower.endswith("?"):
            return TaskType.QUESTION_ANSWER
        
        return TaskType.GENERAL
    
    def select_best_model(
        self,
        task_type: TaskType,
        priority: str = "quality",  # "quality", "speed", "cost", "balanced"
        max_tokens: Optional[int] = None,
    ) -> Tuple[Optional[ModelProfile], str]:
        """
        Select the best model for the task
        
        Args:
            task_type: Type of task
            priority: Optimization priority
            max_tokens: Maximum tokens needed
            
        Returns:
            Tuple of (ModelProfile, reason)
        """
        
        # Filter models that can handle this task
        suitable_models = [
            m for m in self.get_available_models()
            if task_type in m.best_for and (max_tokens is None or m.token_limit >= max_tokens)
        ]
        
        if not suitable_models:
            # Fallback to general models
            logger.warning(f"No suitable models for {task_type}, using fallback")
            suitable_models = [
                m for m in self.get_available_models()
                if m.token_limit >= (max_tokens or 4000)
            ]
        
        if not suitable_models:
            return None, "No available models"
        
        # Sort based on priority
        if priority == "speed":
            best = max(suitable_models, key=lambda m: m.speed)
            reason = f"Selected for fastest response ({best.speed}/10 speed)"
        elif priority == "cost":
            best = min(suitable_models, key=lambda m: m.cost)
            reason = f"Selected for lowest cost ({best.cost}/10 cost)"
        elif priority == "balanced":
            # Balanced = (quality + speed) - cost
            best = max(suitable_models, key=lambda m: (m.quality + m.speed) / 2 - m.cost)
            reason = f"Selected for balanced performance"
        else:  # quality
            best = max(suitable_models, key=lambda m: m.quality)
            reason = f"Selected for highest quality ({best.quality}/10 quality)"
        
        return best, reason
    
    def get_model_for_message(
        self,
        message: str,
        user_preference: Optional[str] = None,
        priority: str = "quality",
    ) -> Tuple[Optional[ModelProfile], TaskType, str]:
        """
        Get the best model for a user message
        
        Args:
            message: User message
            user_preference: User's model preference (if any)
            priority: Optimization priority
            
        Returns:
            Tuple of (ModelProfile, TaskType, reason)
        """
        
        # If user specified a model, use it
        if user_preference and user_preference in self.models:
            model = self.models[user_preference]
            if model.available:
                return model, TaskType.GENERAL, "Using user preference"
        
        # Detect task type
        task_type = self.detect_task_type(message)
        
        # Select best model
        model, reason = self.select_best_model(task_type, priority=priority)
        
        if model:
            logger.info(f"Selected model: {model.name} for task: {task_type.value}. {reason}")
        
        return model, task_type, reason


# Global instance
model_selector = ModelSelector()


def get_model_selector() -> ModelSelector:
    """Get the global model selector instance"""
    return model_selector
