import streamlit as st
from components.translator import translate_text

def feedback_page(dest_lang='en'):
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except:
            return text
    
    st.title(t("Feedback Form"))
    st.markdown(f"<p>{t('We value your feedback! Please share your experience with us.')}</p>", unsafe_allow_html=True)
    
    with st.form("feedback_form"):
        # Name field
        name = st.text_input(t("Your Name"))
        
        # Email field
        email = st.text_input(t("Email Address"))
        
        # Rating
        rating = st.slider(t("Overall Rating"), 1, 5, 3)
        
        # Feedback category
        category = st.selectbox(
            t("Feedback Category"),
            [t("General Feedback"), t("Bug Report"), t("Feature Request"), t("Usability Issue")]
        )
        
        # Feedback message
        message = st.text_area(t("Your Feedback"), height=150)
        
        # Attachment
        attachment = st.file_uploader(t("Attach screenshot (if applicable)"), type=['png', 'jpg', 'jpeg'])
        
        # Submit button
        submitted = st.form_submit_button(t("Submit Feedback"))
        
        if submitted:
            if message.strip():
                # Here you would typically save the feedback to a database or send via email
                st.success(t("Thank you for your feedback! We appreciate you taking the time to help us improve."))
                
                # Option to return to home
                if st.button(t("Return to Home")):
                    st.session_state.selected_page = "Home"
                    st.rerun()
            else:
                st.error(t("Please provide your feedback in the message field."))