import streamlit as st
import time
from ollama_backend import get_ai_response
from voice_assistant import listen_to_voice
from components.translator import translate_text


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
                return cleaned or translate_text("Sorry, I couldn't understand your question.", dest_lang)
            else:
                return translate_text("❌ Error: Unable to fetch response. Please try again.", dest_lang)

        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return translate_text(f"❌ Error: Failed after multiple attempts. {e}", dest_lang)


# --- MAIN PAGE FUNCTION ---
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

    # 🎙️ Voice Assistant (Unchanged)
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
                    response = get_ai_response(query, dest_lang)
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

    # ⌨️ Text Assistant (Updated logic only)
    st.markdown(f"### ⌨️ {translate_text('Text Assistant', dest_lang)}")
    st.markdown(
        f"<p style='color: gray;'>{translate_text('Type your question below.', dest_lang)}</p>",
        unsafe_allow_html=True
    )

    # Initialize chat memory
    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_input(
        translate_text("Ask a question", dest_lang),
        placeholder=translate_text("e.g., Best crop for this season?", dest_lang)
    )

    if user_input:
        with st.spinner(translate_text("Thinking...", dest_lang)):
            final_response = query_with_retry(user_input, dest_lang)

        st.success(translate_text("Here's the response:", dest_lang))
        st.markdown(f"🧠 {translate_text(final_response, dest_lang)}")

    # Final spacing
    st.markdown("<br><br>", unsafe_allow_html=True)
