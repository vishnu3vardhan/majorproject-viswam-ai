# pages/record_keeping.py
import streamlit as st
from db import add_record, get_records, insert_image, list_all_images, get_image_by_id
from components.translator import translate_text
from components.feedback_button import feedback_button  # Import the feedback component
import datetime
import os

def show(dest_lang='en'):
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except:
            return text

    # Add the feedback button at the top
    feedback_button("record_keeping")
    
    st.header(f"📒 {t('Farm Record Keeping')}")

    # Section 1 — General Text-Based Record
    st.subheader(f"📝 {t('General Record')}")
    record_type = st.selectbox(f"📂 {t('Record Type')}", [t("Dairy"), t("Poultry"), t("Crop")])
    detail = st.text_input(f"📝 {t('Record Details')}")

    if st.button(f"💾 {t('Save Record')}"):
        today = datetime.date.today().isoformat()
        add_record(record_type, detail, today)
        st.success(f"✅ {t('Record saved successfully!')}")

    if st.checkbox(f"📜 {t('Show All Records')}"):
        records = get_records()
        st.table(records)

    # Section 2 — Disease Image Upload
    st.subheader(f"🦠 {t('Upload Crop/Cattle Disease Image')}")

    image_name = st.text_input(f"🔤 {t('Image Name')}")
    category = st.selectbox(f"📁 {t('Category')}", [t("crop"), t("cattle")])
    description = st.text_area(f"🖋️ {t('Description of Disease')}")
    image_file = st.file_uploader(f"📤 {t('Upload Disease Image')}", type=["jpg", "jpeg", "png"])

    if st.button(f"🧬 {t('Save Disease Image')}"):
        if image_file and image_name and category:
            # Save temp image
            temp_path = "temp_image.jpg"
            with open(temp_path, "wb") as f:
                f.write(image_file.read())
            insert_image(image_name, category, description, temp_path)
            os.remove(temp_path)  # Clean up after storing
            st.success(f"✅ {t('Disease image saved!')}")
        else:
            st.warning(f"⚠️ {t('Please fill all fields and upload an image.')}")

    # Section 3 — Show All Images with Previews
    if st.checkbox(f"🖼️ {t('Show Stored Disease Images')}"):
        images = list_all_images()
        if images:
            for img in images:
                img_id, name, cat, desc = img
                st.markdown(f"**🆔 ID:** {img_id} | **📛 {t('Name')}:** {name} | **📂 {t('Category')}:** {cat}")
                st.markdown(f"**📝 {t('Description')}:** {desc}")
                
                # Get image blob
                data = get_image_by_id(img_id)
                if data:
                    _, _, _, image_blob = data
                    st.image(image_blob, caption=name, use_column_width=True)
                st.markdown("---")
        else:
            st.info(f"{t('No disease images stored yet.')}")