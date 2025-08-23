import requests
import logging
from typing import Optional, Dict, Any
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_GENERATE_URL = f"{OLLAMA_BASE_URL}/api/generate"
OLLAMA_TAGS_URL = f"{OLLAMA_BASE_URL}/api/tags"
MODEL_NAME = "deepseek-r1:1.5b"  # keep; prompt + postprocessing handle domain focus

def is_ollama_running() -> bool:
    try:
        resp = requests.get(OLLAMA_TAGS_URL, timeout=5)
        return resp.status_code == 200
    except Exception:
        return False

def ensure_model_available() -> bool:
    try:
        resp = requests.get(OLLAMA_TAGS_URL, timeout=10)
        if resp.status_code == 200:
            models = resp.json().get("models", [])
            return any(m.get("name") == MODEL_NAME for m in models)
        return False
    except Exception:
        return False

def get_ai_response(prompt: str, lang_code: str = "en", max_retries: int = 2, attempt: int = 0) -> Optional[str]:
    """Get response from Ollama with farming domain + language guard."""
    if not is_ollama_running() or not ensure_model_available():
        return None

    # Language instruction
    lang_instruction = ""
    if lang_code != "en":
        lang_map = {"te": "Telugu", "hi": "Hindi", "ta": "Tamil", "kn": "Kannada"}
        lang_name = lang_map.get(lang_code, "the user's language")
        lang_instruction = f"Respond entirely in {lang_name}."

    # Farming domain guard
    domain_instruction = (
        "You are FarminAi. Only answer farming/agriculture questions (crops, soil, irrigation, pests, diseases, fertilizers, animal husbandry). "
        "If unrelated, state briefly that you only handle farming topics."
    )

    final_prompt = f"{domain_instruction}\n{lang_instruction}\n\n{prompt}"

    payload = {
        "model": MODEL_NAME,
        "prompt": final_prompt,
        "stream": False,
        "options": {
            "temperature": 0.6 if attempt == 0 else 0.4,  # make retries more deterministic
            "top_p": 0.9,
            "top_k": 40,
            "num_predict": 512,
            "repeat_penalty": 1.08,
            # keep only reasoning-stop tokens; do not cut on newlines
            "stop": ["<think>", "<|im_end|>"]
        }
    }

    for retry in range(max_retries):
        try:
            logger.info(f"Ollama request attempt {retry + 1} (temp={payload['options']['temperature']})")
            resp = requests.post(OLLAMA_GENERATE_URL, json=payload, timeout=40)
            resp.raise_for_status()
            result = resp.json()
            ai_response = result.get("response", "").strip()
            if ai_response:
                logger.info(f"Received response: {ai_response[:140]}...")
                return ai_response
        except Exception as e:
            logger.warning(f"Ollama attempt {retry + 1} failed: {e}")
            time.sleep(0.8)

    return None

def test_connection() -> Dict[str, Any]:
    return {
        "ollama_running": is_ollama_running(),
        "model_available": ensure_model_available(),
        "status": "success" if is_ollama_running() and ensure_model_available() else "failed"
    }
