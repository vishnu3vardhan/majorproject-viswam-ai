import streamlit as st
from ollama_backend import get_ai_response
from voice_assistant import listen_to_voice
from components.translator import translate_text

def show(dest_lang='en'):
    # Stylized header
    st.markdown(
        f"""
        <div style='text-align: center; padding-bottom: 10px;'>
            <h2 style='color:#2E7D32;'>{translate_text("🌾 Your Smart Assistant for Agriculture", dest_lang)}</h2>
            <p style='color: gray;'>{translate_text("Ask using voice or text to get instant help.", dest_lang)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    ### 🎙️ Voice Assistant ###
    st.markdown(f"### 🎙️ {translate_text('Voice Assistant', dest_lang)}")
    st.markdown(
        f"<p style='color: gray;'>{translate_text('Click the mic and ask your farming question.', dest_lang)}</p>",
        unsafe_allow_html=True
    )

    mic_clicked = st.button(translate_text("🎤 Start Speaking", dest_lang))

    if mic_clicked:
        try:
            query = listen_to_voice()
            if query:
                with st.spinner(translate_text("Processing your voice...", dest_lang)):
                    response = get_ai_response(query)
                    if response:
                        st.success(translate_text("Here's the response:", dest_lang))
                        st.markdown(f"🧠 {translate_text(response, dest_lang)}")
                    else:
                        st.error(translate_text("Sorry, I couldn't understand that.", dest_lang))
            else:
                st.warning(translate_text("No voice detected. Please try again.", dest_lang))
        except Exception:
            st.error(translate_text("Voice assistant failed to start.", dest_lang))

    st.markdown("---")

    ### ⌨️ Text Assistant ###
    st.markdown(f"### ⌨️ {translate_text('Text Assistant', dest_lang)}")
    st.markdown(
        f"<p style='color: gray;'>{translate_text('Type your question below.', dest_lang)}</p>",
        unsafe_allow_html=True
    )

    user_input = st.text_input(
        translate_text("Ask a question", dest_lang),
        placeholder=translate_text("e.g., Best crop for this season?", dest_lang)
    )

    if user_input:
        with st.spinner(translate_text("Thinking...", dest_lang)):
            response = get_ai_response(user_input)
            if response:
                st.success(translate_text("Here's the response:", dest_lang))
                st.markdown(f"🧠 {translate_text(response, dest_lang)}")
            else:
                st.error(translate_text("Sorry, I couldn't find an answer.", dest_lang))

    # Final spacing
    st.markdown("<br><br>", unsafe_allow_html=True)
