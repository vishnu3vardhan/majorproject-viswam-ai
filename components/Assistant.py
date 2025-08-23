import streamlit as st
import time
import re
import logging
from ollama_backend import get_ai_response
from voice_assistant import listen_to_voice
from components.translator import translate_text
from components.feedback_button import feedback_button

logger = logging.getLogger(__name__)

STOPWORDS = {
    "what","is","are","the","a","an","of","and","or","to","in","on","about","for",
    "please","tell","me","explain","define","meaning","meaningof","how","does","do",
    "with","by","from","as","at","that","this","those","these","it","its","into"
}

def extract_keywords(text: str):
    """Very lightweight keyword extractor (no external libs)."""
    if not text:
        return set()
    txt = re.sub(r"[^a-zA-Z0-9\s\-]", " ", text.lower())
    parts = [p.strip("-") for p in txt.split()]
    return {p for p in parts if p and p not in STOPWORDS and len(p) > 2}

def is_definition_query(text: str) -> bool:
    """Detect 'define/what is/meaning of' style queries."""
    if not text:
        return False
    t = text.strip().lower()
    return bool(re.match(r"^\s*(what\s+is|what\s+are|define|definition|meaning\s+of)\b", t))

def format_prompt(messages, system_prompt: str, latest_user: str) -> str:
    """
    Include short conversation context AND explicitly quote the latest user question
    to stop the model from answering previous turns.
    """
    formatted = system_prompt.rstrip() + "\n\n"
    if messages:
        formatted += "Conversation context (most recent first):\n"
        for msg in messages[-8:]:
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted += f"{role}: {msg['content']}\n"

    formatted += "\nLatest user question (answer ONLY this):\n"
    formatted += f"\"{latest_user.strip()}\"\n\n"
    formatted += "Assistant:"
    return formatted

def clean_response(response: str) -> str:
    """Clean but do not over-prune."""
    if not response:
        return None
    # Remove hidden reasoning tags if any
    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL | re.IGNORECASE)
    response = re.sub(r'<\|im_start\|>.*?<\|im_end\|>', '', response, flags=re.DOTALL)

    # Light trim of leading conversational fillers
    cleaned = response.strip()
    cleaned = re.sub(r'^(well|okay|ok|so|now)[,:\s]+', '', cleaned, flags=re.IGNORECASE)
    return cleaned if cleaned else None

def enforce_topic_coverage(user_input: str, reply: str) -> bool:
    """Ensure reply mentions at least one key term from the user input."""
    if not user_input or not reply:
        return False
    q_keys = extract_keywords(user_input)
    # If no useful keywords, accept
    if not q_keys:
        return True
    # Basic coverage: any keyword appears in reply (substring match, case-insensitive)
    text = reply.lower()
    return any(k in text for k in q_keys)

def build_definition_style_instruction(latest_user: str) -> str:
    """Instruction block for definition queries."""
    return (
        "If the question asks for a definition (e.g., starts with 'what is', 'what are', 'define', or 'meaning of'), "
        "answer in this structure:\n"
        "1) Definition: one clear sentence using the exact term.\n"
        "2) Key points: 3 concise bullets focused on practical farming relevance.\n"
        "Avoid repeating earlier terms unless necessary.\n"
    )

def query_with_retry(user_input: str, dest_lang="en", retries=2) -> str:
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except Exception:
            return text

    # Farming-specific system prompt with strong targeting to latest question
    system_prompt = (
        "You are FarminAi, a helpful farming assistant.\n"
        "- Only answer farming and agriculture-related topics (crops, soil, water, irrigation, pests, diseases, fertilizers, animal husbandry).\n"
        "- Be practical and concise. Use bullet points or short steps.\n"
        "- Answer ONLY the latest user question quoted below.\n"
        "- If unsure, briefly ask a targeted clarification instead of guessing.\n"
        "- Always respond in the user's language."
    )

    # Add definition-style scaffolding if needed
    if is_definition_query(user_input):
        system_prompt += "\n\n" + build_definition_style_instruction(user_input)

    # Expanded farming knowledge for final fallback
    fallback_knowledge = {
        "farming": "Farming is the practice of cultivating land to grow crops and raising animals for food, fiber, and other products.",
        "organic": "Organic farming avoids synthetic fertilizers and pesticides; it relies on compost, crop rotation, resistant varieties, and biological pest control.",
        "soil": "Healthy soil improves yields. Add compost or manure, rotate crops, keep ground covered, and avoid over-tillage to protect structure and microbes.",
        "water": "Good water management reduces stress and waste. Use drip irrigation, mulch to reduce evaporation, schedule watering by soil moisture.",
        "irrigation": "Irrigation supplies water during dry periods. Common systems: drip (efficient), sprinkler (flexible), furrow/flood (low-cost but less efficient).",
        "pest": "Pests reduce yields by feeding on crops and spreading disease. Use integrated pest management: monitoring, traps, cultural practices, and targeted controls.",
        "fertilizer": "Fertilizers add nutrients. Common types: nitrogen (urea), phosphorus (DAP/SSP), potassium (MOP), and organics (compost/manure). Apply by soil test.",
        "crops": "Crops are plants grown for food, feed, fiber, or biofuel. Examples: cereals (wheat, rice, maize), pulses (chickpea), oilseeds (mustard), vegetables, fruits."
    }

    # Outer attempts (high-level prompt variants)
    for attempt in range(retries):
        try:
            # Build prompt with conversation + explicit latest question
            messages = st.session_state.get("messages", [])
            formatted_prompt = format_prompt(messages, system_prompt, user_input)

            raw = get_ai_response(formatted_prompt, dest_lang, attempt=attempt)
            if not raw:
                continue

            cleaned = clean_response(raw) or raw.strip()

            # If reply doesn't cover the topic terms, do a single targeted correction
            if not enforce_topic_coverage(user_input, cleaned):
                logger.info("Topic coverage check failed; issuing targeted correction prompt.")
                missing_terms = ", ".join(sorted(extract_keywords(user_input)))
                corrective_prompt = (
                    system_prompt
                    + "\n\nConversation note: Your previous draft did not explicitly address these keywords: "
                    + f"{missing_terms}.\n"
                    "Rewrite a direct 2–4 sentence answer that explicitly mentions these keywords and focuses on farming practice.\n\n"
                    f'Latest user question: "{user_input}"\n\nAssistant:'
                )
                corrected = get_ai_response(corrective_prompt, dest_lang, attempt=attempt+1)
                corrected = clean_response(corrected) if corrected else None
                if corrected and enforce_topic_coverage(user_input, corrected):
                    return corrected
                # If still not good, fall back to first cleaned answer
                return cleaned

            return cleaned

        except Exception as e:
            logger.error(f"query_with_retry attempt {attempt+1} failed: {e}")
            time.sleep(0.8)

    # Final fallback: dictionary match
    q_lower = user_input.lower()
    for keyword, tip in fallback_knowledge.items():
        if keyword in q_lower or (keyword.endswith("s") and keyword[:-1] in q_lower):
            return t(tip)

    return t("I couldn't find an exact answer. Is your question about crops, soil, irrigation, pests, fertilizers, or animals? Please specify so I can be precise.")

def show(dest_lang='en'):
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except Exception:
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

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Voice Assistant
    st.markdown(f"### 🎙️ {t('Voice Assistant')}")
    col1, _ = st.columns([1, 4])
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
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**👤 You:** {message['content']}")
        else:
            st.markdown(f"**🤖 Assistant:** {message['content']}")
        st.markdown("---")

    user_input = st.chat_input(t("Ask about farming..."), key="chat_input")

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

    if st.session_state.messages:
        if st.button(t("🗑️ Clear Chat"), type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
