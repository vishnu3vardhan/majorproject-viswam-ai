import streamlit as st
import json
from pages import home, record_keeping, disease_detection

# Set page config
st.set_page_config(page_title="FarminAI Assistant", page_icon="assests/logo.png", layout="wide")

# Sidebar
st.sidebar.image("assests/logo.png", width=120)
st.sidebar.title("🚜 FarminAI Navigation")

# Navigation Options
page = st.sidebar.radio("Go to", (
    "Home",
    "Disease Detection",
    "Farm Record Keeping",
    "Profit Calculator",
    "Crop Suggestion"
))

# Page Routing
if page == "Home":
    home.show()

elif page == "Disease Detection":
    st.sidebar.subheader("Detection Type")
    detection_type = st.sidebar.radio("Select Type", ("Poultry", "Cow", "Crop"))

    if detection_type == "Poultry":
        disease_detection.poultry_disease_detection()
    elif detection_type == "Cow":
        disease_detection.cow_disease_detection()
    elif detection_type == "Crop":
        disease_detection.crop_disease_detection()

elif page == "Farm Record Keeping":
    record_keeping.show()

elif page == "Profit Calculator":
    st.title("🌾 Crop Profit Calculator")

    crop_name = st.text_input("Enter Crop Name", placeholder="e.g. Wheat, Rice, Maize")
    investment = st.number_input("Enter Total Investment (₹)", min_value=0.0, step=100.0)
    num_bags = st.number_input("Enter Total Number of Bags", min_value=0, step=1)
    market_price_per_bag = st.number_input("Enter Market Price per Bag (₹)", min_value=0.0, step=10.0)

    def calculate_crop_profit(investment, num_bags, market_price_per_bag):
        total_revenue = num_bags * market_price_per_bag
        final_profit = total_revenue - investment
        return total_revenue, final_profit

    if st.button("Calculate Final Profit"):
        total_revenue, final_profit = calculate_crop_profit(investment, num_bags, market_price_per_bag)

        st.subheader("📊 Profit Summary")
        st.write(f"🌱 **Crop Name:** {crop_name if crop_name else 'N/A'}")
        st.write(f"💸 **Total Investment:** ₹ {investment:,.2f}")
        st.write(f"💰 **Total Revenue (from selling bags):** ₹ {total_revenue:,.2f}")
        st.write(f"📈 **Final Profit:** ₹ {final_profit:,.2f}")

        if final_profit > 0:
            st.success("✅ You made a profit!")
            st.balloons()
        elif final_profit == 0:
            st.info("😐 No profit, no loss (Break-even).")
        else:
            st.warning("❌ You are at a loss. Try optimizing your farming inputs.")

elif page == "Crop Suggestion":
    st.title("🌿 Crop Suggestion Based on Season")

    try:
        with open("data/crop_data.json") as f:
            crop_data = json.load(f)
    except FileNotFoundError:
        st.error("❌ crop_data.json not found in data/ folder.")
    else:
        season_input = st.text_input(
            "Enter Season (e.g. Summer, Winter, Monsoon)",
            placeholder="Type a season..."
        )

        if season_input:
            matching_crops = [
                crop for crop in crop_data
                if crop["season"].strip().lower() == season_input.strip().lower()
            ]

            if matching_crops:
                for crop in matching_crops:
                    st.subheader(f"🌾 Suggested Crop: {crop['crop']}")
                    st.markdown(f"""
                    - **Season:** {crop['season']}
                    - **Weather Condition:** {crop['weather']}
                    - **Soil Type:** {crop['soil']}
                    - **Duration:** {crop['duration']}
                    - **Investment:** {crop['investment']}
                    - **Expected Profit:** {crop['profit']}
                    - **How to Start:** {crop['how_to_start']}
                    """)
            else:
                st.warning(f"⚠ No crop suggestions found for season: {season_input}")
        else:
            st.info("Please enter a season to get suggestions.")
