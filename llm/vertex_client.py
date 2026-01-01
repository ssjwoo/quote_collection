import logging
import asyncio
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Cache for libraries to avoid repeated imports
_VERTEX_LIBS_READY = None 

def _ensure_vertex_libs():
    """Import Vertex AI libs safely and cache them."""
    global _VERTEX_LIBS_READY
    if _VERTEX_LIBS_READY is not None:
        return _VERTEX_LIBS_READY
    
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel, Tool
        try:
            from vertexai.generative_models import GoogleSearchRetrieval
            grounding = GoogleSearchRetrieval
        except ImportError:
            grounding = None
        
        _VERTEX_LIBS_READY = (vertexai, GenerativeModel, Tool, grounding)
        return _VERTEX_LIBS_READY
    except Exception as e:
        logger.error(f"Failed to load Vertex AI libraries: {e}")
        _VERTEX_LIBS_READY = False
        return False

class VertexAIClient:
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        self._model_cache = {}

    def get_model(self, model_name: str = "gemini-2.0-flash") -> Optional[Any]:
        """Initialize and return a GenerativeModel instance."""
        libs = _ensure_vertex_libs()
        if not libs:
            return None
        
        vertexai_lib, GenerativeModel, _, _ = libs
        
        # Avoid repeated initialization for the same model/location
        cache_key = (model_name, self.location)
        if cache_key in self._model_cache:
            return self._model_cache[cache_key]

        try:
            vertexai_lib.init(project=self.project_id, location=self.location)
            logger.info(f"Vertex AI Init: project={self.project_id}, location={self.location}, model={model_name}")
            
            # Add Google Search Grounding if available
            tools = []
            if libs[3]: # grounding (GoogleSearchRetrieval)
                from vertexai.generative_models import Tool
                tools = [Tool.from_google_search_retrieval(libs[3]())]
                logger.info("Google Search Grounding Tool enabled.")
            
            model = GenerativeModel(model_name, tools=tools)
            self._model_cache[cache_key] = model
            return model
        except Exception as e:
            logger.error(f"Failed to initialize Vertex AI model {model_name} with tools: {e}")
            return None

    async def generate_content(self, prompt: str, model_name: str = "gemini-2.0-flash", **kwargs) -> Optional[str]:
        """Wrapper for async content generation."""
        model = self.get_model(model_name)
        if not model:
            return None
        
        try:
            response = await model.generate_content_async(prompt, **kwargs)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Vertex AI generation error: {e}")
            return None
