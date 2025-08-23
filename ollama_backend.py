import requests
import logging
from typing import Optional, Dict, Any
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_GENERATE_URL = f"{OLLAMA_BASE_URL}/api/generate"
OLLAMA_TAGS_URL = f"{OLLAMA_BASE_URL}/api/tags"
MODEL_NAME = "deepseek-r1:1.5b"

def is_ollama_running() -> bool:
    """Check if Ollama service is running and accessible"""
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=5)
        return response.status_code == 200
    except:
        return False

def ensure_model_available() -> bool:
    """Check if the specified model is available"""
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return any(model.get("name") == MODEL_NAME for model in models)
        return False
    except:
        return False

def get_ai_response(prompt: str, lang_code: str = "en", max_retries: int = 2) -> Optional[str]:
    """Get response from Ollama with optimized parameters"""
    if not is_ollama_running() or not ensure_model_available():
        return None

    # Language instruction
    lang_instruction = ""
    if lang_code != "en":
        lang_map = {"te": "Telugu", "hi": "Hindi", "ta": "Tamil", "kn": "Kannada"}
        lang_name = lang_map.get(lang_code, "the same language as the user")
        lang_instruction = f"Respond in {lang_name}."

    # Add language instruction to prompt
    final_prompt = f"{lang_instruction} {prompt}" if lang_instruction else prompt

    # Optimized parameters for better responses
    payload = {
        "model": MODEL_NAME,
        "prompt": final_prompt,
        "stream": False,
        "options": {
            "temperature": 0.5,
            "top_p": 0.85,
            "top_k": 30,
            "num_predict": 300,
            "repeat_penalty": 1.1,
            "stop": ["\n\n", "###", "<think>", "<|im_end|>"]
        }
    }

    for attempt in range(max_retries):
        try:
            logger.info(f"Sending request to Ollama (attempt {attempt + 1})")
            
            response = requests.post(OLLAMA_GENERATE_URL, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            ai_response = result.get("response", "").strip()
            
            if ai_response:
                logger.info(f"Received response: {ai_response[:100]}...")
                return ai_response
                
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(1)
    
    return None

def test_connection() -> Dict[str, Any]:
    """Test Ollama connection"""
    return {
        "ollama_running": is_ollama_running(),
        "model_available": ensure_model_available(),
        "status": "success" if is_ollama_running() and ensure_model_available() else "failed"
    }