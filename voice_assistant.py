import speech_recognition as sr

def listen_to_voice():
    """Capture voice input and convert it to text (offline)."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Use Sphinx for offline recognition
        text = recognizer.recognize_sphinx(audio)
        print(f"📝 You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return "Sorry, I couldn’t understand you."
    except sr.RequestError as e:
        print(f"⚠ Sphinx error; {e}")
        return "Speech recognition failed."

