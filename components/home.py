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

    # Header with improved styling
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

    # Card configuration
    CARD_WIDTH = 300
    CARD_HEIGHT = 200
    PLACEHOLDER_IMAGES = {
        "crop": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=300",
        "weather": "https://images.unsplash.com/photo-1561484930-974554019ade?w=300",
        "disease": "https://images.unsplash.com/photo-1604977046806-87b8b1b5b533?w=300",
        "profit": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=300",
        "record": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=300",
        "assistant": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=300"
    }

    def load_image(card_key, path):
        try:
            # First try local assets
            if os.path.exists(path):
                img = Image.open(path)
                img.thumbnail((CARD_WIDTH, CARD_HEIGHT))
                return img
            
            # Fallback to online placeholder
            st.warning(f"⚠️ Local image not found, using placeholder: {path}")
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

    # Card grid layout
    for i in range(0, len(cards), 3):
        cols = st.columns(3)
        for col, (title, img_path, page, icon) in zip(cols, cards[i:i+3]):
            with col:
                # Card container with consistent styling
                with st.container():
                    st.markdown(
                        f"""
                        <style>
                            div[data-testid="stVerticalBlock"] {{
                                border: 1px solid #e6e6e6;
                                border-radius: 8px;
                                padding: 15px;
                                height: 320px;
                                transition: all 0.3s ease;
                            }}
                            div[data-testid="stVerticalBlock"]:hover {{
                                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                                transform: translateY(-2px);
                            }}
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Load image with fallback
                    img = load_image(title, img_path)
                    
                    if isinstance(img, Image.Image):
                        st.image(img, use_column_width=True)
                    elif isinstance(img, str):  # URL fallback
                        st.image(img, use_column_width=True)
                    else:
                        st.markdown(
                            f"<div style='height:{CARD_HEIGHT}px; display:flex; align-items:center; justify-content:center; background:#f0f2f6; border-radius:8px;'>"
                            f"<h1 style='font-size:3rem;'>{icon}</h1></div>",
                            unsafe_allow_html=True
                        )

                    # Card content
                    st.markdown(f"<h3 style='text-align:center; margin-top:10px;'>{icon} {t(title)}</h3>", unsafe_allow_html=True)
                    
                    if st.button(
                        t(f"Open {title}"), 
                        use_container_width=True,
                        key=f"btn_{page.lower().replace(' ', '_')}"
                    ):
                        st.session_state["selected_page"] = page
                        st.session_state["navigated_from_card"] = True
                        st.rerun()

    # Add some spacing at the bottom
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
