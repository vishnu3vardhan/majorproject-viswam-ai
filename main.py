import streamlit as st
from components import (
    home,
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
    st.image("assests/logo.png", width=180)
    #st.markdown("<h3 style='text-align: left;'>🚜 Farmin-A.I Assistant</h3>", unsafe_allow_html=True)
    #st.markdown("---")

    # Language Toggle
    lang = st.selectbox("🌐 Choose Language", ["English", "తెలుగు"])
    dest_lang = "te" if "తెలుగు" in lang else "en"

    # Translation helper
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except:
            return text  # Fallback in case of translation error

# ---- Navigation ----
pages = [
    "Home",
    "Crop Suggestion",
    "Weather-Based Crop Planning",
    "Disease Detection",
    "Profit Calculator",
    "Farm Record Keeping"
]

translated_labels = [t(page) for page in pages]
selected_label = st.sidebar.radio("📌 " + t("Go to"), translated_labels)
selected_page = pages[translated_labels.index(selected_label)]


# ---- Page Routing ----
with st.spinner(t("Loading...")):
    if selected_page == "Home":
        home.show(dest_lang)
    elif selected_page == "Disease Detection":
        disease_detection.show(dest_lang)
    elif selected_page == "Farm Record Keeping":
        record_keeping.show(dest_lang)
    elif selected_page == "Profit Calculator":
        profit_calculator.show(dest_lang)
    elif selected_page == "Crop Suggestion":
        crop_suggestion.show(dest_lang)
    elif selected_page == "Weather-Based Crop Planning":
        weather_crop_planner.show(dest_lang)

# ---- Footer ----
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "© 2025 Farmin-A.I Assistant | Built for smarter farming 🌾"
    "</div>",
    unsafe_allow_html=True
)
