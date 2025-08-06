import streamlit as st
from PIL import Image
import os
from components.translator import translate_text  # Translation helper

def show(dest_lang='en'):
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except:
            return text

    # Header
    st.markdown(
        f"""
        <h1 style='text-align: center;'>
            <img src='https://img.icons8.com/emoji/48/seedling.png' width='35'/>
            {t("Welcome to")} <strong>Farmin-A.I Assistant</strong>
        </h1>
        """,
        unsafe_allow_html=True
    )

    # Card image size
    card_width = 300
    card_height = 200

    # Image loader
    def load_image(path):
        if not os.path.exists(path):
            st.warning(f"⚠️ Image not found: `{path}`")
            return None
        try:
            image = Image.open(path).resize((card_width, card_height))
            return image
        except Exception as e:
            st.error(f"Error loading image from `{path}`: {e}")
            return None

    # ✅ Correct image paths
    cards = [
        ("Crop Suggestion", "assets/crop.jpg", "Crop Suggestion", "🌱"),
        ("Weather Crop Planner", "assets/weather.jpg", "Weather-Based Crop Planning", "🌤️"),
        ("Disease Detection", "assets/disease.jpg", "Disease Detection", "🥬"),
        ("Profit Calculator", "assets/profit.jpg", "Profit Calculator", "💰"),
        ("Record Keeping", "assets/record.jpg", "Farm Record Keeping", "📒"),
        ("Voice & Text Assistant", "assets/assistant.jpg", "Voice & Text Assistant", "🎙️")
    ]

    # Render cards in 2 rows (3 columns each)
    for i in range(0, len(cards), 3):
        cols = st.columns(3)
        for col, (title, img_path, page, icon) in zip(cols, cards[i:i+3]):
            with col:
                img = load_image(img_path)

                if isinstance(img, Image.Image):
                    st.image(img, use_container_width=True)
                else:
                    st.warning(f"⚠️ Unable to display image for: {title}")
                    st.text(f"(Missing image: {img_path})")  # Optional debug line

                st.markdown(f"### {icon} {t(title)}", unsafe_allow_html=True)
                if st.button(t(f"Open {title}")):
                    st.session_state["selected_page"] = page
                    st.session_state["navigated_from_card"] = True
                    st.rerun()
