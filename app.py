import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load model
model = joblib.load("model.pkl")

# Set layout
st.set_page_config(page_title="EcoTrace | Carbon Footprint Predictor", layout="centered")

# Branding
st.title("🌍 EcoTrace")
st.subheader("Predict and Reduce Your Carbon Footprint")
st.markdown("---")

st.markdown("Fill in your lifestyle details below to estimate your carbon emissions and receive tailored suggestions for improvement.")

# Inputs
col1, col2 = st.columns(2)
with col1:
    transport_km = st.number_input("🚗 Distance Traveled (km)", min_value=0.0, step=1.0)
    electricity_kWh = st.number_input("⚡ Electricity Used (kWh)", min_value=0.0, step=1.0)
with col2:
    diet_type = st.selectbox("🥗 Diet Type", ["Vegetarian", "Non-Vegetarian"])
    waste_kg = st.number_input("🗑️ Waste Produced (kg)", min_value=0.0, step=1.0)

diet_encoded = 0 if diet_type == "Vegetarian" else 1

if st.button("🔍 Predict My Footprint"):
    input_df = pd.DataFrame([[transport_km, electricity_kWh, diet_encoded, waste_kg]],
                            columns=["Transport_km", "Electricity_kWh", "Diet_Type", "Waste_kg"])
    log_prediction = model.predict(input_df)[0]
    final_prediction = np.expm1(log_prediction)

    st.success(f"🌡️ Estimated Carbon Footprint: **{round(final_prediction, 2)} kgCO₂**")
    st.markdown("---")

    # 🎯 Suggestions
    st.subheader("♻️ Suggestions to Reduce Your Footprint")

    if transport_km > 100:
        st.warning("🚲 Consider using public transport or biking for shorter distances.")
    if electricity_kWh > 50:
        st.info("💡 Switch to energy-efficient appliances or renewable energy sources.")
    if diet_encoded == 1:
        st.error("🥕 Try incorporating more plant-based meals into your diet.")
    if waste_kg > 5:
        st.success("🔄 Start composting organic waste and reduce single-use plastics.")

    st.caption("Suggestions are generated based on typical carbon emission trends. Actual impact may vary.")

# Footer
st.markdown("---")
st.markdown("💚 _Built with Machine Learning and Streamlit by Geetha Inaganti_")
