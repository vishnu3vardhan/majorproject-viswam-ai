# pages/home.py
import streamlit as st
from ollama_backend import get_ai_response
from voice_assistant import listen_to_voice

def show():
    st.header("🤖 FarminAI Assistant")
    st.write("Your offline assistant for Agriculture, Dairy, and Poultry.")

    languages = {"English": "en", "తెలుగు": "te", "हिंदी": "hi"}
    lang = st.selectbox("🌐 Select Language", list(languages.keys()))
    lang_code = languages[lang]

    if st.button("🎤 Speak"):
        user_input = listen_to_voice()
        st.text_area("Your Voice Input", user_input)
    else:
        user_input = st.text_input("💬 Type your question:")

    if st.button("Ask AI"):
        with st.spinner("Thinking..."):
            response = get_ai_response(user_input, lang_code)
        st.success(response)
