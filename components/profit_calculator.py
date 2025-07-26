import streamlit as st
from components.translator import translate_text

def show(dest_lang='en'):
    st.title(translate_text(" 🌾Crop Profit Calculator", dest_lang))

    crop_name = st.text_input(translate_text("Enter Crop Name", dest_lang), placeholder=translate_text("e.g. Wheat, Rice, Maize", dest_lang))
    investment = st.number_input(translate_text("Enter Total Investment (₹)", dest_lang), min_value=0.0, step=100.0)
    num_bags = st.number_input(translate_text("Enter Total Number of Bags", dest_lang), min_value=0, step=1)
    market_price_per_bag = st.number_input(translate_text("Enter Market Price per Bag (₹)", dest_lang), min_value=0.0, step=10.0)

    def calculate_crop_profit(investment, num_bags, market_price_per_bag):
        total_revenue = num_bags * market_price_per_bag
        final_profit = total_revenue - investment
        return total_revenue, final_profit

    if st.button(translate_text("Calculate Final Profit", dest_lang)):
        total_revenue, final_profit = calculate_crop_profit(investment, num_bags, market_price_per_bag)

        st.subheader(translate_text("📊 Profit Summary", dest_lang))
        st.write(f"🌱 **{translate_text('Crop Name', dest_lang)}:** {crop_name if crop_name else 'N/A'}")
        st.write(f"💸 **{translate_text('Total Investment', dest_lang)}:** ₹ {investment:,.2f}")
        st.write(f"💰 **{translate_text('Total Revenue (from selling bags)', dest_lang)}:** ₹ {total_revenue:,.2f}")
        st.write(f"📈 **{translate_text('Final Profit', dest_lang)}:** ₹ {final_profit:,.2f}")

        if final_profit > 0:
            st.success(translate_text("✅ You made a profit!", dest_lang))
            st.balloons()
        elif final_profit == 0:
            st.info(translate_text("😐 No profit, no loss (Break-even).", dest_lang))
        else:
            st.warning(translate_text("❌ You are at a loss. Try optimizing your farming inputs.", dest_lang))
