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
st.set_page_config(page_title="FarminAI Assistant", page_icon="assests/logo.png", layout="wide")

# Sidebar Branding
st.sidebar.image("assests/logo.png", width=120)
st.sidebar.title("🚜 FarminAI Navigation")

# Language Toggle
lang = st.sidebar.selectbox("🌐 Language", ("English", "Telugu"))
dest_lang = "te" if lang == "Telugu" else "en"

# Simple Translator Shortcut
def t(text):
    return translate_text(text, dest_lang)

# Internal page keys
pages = [
    "Home",
    "Disease Detection",
    "Farm Record Keeping",
    "Profit Calculator",
    "Crop Suggestion",
    "Weather-Based Crop Planning"
]

# Translated labels to show in sidebar
translated_labels = [t(page) for page in pages]

# Display translated names but store the index
selected_label = st.sidebar.radio(t("Go to"), translated_labels)
selected_page = pages[translated_labels.index(selected_label)]

# Route to the selected page
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
