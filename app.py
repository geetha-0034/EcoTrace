import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

# Load your model
model = joblib.load("model.pkl")

# Page settings
st.set_page_config(page_title="EcoTrace – Carbon Footprint Estimator", layout="centered")

# Inject custom CSS
st.markdown("""
    <style>
    .main {
        background-image: url('https://images.unsplash.com/photo-1547721064-da6cfb341d50?auto=format&fit=crop&w=1950&q=80');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .glass-box {
        background: rgba(255, 255, 255, 0.90);
        padding: 2.5rem 3rem;
        border-radius: 15px;
        max-width: 500px;
        margin: 4rem auto;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        color: #000000;
    }
    .title {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: left;
        margin-bottom: 2rem;
        color: white;
    }
    .title span {
        color: #f77f00;
    }
    .suggestions {
        margin-top: 1rem;
        font-size: 0.9rem;
        color: #333333;
    }
    </style>
""", unsafe_allow_html=True)

# Header text
st.markdown('<div class="title">What\'s the <span>carbon footprint</span> of your lifestyle?</div>', unsafe_allow_html=True)

# Input box (glass)
st.markdown('<div class="glass-box">', unsafe_allow_html=True)

# Inputs
transport_km = st.number_input("Transport (km traveled)", min_value=0.0)
electricity_kWh = st.number_input("Electricity usage (kWh)", min_value=0.0)
diet_type = st.selectbox("Diet Type", options=["Vegetarian", "Non-Vegetarian"])
waste_kg = st.number_input("Waste generated (kg)", min_value=0.0)

# Prediction
if st.button("Calculate My Emissions"):
    diet_encoded = 0 if diet_type == "Vegetarian" else 1

    input_data = pd.DataFrame([[transport_km, electricity_kWh, diet_encoded, waste_kg]],
                              columns=["Transport_km", "Electricity_kWh", "Diet_Type", "Waste_kg"])

    log_prediction = model.predict(input_data)[0]
    final_prediction = np.expm1(log_prediction)

    st.success(f"Your estimated carbon footprint is: **{round(final_prediction, 2)} kgCO₂**")

    # Suggestions section
    st.markdown("### Suggestions")
    tips = []

    if transport_km > 100:
        tips.append("🚗 Consider using public transport or carpooling.")
    if electricity_kWh > 200:
        tips.append("💡 Try using energy-efficient lighting or appliances.")
    if diet_type == "Non-Vegetarian":
        tips.append("🥦 A vegetarian diet once a week reduces your impact.")
    if waste_kg > 10:
        tips.append("♻️ Recycle and compost organic waste.")

    if tips:
        for tip in tips:
            st.markdown(f"- {tip}")
    else:
        st.info("You're doing great already! 🌿")

st.markdown('</div>', unsafe_allow_html=True)
