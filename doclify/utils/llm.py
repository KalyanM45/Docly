from google import genai
import os
from doclify.config.constants import CliConfig
from doclify.utils.utils import get_prompt
from pydantic import BaseModel
from typing import Optional, Type, Any
from doclify.utils.logger import get_logger

logger = get_logger(__name__)

_client = None

def _get_client():
    """Lazy initialization of the Gemini client."""
    global _client
    if _client is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("GOOGLE_API_KEY environment variable is missing.")
            raise ValueError("GOOGLE_API_KEY environment variable is not set.")
        
        logger.info("Initializing new Gemini genai.Client")
        _client = genai.Client(api_key=api_key)
    return _client

def generate_doc(code_content: str, type: str, json_format: Optional[Type[Any]] = None) -> str:    
    try:
        client = _get_client()
        
        prompt_name = type
        prompt = get_prompt(prompt_name)

        if json_format:
            response = client.models.generate_content(
                model=CliConfig.MODEL_NAME,
                contents=prompt + code_content,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": json_format.model_json_schema(),
                },
            )
            logger.info(f"LLM call successful (Structured Output). Metadata: {response.usage_metadata}")
            return response.text
            
        else:
            response = client.models.generate_content(
                model=CliConfig.MODEL_NAME,
                contents=prompt + code_content
            )
            logger.info(f"LLM call successful (Standard Output). Metadata: {response.usage_metadata}")
            return response.text
            
    except Exception as e:
        logger.error(f"Failed to generate documentation: {str(e)}", exc_info=True)
        raise ValueError(f"Failed to generate documentation: {e}")