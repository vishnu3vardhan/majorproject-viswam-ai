import streamlit as st
from db import add_record, get_records
from components.translator import translate_text

def show(dest_lang='en'):
    st.header(translate_text("📒 Farm Record Keeping", dest_lang))

    record_type = st.selectbox(
        translate_text("📂 Record Type", dest_lang),
        [translate_text("Dairy", dest_lang), translate_text("Poultry", dest_lang), translate_text("Crop", dest_lang)]
    )

    detail = st.text_input(translate_text("📝 Record Details", dest_lang))

    if st.button(translate_text("💾 Save Record", dest_lang)):
        add_record(record_type, detail, "2025-07-17")  # Replace with dynamic date if needed
        st.success(translate_text("✅ Record saved successfully!", dest_lang))

    if st.checkbox(translate_text("📜 Show All Records", dest_lang)):
        records = get_records()
        st.table(records)
