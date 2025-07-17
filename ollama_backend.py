import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama2"  # Or "mistral", "gemma", etc.

def get_ai_response(prompt, lang_code="en"):
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
        return result.get("response", "").strip()
    except Exception as e:
        return f"⚠️ Error: {e}"


