import streamlit as st
import time
import re
from ollama_backend import get_ai_response
from voice_assistant import listen_to_voice
from components.translator import translate_text
from components.feedback_button import feedback_button


def format_conversational_prompt(messages, system_prompt):
    """Format the prompt with clear instructions"""
    # Start with system prompt
    formatted_prompt = system_prompt + "\n\n"
    
    # Add conversation context
    if messages:
        formatted_prompt += "Conversation context:\n"
        user_messages = [msg for msg in messages if msg["role"] == "user"]
        recent_messages = user_messages[-3:]  # Last 3 user messages
        
        for msg in recent_messages:
            formatted_prompt += f"User: {msg['content']}\n"
    
    # Add current instruction
    formatted_prompt += "\nPlease provide a direct, helpful response to the user's latest question.\n\nAssistant:"
    
    return formatted_prompt


def clean_response(response: str) -> str:
    """Clean response without being overly aggressive"""
    if not response:
        return None
    
    # Remove thinking tags
    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL | re.IGNORECASE)
    response = re.sub(r'<\|im_start\|>.*?<\|im_end\|>', '', response, flags=re.DOTALL)
    
    # Remove common thinking patterns at the start
    thinking_patterns = [
        r'^(okay|ok|alright|well|so|now|first|actually|basically|hmm|hm)[,\s\.\-]*',
        r'^i (need to|should|think|believe|wonder|guess|suppose)',
        r'^let me (think|see|explain|try|answer)',
        r'^the user (asked|wants|is asking)',
        r'^the question (is|was|seems)',
        r'^as an ai (assistant|model)',
    ]
    
    cleaned = response.strip()
    
    for pattern in thinking_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE).strip()
    
    # Remove leading punctuation
    cleaned = re.sub(r'^[,\s\.\-!?:;]+', '', cleaned)
    
    # If we have a reasonable response, return it
    if cleaned and len(cleaned) > 10:
        return cleaned
    
    return None


def query_with_retry(user_input: str, dest_lang="en", retries=2) -> str:
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except:
            return text
            
    # Clear, direct system prompt
    system_prompt = """You are FarminAi, a helpful farming assistant. Provide clear, practical advice about agriculture and farming.

IMPORTANT:
- Answer directly without thinking aloud
- No internal monologue or self-reference
- Be concise and helpful
- Use the same language as the user
- Focus on practical farming information"""

    for attempt in range(retries):
        try:
            # Format prompt
            formatted_prompt = format_conversational_prompt(
                st.session_state.messages, system_prompt
            )

            # Get response
            response = get_ai_response(formatted_prompt, dest_lang)

            if response:
                # Clean response
                cleaned = clean_response(response)
                
                if cleaned:
                    return cleaned
                
                # If cleaning removed everything, try original response
                if len(response.strip()) > 20:
                    return response.strip()
            
            # If we get here, try a different approach
            if attempt == 0:
                # Try a more direct prompt on second attempt
                direct_prompt = f"{system_prompt}\n\nUser: {user_input}\n\nAssistant:"
                response = get_ai_response(direct_prompt, dest_lang)
                if response:
                    cleaned = clean_response(response)
                    if cleaned:
                        return cleaned
                    if len(response.strip()) > 20:
                        return response.strip()
                        
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(1)
    
    # Final fallback - provide actual information
    if "organic" in user_input.lower():
        return t("Organic farming avoids synthetic chemicals and uses natural methods for soil health and pest control.")
    elif "farming" in user_input.lower():
        return t("Farming is cultivating land to grow crops and raise animals for food, fiber, and other products.")
    else:
        return t("I can help with farming questions about crops, soil, animals, or agricultural practices.")


def show(dest_lang='en'):
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except:
            return text

    feedback_button("voice_assistant")
    
    st.markdown(
        f"""
        <div style='text-align: center; padding-bottom: 10px;'>
            <h2 style='color:#2E7D32;'>{t("🌾 FarminAi Assistant")}</h2>
            <p style='color: gray;'>{t("Get expert farming advice")}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Initialize chat memory
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Voice Assistant
    st.markdown(f"### 🎙️ {t('Voice Assistant')}")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        mic_clicked = st.button(t("🎤 Speak"), use_container_width=True)

    if mic_clicked:
        try:
            with st.spinner(t("Listening...")):
                query = listen_to_voice()
            
            if query and query.strip():
                st.session_state.messages.append({"role": "user", "content": query})
                
                with st.spinner(t("Processing...")):
                    response = query_with_retry(query, dest_lang)
                
                if response:
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.markdown(f"**🤖 Assistant:** {response}")
            else:
                st.warning(t("Please speak clearly or try typing your question."))
                
        except Exception:
            st.error(t("Voice input unavailable. Please type your question."))

    st.markdown("---")

    # Text Assistant
    st.markdown(f"### ⌨️ {t('Text Assistant')}")

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**👤 You:** {message['content']}")
        else:
            st.markdown(f"**🤖 Assistant:** {message['content']}")
        st.markdown("---")

    # Text input
    user_input = st.chat_input(
        t("Ask about farming..."),
        key="chat_input"
    )

    if user_input and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.markdown(f"**👤 You:** {user_input}")
        st.markdown("---")
        
        with st.spinner(t("Thinking...")):
            response = query_with_retry(user_input, dest_lang)
        
        if response:
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.markdown(f"**🤖 Assistant:** {response}")
        else:
            st.error(t("Please try again or ask a different question."))
        
        st.markdown("---")

    # Clear chat
    if st.session_state.messages:
        if st.button(t("🗑️ Clear Chat"), type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)