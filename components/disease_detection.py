import streamlit as st
from detection import predict_disease
from components.translator import translate_text
from components.feedback_button import feedback_button  # Import the feedback component

def show(dest_lang='en'):
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except:
            return text

    # Add the feedback button at the top
    feedback_button("disease_detection")
    
    st.markdown(
        f"""
        <div style='text-align: center; padding-bottom: 10px;'>
            <h2 style='color:#6A1B9A;'>{t("🧫 Disease Detection System")}</h2>
            <p style='color: gray;'>{t("Upload an image of a crop, cow, or poultry to detect possible diseases.")}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Detection Type
    detection_type = st.selectbox(
        t("🧬 Select Detection Type"),
        [
            t("Crop"),
            t("Cow"),
            t("Poultry")
        ]
    )

    uploaded_file = st.file_uploader(
        t("📷 Upload an image"),
        type=["jpg", "jpeg", "png"]
    )

    # Preview uploaded image
    if uploaded_file:
        st.markdown("<p style='text-align: center; color: gray;'>"
                    f"{t('Preview of the uploaded image')}"
                    "</p>", unsafe_allow_html=True)
        st.image(uploaded_file, width=600)

    st.markdown("<br>", unsafe_allow_html=True)

    # Prediction trigger
    if uploaded_file and st.button(t("🔍 Predict Disease"), use_container_width=True):
        type_map = {
            t("Crop"): "crop",
            t("Cow"): "cow",
            t("Poultry"): "poultry"
        }
        model_type = type_map.get(detection_type, "crop")

        with st.spinner(t("Analyzing image...")):
            result = predict_disease(uploaded_file, model_type=model_type)

        st.success(f"🧪 {t('Prediction for')} {detection_type}: **{t(result)}**")

    # Footer spacing
    st.markdown("<br><br>", unsafe_allow_html=True)