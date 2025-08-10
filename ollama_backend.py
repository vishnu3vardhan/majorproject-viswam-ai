import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:1.5b"  # Or "mistral", "gemma", etc.

def get_ai_response(prompt, lang_code="en"):
    # Optional: Language hinting
    if lang_code == "te":
        prompt = "తెలుగులో సమాధానం ఇవ్వండి: " + prompt
    elif lang_code == "hi":
        prompt = "हिंदी में उत्तर दें: " + prompt

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False  # Get full response at once
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip() or None
    except Exception as e:
        print(f"[get_ai_response ERROR] {e}")
        return None
