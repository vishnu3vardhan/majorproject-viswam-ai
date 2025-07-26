import streamlit as st
from db import add_record, get_records
from components.translator import translate_text
from datetime import datetime

def show(dest_lang='en'):
    # Header Section
    st.markdown(
        f"""
        <div style='text-align: center; padding: 10px 0;'>
            <h2 style='color:#2E7D32;'>{translate_text("📒 Farm Record Keeping", dest_lang)}</h2>
            <p style='color: gray;'>{translate_text("Keep track of your dairy, poultry, or crop activities easily.", dest_lang)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Form Section
    with st.container():
        col1, col2 = st.columns([2, 5])

        with col1:
            record_type = st.selectbox(
                translate_text("📂 Record Type", dest_lang),
                [translate_text("Dairy", dest_lang), translate_text("Poultry", dest_lang), translate_text("Crop", dest_lang)]
            )

        with col2:
            detail = st.text_input(
                translate_text("📝 Record Details", dest_lang),
                placeholder=translate_text("e.g., Bought 10 hens / Applied fertilizer", dest_lang)
            )

    # Save Button
    save_clicked = st.button(translate_text("💾 Save Record", dest_lang), use_container_width=True)

    if save_clicked:
        current_date = datetime.now().strftime("%Y-%m-%d")
        add_record(record_type, detail, current_date)
        st.success(translate_text("✅ Record saved successfully!", dest_lang))

    st.markdown("---")

    # Display Records
    if st.checkbox(translate_text("📜 Show All Records", dest_lang)):
        records = get_records()
        if records and len(records) > 0:
            st.markdown(
                f"<h4 style='color:#2E7D32;'>{translate_text('📋 All Saved Records', dest_lang)}</h4>",
                unsafe_allow_html=True
            )
            st.table(records)
        else:
            st.info(translate_text("No records found.", dest_lang))

    # Footer spacing
    st.markdown("<br><br>", unsafe_allow_html=True)
