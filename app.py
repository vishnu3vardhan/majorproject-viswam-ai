import streamlit as st
from ollama_backend import get_ai_response
from detection import predict_disease
from db import add_record, get_records
from voice_assistant import listen_to_voice

st.set_page_config(page_title="🌾 Farmer AI Assistant", layout="wide")
# 🌐 Language Selector
languages = {"English": "en", "తెలుగు": "te", "हिंदी": "hi"}
lang = st.sidebar.selectbox("🌐 Language", list(languages.keys()))
lang_code = languages[lang]

st.title("🤖 Farmer & Dairy AI Assistant")
st.write("Your offline assistant for Agriculture, Dairy, and Poultry.")

# 🗣️ Voice Command
if st.button("🎤 Speak"):
    user_input = listen_to_voice()
    st.text_area("Your Voice Input", user_input)
else:
    user_input = st.text_input("💬 Type your question:")

if st.button("Ask AI"):
    with st.spinner("Thinking..."):
        response = get_ai_response(user_input, lang_code)
    st.success(response)

# 📷 Disease Detection
st.subheader("🐄 Disease Detection (Upload Image)")
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png"])
if uploaded_file and st.button("🔍 Predict Disease"):
    result = predict_disease(uploaded_file, model_type="poultry")
    st.info(f"Prediction: **{result}**")

# 📒 Farmer Records
st.subheader("📒 Farm Record Keeping")
record_type = st.selectbox("Type", ["Dairy", "Poultry", "Crop"])
detail = st.text_input("Details")
if st.button("💾 Save Record"):
    add_record(record_type, detail, "2025-07-16")
    st.success("Record saved!")
if st.checkbox("📜 Show Records"):
    records = get_records()
    st.table(records)

