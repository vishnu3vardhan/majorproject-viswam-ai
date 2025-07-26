import streamlit as st
from detection import predict_disease
from components.translator import translate_text

def show(dest_lang='en'):
    st.title(translate_text("🧫 Disease Detection System", dest_lang))
    st.write(translate_text("Upload an image to detect possible diseases in crops or livestock.", dest_lang))

    # Detection Type Selection
    detection_type = st.selectbox(
        translate_text("Select Detection Type", dest_lang),
        [
            translate_text("Crop", dest_lang),
            translate_text("Cow", dest_lang),
            translate_text("Poultry", dest_lang)
        ]
    )

    uploaded_file = st.file_uploader(translate_text("📷 Upload an image", dest_lang), type=["jpg", "jpeg", "png"])

    if uploaded_file and st.button(translate_text("🔍 Predict Disease", dest_lang)):
        # Map translated detection_type back to model keyword
        type_map = {
            translate_text("Crop", dest_lang): "crop",
            translate_text("Cow", dest_lang): "cow",
            translate_text("Poultry", dest_lang): "poultry"
        }
        model_type = type_map.get(detection_type, "crop")

        result = predict_disease(uploaded_file, model_type=model_type)
        st.success(f"{translate_text('🧪 Prediction for', dest_lang)} {detection_type}: **{translate_text(result, dest_lang)}**")
