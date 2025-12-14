"""
Model Manager with Intelligent Fallback System
Handles RESOURCE_EXHAUSTED errors by cascading through available models
"""

import logging
import time
from typing import Optional, List, Dict, Any
from google.adk.models.google_llm import Gemini
from google.genai import types
import threading

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ModelManager:
    """
    Manages model selection with intelligent fallback for quota exhaustion.
    
    Fallback Chain (based on your available quota):
    1. gemini-2.0-flash-lite (primary - fastest, highest quota)
    2. gemini-2.5-flash-lite (secondary)
    3. gemini-2.0-flash (tertiary)
    4. gemini-2.5-pro (last resort - highest quality but limited quota)
    """
    
    # Model fallback chain in priority order
    MODEL_FALLBACK_CHAIN = [
        "gemini-2.0-flash-lite",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
        "gemini-2.5-pro"
    ]
    
    def __init__(self):
        """Initialize model manager with availability tracking."""
        self._exhausted_models: Dict[str, float] = {}  # model_name -> timestamp
        self._lock = threading.Lock()
        self._retry_config = types.HttpRetryOptions(
            attempts=3,
            exp_base=2,
            initial_delay=1,
            http_status_codes=[429, 500, 503, 504]
        )
        logger.info(f"🔧 ModelManager initialized with fallback chain: {self.MODEL_FALLBACK_CHAIN}")
    
    def get_model(self, preferred_model: Optional[str] = None) -> Gemini:
        """
        Get an available model, falling back to alternatives if needed.
        
        Args:
            preferred_model: Preferred model name (defaults to first in chain)
            
        Returns:
            Gemini model instance
        """
        # Start with preferred model or first in chain
        if preferred_model and preferred_model in self.MODEL_FALLBACK_CHAIN:
            models_to_try = [preferred_model] + [
                m for m in self.MODEL_FALLBACK_CHAIN if m != preferred_model
            ]
        else:
            models_to_try = self.MODEL_FALLBACK_CHAIN.copy()
        
        # Filter out recently exhausted models (within last 60 seconds)
        current_time = time.time()
        available_models = []
        
        with self._lock:
            for model_name in models_to_try:
                if model_name in self._exhausted_models:
                    exhausted_time = self._exhausted_models[model_name]
                    # Reset after 60 seconds
                    if current_time - exhausted_time > 60:
                        del self._exhausted_models[model_name]
                        available_models.append(model_name)
                    else:
                        logger.debug(f"⏭️ Skipping {model_name} (exhausted {current_time - exhausted_time:.0f}s ago)")
                else:
                    available_models.append(model_name)
        
        if not available_models:
            logger.warning("⚠️ All models temporarily exhausted, resetting and using primary")
            with self._lock:
                self._exhausted_models.clear()
            available_models = [self.MODEL_FALLBACK_CHAIN[0]]
        
        selected_model = available_models[0]
        logger.info(f"✅ Selected model: {selected_model}")
        
        return Gemini(
            model=selected_model,
            fallback_models=available_models[1:] if len(available_models) > 1 else [],
            retry_options=self._retry_config
        )
    
    def mark_exhausted(self, model_name: str):
        """
        Mark a model as exhausted (quota exceeded).
        
        Args:
            model_name: Name of the exhausted model
        """
        with self._lock:
            self._exhausted_models[model_name] = time.time()
            logger.warning(f"🚫 Marked {model_name} as exhausted")
    
    def is_resource_exhausted_error(self, error: Exception) -> bool:
        """
        Check if an error is a RESOURCE_EXHAUSTED (429) error.
        
        Args:
            error: Exception to check
            
        Returns:
            True if error is resource exhaustion
        """
        error_str = str(error).lower()
        return (
            "429" in error_str or
            "resource_exhausted" in error_str or
            "resource exhausted" in error_str or
            "quota" in error_str
        )
    
    def get_user_friendly_error(self, error: Exception) -> Dict[str, Any]:
        """
        Convert technical error to user-friendly message.
        
        Args:
            error: Exception that occurred
            
        Returns:
            Dictionary with error details and suggestions
        """
        if self.is_resource_exhausted_error(error):
            return {
                "type": "quota_exhausted",
                "title": "API Quota Temporarily Exceeded",
                "message": "We're experiencing high demand right now. Our system is trying alternative models automatically.",
                "suggestions": [
                    "Wait a few seconds and try again",
                    "Use your own Google API key for unlimited access",
                    "Try a simpler query"
                ],
                "can_retry": True,
                "show_api_key_option": True
            }
        else:
            return {
                "type": "general_error",
                "title": "Something Went Wrong",
                "message": str(error),
                "suggestions": [
                    "Check your internet connection",
                    "Try again in a moment",
                    "Contact support if the issue persists"
                ],
                "can_retry": True,
                "show_api_key_option": False
            }
    
    def reset_exhausted_models(self):
        """Reset all exhausted model flags (for testing/admin)."""
        with self._lock:
            self._exhausted_models.clear()
            logger.info("🔄 Reset all exhausted model flags")


# Global singleton instance
_model_manager = None


def get_model_manager() -> ModelManager:
    """Get or create the global ModelManager instance."""
    global _model_manager
    if _model_manager is None:
        _model_manager = ModelManager()
    return _model_manager
