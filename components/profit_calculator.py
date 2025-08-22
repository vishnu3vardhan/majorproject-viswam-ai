import streamlit as st
from components.translator import translate_text
from components.feedback_button import feedback_button  # Import the feedback component
import pandas as pd
import plotly.graph_objects as go

def show(dest_lang='en'):
    def t(text):
        try:
            return translate_text(text, dest_lang)
        except:
            return text

    # Add the feedback button at the top
    feedback_button("profit_calculator")
    
    st.markdown(
        f"""
        <div style='text-align: center; padding-bottom: 10px;'>
            <h2 style='color:#2E7D32;'>{t("🌾 Crop Profit Calculator")}</h2>
            <p style='color: gray;'>{t("Estimate earnings, analyze performance, and compare multiple crops.")}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.subheader("🔢 " + t("Single Crop Profit Estimator"))

    # --- Single Crop Input Section ---
    col1, col2 = st.columns(2)
    with col1:
        crop_name = st.text_input(t("Crop Name"), placeholder=t("e.g. Wheat"))
        investment = st.number_input(t("Total Investment (₹)"), min_value=0.0, step=100.0, format="%.2f")
    with col2:
        num_bags = st.number_input(t("Total Number of Bags"), min_value=0, step=1)
        market_price_per_bag = st.number_input(t("Market Price per Bag (₹)"), min_value=0.0, step=10.0, format="%.2f")

    st.markdown("---")

    def calculate_crop_profit(investment, num_bags, market_price_per_bag):
        total_revenue = num_bags * market_price_per_bag
        final_profit = total_revenue - investment
        return total_revenue, final_profit

    if st.button(t("📈 Calculate Final Profit"), use_container_width=True):
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
            <h3>📊 {t("Profit Summary")}</h3>
            <p>🌱 <strong>{t('Crop Name')}</strong>: {crop_name if crop_name else 'N/A'}</p>
            <p>💸 <strong>{t('Total Investment')}</strong>: ₹ {investment:,.2f}</p>
            <p>💰 <strong>{t('Total Revenue (from selling bags)')}</strong>: ₹ {total_revenue:,.2f}</p>
            <p>📈 <strong>{t('Final Profit')}</strong>: ₹ {final_profit:,.2f}</p>
        </div>
        """
        st.markdown(summary_html, unsafe_allow_html=True)

        # --- Profit Feedback ---
        if final_profit > 0:
            st.success("✅ " + t("You made a profit!"))
            st.balloons()
        elif final_profit == 0:
            st.info("😐 " + t("No profit, no loss (Break-even)."))
        else:
            st.warning("❌ " + t("You are at a loss. Try optimizing your farming inputs."))

        # --- Visualization: Bar Chart ---
        st.markdown("### 📉 " + t("Investment vs Revenue"))
        fig = go.Figure(data=[
            go.Bar(name='💸 ' + t("Investment"), x=["Investment"], y=[investment], marker_color='#ff7043'),
            go.Bar(name='💰 ' + t("Revenue"), x=["Revenue"], y=[total_revenue], marker_color='#66bb6a')
        ])
        fig.update_layout(barmode='group', height=350)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # --- Optional: Multi-Crop Comparison ---
    st.subheader("🧮 " + t("Compare Multiple Crops"))

    st.markdown(t("Enter crop data below and click compare to analyze profits."))
    with st.form("multi_crop_form"):
        crop_data = st.text_area(
            t("Paste crop data (format: Crop,Investment,Bags,Price)"),
            placeholder=t("Example:\nWheat,10000,20,800\nRice,15000,30,600"),
            height=150
        )
        compare_btn = st.form_submit_button(t("🔍 Compare"))

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
                st.error(t("Error processing row: ") + ", ".join(row))

        if results:
            df = pd.DataFrame(results)
            df["Profit Status"] = df["Profit"].apply(lambda x: "✅ Profit" if x > 0 else "❌ Loss" if x < 0 else "⚖️ Break-even")
            st.dataframe(df.style.applymap(lambda val: 'background-color: #d0f0c0' if isinstance(val, float) and val > 0 else '', subset=['Profit']))

            st.markdown("### 📊 " + t("Crop Comparison Chart"))
            fig = go.Figure()
            fig.add_trace(go.Bar(x=df["Crop"], y=df["Profit"], name="Profit", marker_color='#26a69a'))
            fig.add_trace(go.Bar(x=df["Crop"], y=df["Revenue"], name="Revenue", marker_color='#7cb342'))
            fig.add_trace(go.Bar(x=df["Crop"], y=df["Investment"], name="Investment", marker_color='#ef5350'))
            fig.update_layout(barmode='group', height=400)
            st.plotly_chart(fig, use_container_width=True)