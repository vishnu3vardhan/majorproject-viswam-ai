import streamlit as st
import json

def show():
    st.title("🌦️ Weather-Based Crop Planning (Offline Mode)")

    # City selection input
    city = st.text_input("🏙️ Enter your district (e.g., Hyderabad, Warangal, Nizamabad)").strip().lower()

    if not city:
        st.info("ℹ️ Please enter a district name to proceed.")
        return

    # Load mock weather data
    try:
        with open("mock_weather.json") as f:
            all_data = json.load(f)
    except FileNotFoundError:
        st.error("❌ mock_weather.json file not found.")
        return

    # Check if city is in predefined mock data
    if city not in all_data:
        st.warning(f"⚠️ No data available for '{city.title()}'. Try: Hyderabad, Warangal, Nizamabad, etc.")
        return

    forecast = all_data[city]['list'][:5]  # Simulated 5 recent intervals

    st.subheader(f"📊 Recent Weather in {city.title()}")
    for i, block in enumerate(forecast, 1):
        temp = block['main']['temp']
        humidity = block['main']['humidity']
        weather = block['weather'][0]['description']
        st.write(f" 🌡️ Temp: {temp}°C, 💧 Humidity: {humidity}%, 🌤️ Condition: {weather}")

    # Calculate average temperature
    avg_temp = sum([block['main']['temp'] for block in forecast]) / len(forecast)

    st.subheader("🌿 Crop Suggestions Based on Temperature")
    if avg_temp > 30:
        st.success("Recommended Crops: **Millets, Sorghum, Groundnut, Cotton**")
    elif 20 <= avg_temp <= 30:
        st.success("Recommended Crops: **Rice, Soybean, Sugarcane, Tomato**")
    else:
        st.success("Recommended Crops: **Wheat, Barley, Mustard, Peas**")
