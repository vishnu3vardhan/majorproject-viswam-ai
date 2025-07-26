import streamlit as st
import json
from components.translator import translate_text

def show(dest_lang='en'):
    st.title(translate_text("🌦️ Weather-Based Crop Planning (Offline Mode)", dest_lang))

    # City input
    city = st.text_input(
        translate_text("🏙️ Enter your district (e.g., Hyderabad, Warangal, Nizamabad)", dest_lang)
    ).strip().lower()

    if not city:
        st.info(translate_text("ℹ️ Please enter a district name to proceed.", dest_lang))
        return

    # Load mock weather data
    try:
        with open("mock_weather.json") as f:
            all_data = json.load(f)
    except FileNotFoundError:
        st.error(translate_text("❌ mock_weather.json file not found.", dest_lang))
        return

    if city not in all_data:
        st.warning(translate_text("⚠️ No data available for", dest_lang) + f" '{city.title()}'. " +
                   translate_text("Try: Hyderabad, Warangal, Nizamabad, etc.", dest_lang))
        return

    forecast = all_data[city]['list'][:5]

    st.subheader(translate_text("📊 Recent Weather in", dest_lang) + f" {city.title()}")
    for block in forecast:
        temp = block['main']['temp']
        humidity = block['main']['humidity']
        weather = block['weather'][0]['description']
        st.write(f"🌡️ {translate_text('Temp', dest_lang)}: {temp}°C, "
                 f"💧 {translate_text('Humidity', dest_lang)}: {humidity}%, "
                 f"🌤️ {translate_text('Condition', dest_lang)}: {translate_text(weather, dest_lang)}")

    avg_temp = sum([block['main']['temp'] for block in forecast]) / len(forecast)

    st.subheader(translate_text("🌿 Crop Suggestions Based on Temperature", dest_lang))
    if avg_temp > 30:
        st.success(translate_text("Recommended Crops:", dest_lang) + " **Millets, Sorghum, Groundnut, Cotton**")
    elif 20 <= avg_temp <= 30:
        st.success(translate_text("Recommended Crops:", dest_lang) + " **Rice, Soybean, Sugarcane, Tomato**")
    else:
        st.success(translate_text("Recommended Crops:", dest_lang) + " **Wheat, Barley, Mustard, Peas**")
