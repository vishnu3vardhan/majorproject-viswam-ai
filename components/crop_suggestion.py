import streamlit as st
import json
from components.translator import translate_text

def show(dest_lang='en'):
    st.title(translate_text("🌿 Crop Suggestion Based on Season", dest_lang))

    try:
        with open("data/crop_data.json", "r", encoding="utf-8") as f:
            crop_data = json.load(f)
    except FileNotFoundError:
        st.error(translate_text("❌ 'crop_data.json' not found in 'data/' folder.", dest_lang))
        return

    season_input = st.text_input(
        translate_text("Enter Season (e.g. Summer, Winter, Monsoon)", dest_lang),
        placeholder=translate_text("Type a season...", dest_lang)
    )

    if season_input:
        matching_crops = [
            crop for crop in crop_data
            if crop["season"].strip().lower() == season_input.strip().lower()
        ]

        if matching_crops:
            for crop in matching_crops:
                st.subheader(translate_text("🌾 Suggested Crop:", dest_lang) + f" {translate_text(crop['crop'], dest_lang)}")
                st.markdown(f"""
                - **{translate_text('Season', dest_lang)}:** {translate_text(crop['season'], dest_lang)}
                - **{translate_text('Weather Condition', dest_lang)}:** {translate_text(crop['weather'], dest_lang)}
                - **{translate_text('Soil Type', dest_lang)}:** {translate_text(crop['soil'], dest_lang)}
                - **{translate_text('Duration', dest_lang)}:** {translate_text(crop['duration'], dest_lang)}
                - **{translate_text('Investment', dest_lang)}:** {translate_text(crop['investment'], dest_lang)}
                - **{translate_text('Expected Profit', dest_lang)}:** {translate_text(crop['profit'], dest_lang)}
                - **{translate_text('How to Start', dest_lang)}:** {translate_text(crop['how_to_start'], dest_lang)}
                """)
        else:
            st.warning(translate_text("⚠ No crop suggestions found for season:", dest_lang) + f" {season_input}")
    else:
        st.info(translate_text("Please enter a season to get crop suggestions.", dest_lang))
