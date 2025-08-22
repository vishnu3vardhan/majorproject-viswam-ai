import streamlit as st

def feedback_button(page_name=""):
    """
    Reusable feedback button component for all pages
    """
    # Create columns to position the feedback button at the top-right
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col3:
        # Use a proper Streamlit button for feedback with a unique key
        if st.button("💬 Feedback", key=f"feedback_btn_{page_name}", 
                    help="Provide feedback about the application"):
            st.session_state.selected_page = "Feedback"
            st.session_state.navigated_from_card = True
            st.rerun()
    
    # Add the CSS styling for the feedback button
    st.markdown("""
        <style>
        /* Style for the feedback button */
        div.stButton > button:first-child {
            background: linear-gradient(45deg, #2e8b57, #3cb371) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 14px 28px !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
            width: 100%;
        }
        div.stButton > button:hover {
            background: linear-gradient(45deg, #267349, #2e8b57) !important;
            box-shadow: 0 6px 22px rgba(0,0,0,0.3) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    