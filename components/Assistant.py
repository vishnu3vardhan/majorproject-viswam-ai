import streamlit as st
import time
from ollama_backend import get_ai_response
from voice_assistant import listen_to_voice
from components.translator import translate_text
from components.feedback_button import feedback_button  # Import the feedback component


# --- Helper: Format conversational history for prompt ---
def format_conversational_prompt(messages, system_prompt):
    last_user_message = ""
    for msg in reversed(messages):
        if msg["role"] == "user":
            last_user_message = msg["content"].strip()
            break

    formatted_prompt = f"{system_prompt.strip()}\n\n"
    formatted_prompt += f"Answer the following question concisely and directly:\n{last_user_message}\n"
    return formatted_prompt


# --- Helper: Retry wrapper ---
def query_with_retry(prompt: str, dest_lang="en", retries=3) -> str:
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except:
            return text
            
    system_prompt = (
        "You are FarminAi, a helpful and friendly AI assistant for farmers. "
        "Provide clear, practical, and localized advice on farming-related topics such as crops, soil health, weather, irrigation, "
        "pest and disease management, government schemes, and market prices. "
        "Your responses should be brief, easy to understand, and relevant to the farmer's local conditions whenever possible. "
        "Use simple language, avoid jargon, and always aim to be kind, respectful, and accurate. "
        "If the user's question lacks detail, ask clarifying questions to provide better help. "
        "If you don't know something, say so honestly rather than guessing."
        "Adapt your responses based on regional practices, climate, and crops when such context is available."
    )

    for attempt in range(retries):
        try:
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Add latest user prompt to history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Format prompt
            formatted_prompt = format_conversational_prompt(
                st.session_state.messages, system_prompt
            )

            # Get response from backend
            response = get_ai_response(formatted_prompt, dest_lang)

            if response:
                # Clean output (remove accidental echoes or prefixes)
                cleaned = response.replace("Assistant:", "").replace("User:", "").split("<think>")[-1].strip()

                # Append assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": cleaned})
                return cleaned or t("Sorry, I couldn't understand your question.")
            else:
                return t("❌ Error: Unable to fetch response. Please try again.")

        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return t(f"❌ Error: Failed after multiple attempts. {e}")


# --- MAIN PAGE FUNCTION ---
def show(dest_lang='en'):
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except:
            return text

    # Add the feedback button at the top
    feedback_button("voice_assistant")
    
    # Stylized header
    st.markdown(
        f"""
        <div style='text-align: center; padding-bottom: 10px;'>
            <h2 style='color:#2E7D32;'>{t("🌾 Your Smart Assistant for Agriculture")}</h2>
            <p style='color: gray;'>{t("Ask using voice or text to get instant help.")}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # 🎙️ Voice Assistant
    st.markdown(f"### 🎙️ {t('Voice Assistant')}")
    st.markdown(
        f"<p style='color: gray;'>{t('Click the mic and ask your farming question.')}</p>",
        unsafe_allow_html=True
    )

    mic_clicked = st.button(t("🎤 Start Speaking"))

    if mic_clicked:
        try:
            query = listen_to_voice()
            if query:
                with st.spinner(t("Processing your voice...")):
                    response = get_ai_response(query, dest_lang)
                    if response:
                        st.success(t("Here's the response:"))
                        st.markdown(f"🧠 {t(response)}")
                    else:
                        st.error(t("Sorry, I couldn't understand that."))
            else:
                st.warning(t("No voice detected. Please try again."))
        except Exception:
            st.error(t("Voice assistant failed to start."))

    st.markdown("---")

    # ⌨️ Text Assistant
    st.markdown(f"### ⌨️ {t('Text Assistant')}")
    st.markdown(
        f"<p style='color: gray;'>{t('Type your question below.')}</p>",
        unsafe_allow_html=True
    )

    # Initialize chat memory
    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_input(
        t("Ask a question"),
        placeholder=t("e.g., Best crop for this season?")
    )

    if user_input:
        with st.spinner(t("Thinking...")):
            final_response = query_with_retry(user_input, dest_lang)

        st.success(t("Here's the response:"))
        st.markdown(f"🧠 {t(final_response)}")

    # Final spacing
    st.markdown("<br><br>", unsafe_allow_html=True)