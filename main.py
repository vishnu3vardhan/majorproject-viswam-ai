import streamlit as st
from components.translator import translate_text

# Import individual components directly instead of through __init__
import components.home as home
import components.Assistant as Assistant
import components.record_keeping as record_keeping
import components.disease_detection as disease_detection
import components.weather_crop_planner as weather_crop_planner
import components.profit_calculator as profit_calculator
import components.crop_suggestion as crop_suggestion

# Import feedback components with fallback
try:
    import components.feedback_page as feedback_page
    import components.feedback_button as feedback_button
    FEEDBACK_AVAILABLE = True
except ImportError:
    FEEDBACK_AVAILABLE = False
    # Create fallback functions if feedback components are not available
    def feedback_page(dest_lang='en'):
        def t(text):
            try:
                return translate_text(text, dest_lang)
            except:
                return text
        st.title(t("Feedback"))
        st.info(t("Feedback feature is currently unavailable. Please check if all components are properly installed."))
    
    def feedback_button(dest_lang='en'):
        pass  # Do nothing if feedback button is not available

# Page Config
st.set_page_config(page_title="Farmin-A.I Assistant", page_icon="assests/favicon.png", layout="wide")

# Initialize session state for navigation
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Home"
if "navigated_from_card" not in st.session_state:
    st.session_state["navigated_from_card"] = False
if "last_lang" not in st.session_state:
    st.session_state["last_lang"] = "en"

# ---- Sidebar Styling ----
with st.sidebar:
    st.image("assets/favicon.png", width=200)
    
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

# Add Feedback page to navigation if available
if FEEDBACK_AVAILABLE:
    pages.append("Feedback")

translated_labels = [t(p) for p in pages]

# ---- Sidebar Navigation ----
# Get the current index based on selected_page to keep radio button in sync
current_index = pages.index(st.session_state["selected_page"]) if st.session_state["selected_page"] in pages else 0

selected_label = st.sidebar.radio("📌 " + t("Go to"), translated_labels, index=current_index, key="sidebar_nav")
selected_page_from_sidebar = pages[translated_labels.index(selected_label)]

# Handle language change rerun only when language actually changes
if st.session_state["last_lang"] != dest_lang:
    st.session_state["last_lang"] = dest_lang
    st.session_state["selected_page"] = selected_page_from_sidebar
    st.rerun()

# Sidebar changes should override card clicks
if not st.session_state["navigated_from_card"]:
    st.session_state["selected_page"] = selected_page_from_sidebar

# Reset card navigation flag after use
if st.session_state["navigated_from_card"]:
    st.session_state["navigated_from_card"] = False

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
    elif current_page == "Feedback" and FEEDBACK_AVAILABLE:
        feedback_page.feedback_page(dest_lang)  # Call the function from the module

# ---- Footer ----
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "© 2025 Farmin-A.I Assistant | Built for smarter farming 🌾"
    "</div>",
    unsafe_allow_html=True
)