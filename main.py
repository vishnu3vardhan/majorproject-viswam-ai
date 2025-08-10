import streamlit as st
from components import (
    home,
    Assistant,
    record_keeping,
    disease_detection,
    weather_crop_planner,
    profit_calculator,
    crop_suggestion
)
from components.translator import translate_text

# Page Config
st.set_page_config(page_title="Farmin-A.I Assistant", page_icon="assests/favicon.png", layout="wide")

# ---- Sidebar Styling ----
with st.sidebar:
    st.image("assets/logo.png", width=180)
    
    # Language toggle
    lang = st.selectbox("🌐 Choose Language", ["English", "తెలుగు"])
    dest_lang = "te" if lang == "తెలుగు" else "en"
    st.session_state["selected_lang"] = dest_lang

    # Translator function
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except:
            return text

# ---- Page Labels and Mapping ----
pages = [
    "Home",
    "Voice & Text Assistant",
    "Crop Suggestion",
    "Weather-Based Crop Planning",
    "Disease Detection",
    "Profit Calculator",
    "Farm Record Keeping"
]
translated_labels = [t(p) for p in pages]

# ---- Initialize Session State ----
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Home"

# ---- Sidebar Navigation ----
selected_label = st.sidebar.radio("📌 " + t("Go to"), translated_labels)
selected_page_from_sidebar = pages[translated_labels.index(selected_label)]

# Sidebar changes should override card clicks
if "navigated_from_card" not in st.session_state:
    st.session_state["selected_page"] = selected_page_from_sidebar

# Remove card navigation flag after routing
if "navigated_from_card" in st.session_state:
    del st.session_state["navigated_from_card"]

# ---- Page Routing ----
with st.spinner(t("Loading...")):
    current_page = st.session_state["selected_page"]
    if current_page == "Home":
        home.show(dest_lang)
    elif current_page == "Voice & Text Assistant":
        Assistant.show(dest_lang)
    elif current_page == "Crop Suggestion":
        crop_suggestion.show(dest_lang)
    elif current_page == "Weather-Based Crop Planning":
        weather_crop_planner.show(dest_lang)
    elif current_page == "Disease Detection":
        disease_detection.show(dest_lang)
    elif current_page == "Profit Calculator":
        profit_calculator.show(dest_lang)
    elif current_page == "Farm Record Keeping":
        record_keeping.show(dest_lang)

# ---- Footer ----
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "© 2025 Farmin-A.I Assistant | Built for smarter farming 🌾"
    "</div>",
    unsafe_allow_html=True
)
