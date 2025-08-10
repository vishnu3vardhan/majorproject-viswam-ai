import streamlit as st
from components.translator import translate_text
import pandas as pd
import plotly.graph_objects as go

def show(dest_lang='en'):
    st.markdown(
        f"""
        <div style='text-align: center; padding-bottom: 10px;'>
            <h2 style='color:#2E7D32;'>{translate_text("🌾 Crop Profit Calculator", dest_lang)}</h2>
            <p style='color: gray;'>{translate_text("Estimate earnings, analyze performance, and compare multiple crops.", dest_lang)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.subheader("🔢 " + translate_text("Single Crop Profit Estimator", dest_lang))

    # --- Single Crop Input Section ---
    col1, col2 = st.columns(2)
    with col1:
        crop_name = st.text_input(translate_text("Crop Name", dest_lang), placeholder=translate_text("e.g. Wheat", dest_lang))
        investment = st.number_input(translate_text("Total Investment (₹)", dest_lang), min_value=0.0, step=100.0, format="%.2f")
    with col2:
        num_bags = st.number_input(translate_text("Total Number of Bags", dest_lang), min_value=0, step=1)
        market_price_per_bag = st.number_input(translate_text("Market Price per Bag (₹)", dest_lang), min_value=0.0, step=10.0, format="%.2f")

    st.markdown("---")

    def calculate_crop_profit(investment, num_bags, market_price_per_bag):
        total_revenue = num_bags * market_price_per_bag
        final_profit = total_revenue - investment
        return total_revenue, final_profit

    if st.button(translate_text("📈 Calculate Final Profit", dest_lang), use_container_width=True):
        total_revenue, final_profit = calculate_crop_profit(investment, num_bags, market_price_per_bag)

        # --- Summary Display ---
        summary_html = f"""
        <div style="
            background-color: #1e1e1e;
            color: white;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #333;
            margin-bottom: 20px;
        ">
            <h3>📊 {translate_text("Profit Summary", dest_lang)}</h3>
            <p>🌱 <strong>{translate_text('Crop Name', dest_lang)}</strong>: {crop_name if crop_name else 'N/A'}</p>
            <p>💸 <strong>{translate_text('Total Investment', dest_lang)}</strong>: ₹ {investment:,.2f}</p>
            <p>💰 <strong>{translate_text('Total Revenue (from selling bags)', dest_lang)}</strong>: ₹ {total_revenue:,.2f}</p>
            <p>📈 <strong>{translate_text('Final Profit', dest_lang)}</strong>: ₹ {final_profit:,.2f}</p>
        </div>
        """
        st.markdown(summary_html, unsafe_allow_html=True)

        # --- Profit Feedback ---
        if final_profit > 0:
            st.success("✅ " + translate_text("You made a profit!", dest_lang))
            st.balloons()
        elif final_profit == 0:
            st.info("😐 " + translate_text("No profit, no loss (Break-even).", dest_lang))
        else:
            st.warning("❌ " + translate_text("You are at a loss. Try optimizing your farming inputs.", dest_lang))

        # --- Visualization: Bar Chart ---
        st.markdown("### 📉 " + translate_text("Investment vs Revenue", dest_lang))
        fig = go.Figure(data=[
            go.Bar(name='💸 ' + translate_text("Investment", dest_lang), x=["Investment"], y=[investment], marker_color='#ff7043'),
            go.Bar(name='💰 ' + translate_text("Revenue", dest_lang), x=["Revenue"], y=[total_revenue], marker_color='#66bb6a')
        ])
        fig.update_layout(barmode='group', height=350)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # --- Optional: Multi-Crop Comparison ---
    st.subheader("🧮 " + translate_text("Compare Multiple Crops", dest_lang))

    st.markdown(translate_text("Enter crop data below and click compare to analyze profits.", dest_lang))
    with st.form("multi_crop_form"):
        crop_data = st.text_area(
            translate_text("Paste crop data (format: Crop,Investment,Bags,Price)", dest_lang),
            placeholder=translate_text("Example:\nWheat,10000,20,800\nRice,15000,30,600", dest_lang),
            height=150
        )
        compare_btn = st.form_submit_button(translate_text("🔍 Compare", dest_lang))

    if compare_btn and crop_data:
        rows = [line.split(",") for line in crop_data.strip().split("\n") if len(line.split(",")) == 4]
        results = []

        for row in rows:
            try:
                name = row[0].strip()
                invest = float(row[1])
                bags = int(row[2])
                price = float(row[3])
                revenue = bags * price
                profit = revenue - invest
                results.append({
                    "Crop": name,
                    "Investment": invest,
                    "Revenue": revenue,
                    "Profit": profit
                })
            except:
                st.error(translate_text("Error processing row: ", dest_lang) + ", ".join(row))

        if results:
            df = pd.DataFrame(results)
            df["Profit Status"] = df["Profit"].apply(lambda x: "✅ Profit" if x > 0 else "❌ Loss" if x < 0 else "⚖️ Break-even")
            st.dataframe(df.style.applymap(lambda val: 'background-color: #d0f0c0' if isinstance(val, float) and val > 0 else '', subset=['Profit']))

            st.markdown("### 📊 " + translate_text("Crop Comparison Chart", dest_lang))
            fig = go.Figure()
            fig.add_trace(go.Bar(x=df["Crop"], y=df["Profit"], name="Profit", marker_color='#26a69a'))
            fig.add_trace(go.Bar(x=df["Crop"], y=df["Revenue"], name="Revenue", marker_color='#7cb342'))
            fig.add_trace(go.Bar(x=df["Crop"], y=df["Investment"], name="Investment", marker_color='#ef5350'))
            fig.update_layout(barmode='group', height=400)
            st.plotly_chart(fig, use_container_width=True)
