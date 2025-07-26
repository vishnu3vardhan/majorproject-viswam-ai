# pages/home.py
import streamlit as st
from ollama_backend import get_ai_response
from voice_assistant import listen_to_voice
from components.translator import translate_text

def show(dest_lang='en'):
    st.header(translate_text("🤖 FarminAI Assistant", dest_lang))

    st.write(translate_text("Your offline assistant for Agriculture, Dairy, and Poultry.", dest_lang))

    # Voice Assistant Button
    if st.button(translate_text("Start Voice Assistant", dest_lang)):
        query = listen_to_voice()
        response = get_ai_response(query)
        st.write(translate_text(response, dest_lang))

    # Text-based Assistant Input
    user_input = st.text_input(translate_text("Ask a question", dest_lang))
    if user_input:
        response = get_ai_response(user_input)
        st.write(translate_text(response, dest_lang))
