import streamlit as st
from pages import home, record_keeping, disease_detection

st.set_page_config(page_title="FarminAI Assistant", page_icon="assets/logo.png", layout="wide")

st.sidebar.image("assests/logo.png", width=120)
st.sidebar.title("🚜 FarminAI Navigation")

# Navigation
page = st.sidebar.radio("Go to", ("Home", "Disease Detection", "Farm Record Keeping"))

if page == "Home":
    home.show()

elif page == "Disease Detection":
    st.sidebar.subheader("Detection Type")
    detection_type = st.sidebar.radio("Select Type", ("Poultry", "Cow", "Crop"))

    if detection_type == "Poultry":
        disease_detection.poultry_disease_detection()
    elif detection_type == "Cow":
        disease_detection.cow_disease_detection()
    elif detection_type == "Crop":
        disease_detection.crop_disease_detection()

elif page == "Farm Record Keeping":
    record_keeping.show()
