import streamlit as st
from PIL import Image
import os
from components.translator import translate_text

def show(dest_lang='en'):
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except:
            return text

    # Header
    st.markdown(
        f"""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h1 style='display: inline-flex; align-items: center; gap: 10px;'>
                <img src='https://img.icons8.com/emoji/48/seedling.png' width='35'/>
                {t("Welcome to")} <span style='color: #2e8b57;'>Farmin-A.I Assistant</span>
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Custom card styling
    st.markdown("""
        <style>
            
            .card:hover {
                transform: scale(1.03);
                box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            }
            .card-title {
                font-weight: 600;
                font-size: 18px;
                margin-top: 10px;
            }
            .stButton > button {
                background-color: #2e8b57;
                color: white;
                font-size: 13px;
                padding: 4px 10px;
                border-radius: 6px;
                margin-top: 8px;
            }
            .stButton > button:hover {
                background-color: #276a46;
            }
        </style>
    """, unsafe_allow_html=True)

    CARD_WIDTH = 300
    CARD_HEIGHT = 200

    PLACEHOLDER_IMAGES = {
        "crop": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=300&h=200&fit=crop",
        "weather": "https://images.unsplash.com/photo-1561484930-974554019ade?w=300&h=200&fit=crop",
        "disease": "https://images.unsplash.com/photo-1604977046806-87b8b1b5b533?w=300&h=200&fit=crop",
        "profit": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=300&h=200&fit=crop",
        "record": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=300&h=200&fit=crop",
        "assistant": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=300&h=200&fit=crop"
    }

    def load_image(card_key, path):
        try:
            if os.path.exists(path):
                img = Image.open(path)
                img = img.resize((CARD_WIDTH, CARD_HEIGHT))
                return img
            return PLACEHOLDER_IMAGES[card_key.lower().replace(" ", "_").split(".")[0]]
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")
            return None

    cards = [
        ("Crop Suggestion", "assets/crop.jpg", "Crop Suggestion", "🌱"),
        ("Weather Crop Planner", "assets/weather.jpg", "Weather-Based Crop Planning", "🌤️"),
        ("Disease Detection", "assets/disease.jpg", "Disease Detection", "🥬"),
        ("Profit Calculator", "assets/profit.jpg", "Profit Calculator", "💰"),
        ("Record Keeping", "assets/record.jpg", "Farm Record Keeping", "📒"),
        ("Voice & Text Assistant", "assets/assistant.jpg", "Voice & Text Assistant", "🎙️")
    ]

    # Render 3 cards per row
    for i in range(0, len(cards), 3):
        cols = st.columns(3)
        for col, (title, img_path, page, icon) in zip(cols, cards[i:i+3]):
            with col:
                st.markdown("<div class='card'>", unsafe_allow_html=True)

                img = load_image(title, img_path)
                if isinstance(img, Image.Image):
                    st.image(img, width=CARD_WIDTH)
                elif isinstance(img, str):
                    st.image(img, width=CARD_WIDTH)
                else:
                    st.markdown(
                        f"<div style='width:{CARD_WIDTH}px; height:{CARD_HEIGHT}px; "
                        f"display:flex; align-items:center; justify-content:center; background:#f0f2f6;'>"
                        f"<h1>{icon}</h1></div>",
                        unsafe_allow_html=True
                    )

                st.markdown(f"<div class='card-title'>{icon} {t(title)}</div>", unsafe_allow_html=True)

                if st.button(t(f"Open {title}"), key=f"btn_{page.lower().replace(' ', '_')}"):
                    st.session_state["selected_page"] = page
                    st.session_state["navigated_from_card"] = True

                st.markdown("</div>", unsafe_allow_html=True)

    # Safely rerun after layout
    if st.session_state.get("navigated_from_card"):
        st.session_state["navigated_from_card"] = False
        st.rerun()
