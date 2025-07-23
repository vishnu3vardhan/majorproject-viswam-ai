# pages/disease_detection.py
import streamlit as st
from detection import predict_disease

def poultry_disease_detection():
    st.header("🐔 Poultry Disease Detection")
    st.write("Upload an image to detect possible disease in livestock or crops.")

    uploaded_file = st.file_uploader("📷 Choose an image", type=["jpg", "png"])
    if uploaded_file and st.button("🔍 Predict Disease"):
        result = predict_disease(uploaded_file, model_type="poultry")
        st.info(f"Prediction: **{result}**")

def cow_disease_detection():
    st.header("🐄 Cow Disease Detection")
    st.write("Upload an image to detect possible disease in livestock or crops.")

    uploaded_file = st.file_uploader("📷 Choose an image", type=["jpg", "png"])
    if uploaded_file and st.button("🔍 Predict Disease"):
        result = predict_disease(uploaded_file, model_type="cow")
        st.info(f"Prediction: **{result}**")

def crop_disease_detection():
    st.header("🌾 Crop Disease Detection")
    st.write("Upload an image to detect possible disease in livestock or crops.")

    uploaded_file = st.file_uploader("📷 Choose an image", type=["jpg", "png"])
    if uploaded_file and st.button("🔍 Predict Disease"):
        result = predict_disease(uploaded_file, model_type="crop")
        st.info(f"Prediction: **{result}**")
    
    
    
     
