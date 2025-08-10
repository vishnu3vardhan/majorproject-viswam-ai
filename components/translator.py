from deep_translator import GoogleTranslator

def translate_text(text, target_lang):
    try:
        # Translate from auto-detected source to target language
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        print(f"[Translation Error] {e}")
        return text  # Fallback: return original text if translation fails
