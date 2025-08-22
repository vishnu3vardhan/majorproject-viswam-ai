import streamlit as st
import json
from components.translator import translate_text
from components.feedback_button import feedback_button  # Import the feedback component

def show(dest_lang='en'):
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except:
            return text

    # Add the feedback button at the top
    feedback_button("crop_suggestion")
    
    st.markdown(
        f"""
        <div style='text-align: center; padding-bottom: 10px;'>
            <h2 style='color:#2E7D32;'>{t("🌿 Crop Suggestion Based on Season")}</h2>
            <p style='color: gray;'>{t("Enter the season to get crop suggestions that match weather, soil, and duration.")}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    try:
        with open("data/crop_data.json", "r", encoding="utf-8") as f:
            crop_data = json.load(f)
    except FileNotFoundError:
        st.error(t("❌ 'crop_data.json' not found in 'data/' folder."))
        return

    season_input = st.text_input(
        t("Enter Season (e.g. Summer, Winter, Monsoon)"),
        placeholder=t("Type a season...")
    )

    if season_input:
        matching_crops = [
            crop for crop in crop_data
            if crop["season"].strip().lower() == season_input.strip().lower()
        ]

        if matching_crops:
            st.success(
                f"✅ {t('Found')} {len(matching_crops)} {t('crop(s) for the season')}: {season_input.title()}"
            )
            st.markdown("")

            # Display matching crops
            for crop in matching_crops:
                st.markdown(
                    f"""
                    <div style="border: 1px solid #444; padding: 15px; border-radius: 10px; background-color: #1e1e1e; color: #f0f0f0; margin-bottom: 20px;">
                        <h4 style="color: #81c784;">🌾 {t(crop['crop'])}</h4>
                        <ul style="padding-left: 20px; line-height: 1.6;">
                            <li><strong>{t("Season")}:</strong> {t(crop['season'])}</li>
                            <li><strong>{t("Weather Condition")}:</strong> {t(crop['weather'])}</li>
                            <li><strong>{t("Soil Type")}:</strong> {t(crop['soil'])}</li>
                            <li><strong>{t("Duration")}:</strong> {t(crop['duration'])}</li>
                            <li><strong>{t("Investment")}:</strong> {t(crop['investment'])}</li>
                            <li><strong>{t("Expected Profit")}:</strong> {t(crop['profit'])}</li>
                            <li><strong>{t("How to Start")}:</strong> {t(crop['how_to_start'])}</li>
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

            st.markdown("### 🥇 " + t("Best Crop to Cultivate Among These"))
            st.success(
                f"🌱 **{t(best_crop['crop'])}** - {t('has the highest expected profit among the suggested crops.')}"
            )

        else:
            st.warning(
                f"⚠ {t('No crop suggestions found for season')}: {season_input.title()}"
            )
    else:
        st.info(t("Please enter a season to get crop suggestions."))

    st.markdown("<br>", unsafe_allow_html=True)