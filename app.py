import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model and scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pk1")

# Features expected
features = ['Transport_km', 'Electricity_kWh', 'Diet_Type', 'Waste_kg']

# Page settings and background
st.set_page_config(page_title="Carbon Footprint Calculator", layout="centered")
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1508780709619-79562169bc64');
        background-size: cover;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Main UI
st.title("🌱 What's the **carbon footprint** of your website?")
st.markdown("Learn what emissions your website is producing and how to offset and reduce them long-term.")

with st.form("carbon_form"):
    st.subheader("Enter your usage details:")

    name = st.text_input("Your Name")
    website = st.text_input("Your Website URL")
    email = st.text_input("Your Email")

    transport = st.number_input("Average Transport (km)", min_value=0)
    electricity = st.number_input("Electricity Use (kWh)", min_value=0)
    diet = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian"])
    waste = st.number_input("Waste Generated (kg)", min_value=0)

    submitted = st.form_submit_button("🌍 Calculate my emissions")

    if submitted:
        diet_type = 0 if diet == "Vegetarian" else 1
        input_data = pd.DataFrame([[transport, electricity, diet_type, waste]], columns=features)

        # Scale the input if scaler is used
        input_scaled = scaler.transform(input_data)
        pred_log = model.predict(input_scaled)
        footprint = np.expm1(pred_log[0])  # if model used log1p target

        st.success(f"Estimated Carbon Footprint: **{round(footprint, 2)} kgCO₂**")

# Learn more section
with st.expander("Not ready to get started? Learn more!"):
    st.markdown("This calculator estimates your website’s carbon footprint using key input factors.")
