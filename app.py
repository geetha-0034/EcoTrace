import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("model.pkl")

# Streamlit app layout
st.set_page_config(page_title="EcoTrace", layout="centered")
st.title("🌍 EcoTrace: Carbon Footprint Predictor")
st.markdown("Estimate your carbon footprint based on transport, energy, diet, and waste!")

# Input form
transport_km = st.number_input("🚗 Transport (km traveled)", min_value=0.0)
electricity_kWh = st.number_input("⚡ Electricity usage (kWh)", min_value=0.0)
diet_type = st.selectbox("🥗 Diet Type", options=["Vegetarian", "Non-Vegetarian"])
waste_kg = st.number_input("🗑️ Waste generated (kg)", min_value=0.0)

# Encode diet
diet_encoded = 0 if diet_type == "Vegetarian" else 1

if st.button("Predict My Carbon Footprint"):
    # Prepare input
    input_data = pd.DataFrame([[transport_km, electricity_kWh, diet_encoded, waste_kg]],
                              columns=["Transport_km", "Electricity_kWh", "Diet_Type", "Waste_kg"])
    
    # Predict and inverse log1p
    log_prediction = model.predict(input_data)[0]
    final_prediction = np.expm1(log_prediction)
    
    st.success(f"Estimated Carbon Footprint: **{round(final_prediction, 2)} kgCO₂**")

    st.markdown("---")
    st.caption("Note: This is an estimate based on simplified data.")


