import streamlit as st
import json
from components.translator import translate_text
from components.feedback_button import feedback_button  # Add this import


def show(dest_lang='en'):
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except:
            return text

    # Add the feedback button at the top
    feedback_button("Weather-Based Crop Planning")
   
    # Stylized title
    st.markdown(
        f"""
        <div style='text-align: center; padding-bottom: 10px;'>
            <h2 style='color:#00796B;'>{translate_text("🌦️ Weather-Based Crop Planning", dest_lang)}</h2>
            <p style='color: gray;'>{translate_text("Plan your crops smartly with recent weather trends.", dest_lang)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # District input
    city = st.text_input(
        translate_text("🏙️ Enter your district (e.g., Hyderabad, Warangal, Nizamabad)", dest_lang),
        placeholder=translate_text("Type a district name...", dest_lang)
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
        st.warning(
            f"⚠️ {translate_text('No data available for', dest_lang)} '{city.title()}'.<br>"
            f"{translate_text('Try: Hyderabad, Warangal, Nizamabad, etc.', dest_lang)}",
            unsafe_allow_html=True
        )
        return

    forecast = all_data[city]['list'][:5]

    st.markdown("### 🌤️ " + translate_text("Recent Weather Overview", dest_lang) + f" - {city.title()}")
    with st.container():
        for block in forecast:
            temp = block['main']['temp']
            humidity = block['main']['humidity']
            weather = block['weather'][0]['description']
            st.markdown(
                f"""
                <div style='background-color: #1e1e1e; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>
                    🌡️ <b>{translate_text('Temperature', dest_lang)}:</b> {temp}°C &nbsp;&nbsp;
                    💧 <b>{translate_text('Humidity', dest_lang)}:</b> {humidity}% &nbsp;&nbsp;
                    🌤️ <b>{translate_text('Condition', dest_lang)}:</b> {translate_text(weather, dest_lang)}
                </div>
                """,
                unsafe_allow_html=True
            )

    avg_temp = sum([block['main']['temp'] for block in forecast]) / len(forecast)

    st.markdown("### 🌱 " + translate_text("Recommended Crops", dest_lang))

    with st.container():
        if avg_temp > 30:
            st.success("**🌞 " + translate_text("Hot Climate", dest_lang) + ":** Millets, Sorghum, Groundnut, Cotton")
        elif 20 <= avg_temp <= 30:
            st.success("**🌤️ " + translate_text("Moderate Climate", dest_lang) + ":** Rice, Soybean, Sugarcane, Tomato")
        else:
            st.success("**❄️ " + translate_text("Cool Climate", dest_lang) + ":** Wheat, Barley, Mustard, Peas")

    # Footer spacing
    st.markdown("<br><br>", unsafe_allow_html=True)
