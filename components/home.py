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

    # Improved image loader with more error handling
    def load_image(path):
        try:
            if not os.path.exists(path):
                # Try alternative path if running in different environment
                alt_path = os.path.join(os.path.dirname(__file__), path)
                if not os.path.exists(alt_path):
                    st.warning(f"⚠️ Image not found: `{path}`")
                    return None
                path = alt_path
            
            image = Image.open(path)
            # Maintain aspect ratio while resizing
            image.thumbnail((card_width, card_height))
            return image
        except Exception as e:
            st.error(f"Error loading image from `{path}`: {str(e)}")
            return None

    # Card definitions - using relative paths
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
                # Create container for consistent card sizing
                with st.container(border=True, height=300):
                    img = load_image(img_path)

                    if img is not None:
                        st.image(img, use_column_width=True)
                    else:
                        # Display placeholder if image fails to load
                        st.markdown(f"<div style='height:{card_height}px; display:flex; align-items:center; justify-content:center;'>"
                                    f"<h2>{icon}</h2></div>", unsafe_allow_html=True)
                        st.warning(t("Image not available"))

                    st.markdown(f"### {icon} {t(title)}")
                    if st.button(t(f"Open {title}"), use_container_width=True):
                        st.session_state["selected_page"] = page
                        st.session_state["navigated_from_card"] = True
                        st.rerun()
