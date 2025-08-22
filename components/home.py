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

    # Initialize session state for navigation control
    if "home_initialized" not in st.session_state:
        st.session_state.home_initialized = True
        st.session_state.navigated_from_card = False

    # Header
    st.markdown(
        f"""
        <div style='text-align: center; margin-bottom: 40px;'>
            <h1 style='display: inline-flex; align-items: center; gap: 10px; color: #2e8b57;'>
                🌾 {t("Welcome to Farmin-A.I Assistant")}
            </h1>
            <p style='color: #666; font-size: 18px; margin-top: 10px;'>
                {t("Your Intelligent Farming Companion")}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Create columns to position the feedback button at the top-right
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col3:
     if st.button("💬 Feedback", key="feedback_btn_home", 
                help="Provide feedback about the application"):
        st.session_state.selected_page = "Feedback"
        st.session_state.navigated_from_card = True
        st.rerun()

    # Clean card styling without white boxes
    st.markdown("""
        <style>
        .feature-card {
            padding: 0;
            border-radius: 15px;
            background: transparent;
            text-align: center;
            margin-bottom: 30px;
            transition: transform 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
        .card-image {
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .card-title {
            font-weight: 600;
            font-size: 20px;
            color: #2e8b57;
            margin-bottom: 15px;
        }
        .card-button {
            background: #0084ff !important; /* Messenger Blue */
            color: white !important;
            border: none !important;
            padding: 12px 25px !important;
            font-weight: 500 !important;
            font-size: 14px !important;
            transition: all 0.3s ease !important;
            width: auto !important;
            margin: 0 auto !important;
            display: block !important;
            border-radius: 20px 20px 20px 5px !important; /* Messenger bubble shape */
            box-shadow: 0 4px 12px rgba(0, 132, 255, 0.3) !important;
        }
        .card-button:hover {
            background: #0066cc !important; /* Darker blue on hover */
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 132, 255, 0.4) !important;
        }
        .card-content {
            padding: 0;
            background: transparent;
        }
        </style>
    """, unsafe_allow_html=True)

    CARD_WIDTH = 280
    CARD_HEIGHT = 180

    PLACEHOLDER_IMAGES = {
        "crop": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=300&h=200&fit=crop",
        "weather": "https://images.unsplash.com/photo-1561484930-974554019ade?w=300&h=200&fit=crop",
        "disease": "https://images.unsplash.com/photo-1604977046806-87b1b5b533?w=300&h=200&fit=crop",
        "profit": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=300&h=200&fit=crop",
        "record": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=300&h=200&fit=crop",
        "assistant": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=300&h=200&fit=crop",
    }

    def load_image(card_key, path):
        try:
            if os.path.exists(path):
                img = Image.open(path)
                img = img.resize((CARD_WIDTH, CARD_HEIGHT))
                return img
            return PLACEHOLDER_IMAGES[card_key.lower().replace(" ", "_").split(".")[0]]
        except Exception as e:
            return PLACEHOLDER_IMAGES.get("crop", "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=300&h=200&fit=crop")

    cards = [
        ("Crop Suggestion", "assets/crop.jpg", "Crop Suggestion", "🌱"),
        ("Weather Crop Planner", "assets/weather.jpg", "Weather-Based Crop Planning", "🌤️"),
        ("Disease Detection", "assets/disease.jpg", "Disease Detection", "🔍"),
        ("Profit Calculator", "assets/profit.jpg", "Profit Calculator", "💰"),
        ("Record Keeping", "assets/record.jpg", "Farm Record Keeping", "📒"),
        ("Voice & Text Assistant", "assets/assistant.jpg", "Voice & Text Assistant", "🎙️"),
    ]

    # Track if any button was clicked in this run
    button_clicked = False
    clicked_page = None

    # Render 3 cards per row
    for i in range(0, len(cards), 3):
        cols = st.columns(3)
        for col, (title, img_path, page, icon) in zip(cols, cards[i:i+3]):
            with col:
                # Card container
                st.markdown(f"""
                    <div class='feature-card'>
                        <div class='card-image'>
                """, unsafe_allow_html=True)
                
                # Image
                img = load_image(title, img_path)
                if isinstance(img, Image.Image):
                    st.image(img, width=CARD_WIDTH)
                elif isinstance(img, str):
                    st.image(img, width=CARD_WIDTH)
                else:
                    st.markdown(
                        f"<div style='width:{CARD_WIDTH}px; height:{CARD_HEIGHT}px; "
                        f"display:flex; align-items:center; justify-content:center; background:linear-gradient(135deg, #f0f8ff, #e0f7fa); "
                        f"border-radius: 15px;'>"
                        f"<h1 style='font-size: 48px;'>{icon}</h1></div>",
                        unsafe_allow_html=True
                    )
                
                # Title and button
                st.markdown(f"""
                    </div>
                    <div class='card-content'>
                        <div class='card-title'>{icon} {t(title)}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Button with unique key
                if st.button(t(f"Open {title}"), key=f"home_btn_{page.lower().replace(' ', '_')}"):
                    button_clicked = True
                    clicked_page = page

    # Handle navigation after all buttons are rendered
    if button_clicked and clicked_page:
        st.session_state.selected_page = clicked_page
        st.session_state.navigated_from_card = True
        st.rerun()