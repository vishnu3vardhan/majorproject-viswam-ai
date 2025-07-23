# pages/record_keeping.py
import streamlit as st
from db import add_record, get_records

def show():
    st.header("📒 Farm Record Keeping")

    record_type = st.selectbox("📂 Record Type", ["Dairy", "Poultry", "Crop"])
    detail = st.text_input("📝 Record Details")

    if st.button("💾 Save Record"):
        add_record(record_type, detail, "2025-07-17")  # You can replace with current date
        st.success("✅ Record saved successfully!")

    if st.checkbox("📜 Show All Records"):
        records = get_records()
        st.table(records)
