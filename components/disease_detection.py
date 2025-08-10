import streamlit as st
from detection import predict_disease
from components.translator import translate_text

def show(dest_lang='en'):
    st.markdown(
        f"""
        <div style='text-align: center; padding-bottom: 10px;'>
            <h2 style='color:#6A1B9A;'>{translate_text("🧫 Disease Detection System", dest_lang)}</h2>
            <p style='color: gray;'>{translate_text("Upload an image of a crop, cow, or poultry to detect possible diseases.", dest_lang)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Detection Type
    detection_type = st.selectbox(
        translate_text("🧬 Select Detection Type", dest_lang),
        [
            translate_text("Crop", dest_lang),
            translate_text("Cow", dest_lang),
            translate_text("Poultry", dest_lang)
        ]
    )

    uploaded_file = st.file_uploader(
        translate_text("📷 Upload an image", dest_lang),
        type=["jpg", "jpeg", "png"]
    )

    # Preview uploaded image
    if uploaded_file:
        st.markdown("<p style='text-align: center; color: gray;'>"
                    f"{translate_text('Preview of the uploaded image', dest_lang)}"
                    "</p>", unsafe_allow_html=True)
        st.image(uploaded_file, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Prediction trigger
    if uploaded_file and st.button(translate_text("🔍 Predict Disease", dest_lang), use_container_width=True):
        type_map = {
            translate_text("Crop", dest_lang): "crop",
            translate_text("Cow", dest_lang): "cow",
            translate_text("Poultry", dest_lang): "poultry"
        }
        model_type = type_map.get(detection_type, "crop")

        with st.spinner(translate_text("Analyzing image...", dest_lang)):
            result = predict_disease(uploaded_file, model_type=model_type)

        st.success(f"🧪 {translate_text('Prediction for', dest_lang)} {detection_type}: **{translate_text(result, dest_lang)}**")

    # Footer spacing
    st.markdown("<br><br>", unsafe_allow_html=True)
