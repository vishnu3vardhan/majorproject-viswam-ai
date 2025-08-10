import streamlit as st
import json
from components.translator import translate_text

def show(dest_lang='en'):
    st.markdown(
        f"""
        <div style='text-align: center; padding-bottom: 10px;'>
            <h2 style='color:#2E7D32;'>{translate_text("🌿 Crop Suggestion Based on Season", dest_lang)}</h2>
            <p style='color: gray;'>{translate_text("Enter the season to get crop suggestions that match weather, soil, and duration.", dest_lang)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

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
            st.success(
                f"✅ {translate_text('Found', dest_lang)} {len(matching_crops)} {translate_text('crop(s) for the season', dest_lang)}: {season_input.title()}"
            )
            st.markdown("")

            # Display matching crops
            for crop in matching_crops:
                st.markdown(
                    f"""
                    <div style="border: 1px solid #444; padding: 15px; border-radius: 10px; background-color: #1e1e1e; color: #f0f0f0; margin-bottom: 20px;">
                        <h4 style="color: #81c784;">🌾 {translate_text(crop['crop'], dest_lang)}</h4>
                        <ul style="padding-left: 20px; line-height: 1.6;">
                            <li><strong>{translate_text("Season", dest_lang)}:</strong> {translate_text(crop['season'], dest_lang)}</li>
                            <li><strong>{translate_text("Weather Condition", dest_lang)}:</strong> {translate_text(crop['weather'], dest_lang)}</li>
                            <li><strong>{translate_text("Soil Type", dest_lang)}:</strong> {translate_text(crop['soil'], dest_lang)}</li>
                            <li><strong>{translate_text("Duration", dest_lang)}:</strong> {translate_text(crop['duration'], dest_lang)}</li>
                            <li><strong>{translate_text("Investment", dest_lang)}:</strong> {translate_text(crop['investment'], dest_lang)}</li>
                            <li><strong>{translate_text("Expected Profit", dest_lang)}:</strong> {translate_text(crop['profit'], dest_lang)}</li>
                            <li><strong>{translate_text("How to Start", dest_lang)}:</strong> {translate_text(crop['how_to_start'], dest_lang)}</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # BEST CROP LOGIC BASED ON PROFIT (Assuming profit is in numbers)
            def extract_profit(value):
                try:
                    return float(''.join(filter(str.isdigit, value)))
                except:
                    return 0

            best_crop = max(matching_crops, key=lambda crop: extract_profit(crop['profit']))

            st.markdown("### 🥇 " + translate_text("Best Crop to Cultivate Among These", dest_lang))
            st.success(
                f"🌱 **{translate_text(best_crop['crop'], dest_lang)}** - {translate_text('has the highest expected profit among the suggested crops.', dest_lang)}"
            )

        else:
            st.warning(
                f"⚠ {translate_text('No crop suggestions found for season', dest_lang)}: {season_input.title()}"
            )
    else:
        st.info(translate_text("Please enter a season to get crop suggestions.", dest_lang))

    st.markdown("<br>", unsafe_allow_html=True)
