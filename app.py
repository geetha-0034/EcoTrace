import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

# Load the trained model
model = joblib.load("model.pkl")

# Streamlit page config
st.set_page_config(page_title="EcoTrace – Carbon Footprint Estimator", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    body {
        color: #fff;
    }
    .main {
        background-image: url('https://images.unsplash.com/photo-1523978591478-c753949ff840?auto=format&fit=crop&w=1950&q=80');
        background-size: cover;
        background-attachment: fixed;
    }
    .glass-box {
        background: rgba(255,255,255,0.9);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.2);
        color: #000000;
    }
    .title-text {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    .highlight {
        color: #34A853;
    }
    .footer {
        text-align: center;
        font-size: 14px;
        margin-top: 2rem;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="title-text">What\'s the <span class="highlight">carbon footprint</span> of your lifestyle?</div>', unsafe_allow_html=True)

# LAYOUT
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)

    transport_km = st.number_input("🚗 Transport (km traveled)", min_value=0.0)
    electricity_kWh = st.number_input("⚡ Electricity usage (kWh)", min_value=0.0)
    diet_type = st.selectbox("🥗 Diet Type", options=["Vegetarian", "Non-Vegetarian"])
    waste_kg = st.number_input("🗑️ Waste generated (kg)", min_value=0.0)

    if st.button("Calculate My Emissions"):
        diet_encoded = 0 if diet_type == "Vegetarian" else 1

        input_data = pd.DataFrame([[transport_km, electricity_kWh, diet_encoded, waste_kg]],
                                  columns=["Transport_km", "Electricity_kWh", "Diet_Type", "Waste_kg"])
        
        log_prediction = model.predict(input_data)[0]
        final_prediction = np.expm1(log_prediction)

        st.success(f"Your estimated carbon footprint is: **{round(final_prediction, 2)} kgCO₂**")

        # 💡 Suggestion logic
        st.markdown("### Recommendations")
        suggestions = []

        if transport_km > 100:
            suggestions.append("🚙 Try using public transport, cycling, or carpooling.")
        if electricity_kWh > 200:
            suggestions.append("💡 Switch to energy-efficient appliances or solar power.")
        if diet_type == "Non-Vegetarian":
            suggestions.append("🥦 Consider a plant-based diet once or twice a week.")
        if waste_kg > 10:
            suggestions.append("♻️ Practice recycling and composting.")

        if suggestions:
            for tip in suggestions:
                st.markdown(f"- {tip}")
        else:
            st.info("Great job! You're already making eco-conscious choices. 🌿")

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if "final_prediction" in locals():
        # FOOTPRINT PIE CHART
        labels = ["Transport", "Electricity", "Diet", "Waste"]
        values = np.array([transport_km, electricity_kWh, diet_encoded * 50, waste_kg])  # Adjust weights
        total = values.sum()
        if total == 0:
            values = [1, 1, 1, 1]
            total = 4

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

# FOOTER
st.markdown('<div class="footer">Want to learn more about reducing your footprint? <a href="https://www.epa.gov/environmental-topics/greener-living" style="color: #FFD700;">Click here</a></div>', unsafe_allow_html=True)
