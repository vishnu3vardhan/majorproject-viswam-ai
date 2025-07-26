from googletrans import Translator

translator = Translator()

def translate_text(text, dest_lang='te'):
    try:
        return translator.translate(text, dest=dest_lang).text
    except Exception:
        return text
