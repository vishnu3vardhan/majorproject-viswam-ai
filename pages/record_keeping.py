# pages/record_keeping.py
import streamlit as st
from db import add_record, get_records, insert_image, list_all_images, get_image_by_id
import datetime
import os

def show():
    st.header("📒 Farm Record Keeping")

    # Section 1 — General Text-Based Record
    st.subheader("📝 General Record")
    record_type = st.selectbox("📂 Record Type", ["Dairy", "Poultry", "Crop"])
    detail = st.text_input("📝 Record Details")

    if st.button("💾 Save Record"):
        today = datetime.date.today().isoformat()
        add_record(record_type, detail, today)
        st.success("✅ Record saved successfully!")

    if st.checkbox("📜 Show All Records"):
        records = get_records()
        st.table(records)

    # Section 2 — Disease Image Upload
    st.subheader("🦠 Upload Crop/Cattle Disease Image")

    image_name = st.text_input("🔤 Image Name")
    category = st.selectbox("📁 Category", ["crop", "cattle"])
    description = st.text_area("🖋️ Description of Disease")
    image_file = st.file_uploader("📤 Upload Disease Image", type=["jpg", "jpeg", "png"])

    if st.button("🧬 Save Disease Image"):
        if image_file and image_name and category:
            # Save temp image
            temp_path = "temp_image.jpg"
            with open(temp_path, "wb") as f:
                f.write(image_file.read())
            insert_image(image_name, category, description, temp_path)
            os.remove(temp_path)  # Clean up after storing
            st.success("✅ Disease image saved!")
        else:
            st.warning("⚠️ Please fill all fields and upload an image.")

    # Section 3 — Show All Images with Previews
    if st.checkbox("🖼️ Show Stored Disease Images"):
        images = list_all_images()
        if images:
            for img in images:
                img_id, name, cat, desc = img
                st.markdown(f"**🆔 ID:** {img_id} | **📛 Name:** {name} | **📂 Category:** {cat}")
                st.markdown(f"**📝 Description:** {desc}")
                
                # Get image blob
                data = get_image_by_id(img_id)
                if data:
                    _, _, _, image_blob = data
                    st.image(image_blob, caption=name, use_column_width=True)
                st.markdown("---")
        else:
            st.info("No disease images stored yet.")



#  pages/record_keeping.py
# import streamlit as st
# from db import add_record, get_records

# def show():
#     st.header("📒 Farm Record Keeping")

#     record_type = st.selectbox("📂 Record Type", ["Dairy", "Poultry", "Crop"])
#     detail = st.text_input("📝 Record Details")

#     if st.button("💾 Save Record"):
#         add_record(record_type, detail, "2025-07-17")  # You can replace with current date
#         st.success("✅ Record saved successfully!")

#     if st.checkbox("📜 Show All Records"):
#         records = get_records()
#         st.table(records)
