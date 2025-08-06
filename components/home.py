import streamlit as st
from PIL import Image
from components.translator import translate_text  # 👈 translation helper

def show(dest_lang='en'):
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except:
            return text

    st.markdown(
        f"""
        <h1 style='text-align: center;'>
            <img src='https://img.icons8.com/emoji/48/seedling.png' width='35'/>
            {t("Welcome to")} <strong>Farmin-A.I Assistant</strong>
        </h1>
        """,
        unsafe_allow_html=True
    )

    card_width = 300
    card_height = 200

    def load_image(path):
        try:
            image = Image.open(path).resize((card_width, card_height))
            return image
        except Exception as e:
            st.error(f"Error loading {path}: {e}")
            return None

    # First row of cards
    cols = st.columns(3)

    with cols[0]:
        img = load_image("assests/crop.jpg")
        if img: st.image(img, use_container_width=True)
        st.markdown(f"### 🌱 {t('Crop Suggestion')}", unsafe_allow_html=True)
        if st.button(t("Open Crop Suggestion")):
            st.session_state["selected_page"] = "Crop Suggestion"
            st.session_state["navigated_from_card"] = True
            st.rerun()

    with cols[1]:
        img = load_image("assests/weather.jpg")
        if img: st.image(img, use_container_width=True)
        st.markdown(f"### 🌤️ {t('Weather Crop Planner')}", unsafe_allow_html=True)
        if st.button(t("Open Weather Planner")):
            st.session_state["selected_page"] = "Weather-Based Crop Planning"
            st.session_state["navigated_from_card"] = True
            st.rerun()

    with cols[2]:
        img = load_image("assests/disease.jpg")
        if img: st.image(img, use_container_width=True)
        st.markdown(f"### 🥬 {t('Disease Detection')}", unsafe_allow_html=True)
        if st.button(t("Open Disease Detection")):
            st.session_state["selected_page"] = "Disease Detection"
            st.session_state["navigated_from_card"] = True
            st.rerun()

    # Second row of cards
    cols2 = st.columns(3)

    with cols2[0]:
        img = load_image("assests/profit.jpg")
        if img: st.image(img, use_container_width=True)
        st.markdown(f"### 💰 {t('Profit Calculator')}", unsafe_allow_html=True)
        if st.button(t("Open Profit Calculator")):
            st.session_state["selected_page"] = "Profit Calculator"
            st.session_state["navigated_from_card"] = True
            st.rerun()

    with cols2[1]:
        img = load_image("assests/record.jpg")
        if img: st.image(img, use_container_width=True)
        st.markdown(f"### 📒 {t('Record Keeping')}", unsafe_allow_html=True)
        if st.button(t("Open Record Keeping")):
            st.session_state["selected_page"] = "Farm Record Keeping"
            st.session_state["navigated_from_card"] = True
            st.rerun()

    with cols2[2]:
        img = load_image("assests/assistant.jpg")
        if img: st.image(img, use_container_width=True)
        st.markdown(f"### 🎙️ {t('Voice & Text Assistant')}", unsafe_allow_html=True)
        if st.button(t("Open Assistant")):
            st.session_state["selected_page"] = "Voice & Text Assistant"
            st.session_state["navigated_from_card"] = True
            st.rerun()
