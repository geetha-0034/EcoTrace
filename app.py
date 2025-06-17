import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# Load model
model = joblib.load("model.pkl")

# Page Configuration
st.set_page_config(
    page_title="EcoTrace - Carbon Footprint Estimator",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Clean White UI with soft blue accents
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #333333;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #666666;
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #00416A;
        margin-top: 40px;
        margin-bottom: 10px;
    }
    .metric-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #dddddd;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-title">EcoTrace: Carbon Footprint Estimator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Estimate and visualize your environmental impact based on lifestyle inputs</div>', unsafe_allow_html=True)
st.markdown("---")

# Input Fields
st.markdown('<div class="section-title">Input Your Data</div>', unsafe_allow_html=True)

transport_km = st.number_input("Transport Distance (km)", min_value=0.0)
electricity_kWh = st.number_input("Electricity Consumption (kWh)", min_value=0.0)
diet_type = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian"])
waste_kg = st.number_input("Waste Produced (kg)", min_value=0.0)

diet_encoded = 0 if diet_type == "Vegetarian" else 1

# Predict Button
if st.button("Estimate Carbon Footprint"):
    input_df = pd.DataFrame([[transport_km, electricity_kWh, diet_encoded, waste_kg]],
                             columns=["Transport_km", "Electricity_kWh", "Diet_Type", "Waste_kg"])
    log_prediction = model.predict(input_df)[0]
    final_prediction = np.expm1(log_prediction)

    # Display Metrics
    st.markdown('<div class="section-title">Results</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="metric-box">')
        st.metric("Your Carbon Footprint", f"{round(final_prediction, 2)} kgCO₂")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box">')
        st.metric("Sustainable Average", "80 kgCO₂")
        st.markdown('</div>', unsafe_allow_html=True)

    # Pie Chart
    st.markdown('<div class="section-title">Footprint Breakdown</div>', unsafe_allow_html=True)
    labels = ['Transport', 'Electricity', 'Diet Impact', 'Waste']
    values = [transport_km, electricity_kWh, diet_encoded * 20, waste_kg]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # Suggestions
    st.markdown('<div class="section-title">Suggestions for Improvement</div>', unsafe_allow_html=True)

    if transport_km > 100:
        st.write("- Consider reducing private vehicle use. Explore shared mobility or public transport.")
    if electricity_kWh > 75:
        st.write("- Use energy-efficient appliances and monitor standby power consumption.")
    if diet_encoded == 1:
        st.write("- Shifting towards plant-based meals can reduce emissions significantly.")
    if waste_kg > 8:
        st.write("- Practice waste segregation and composting to manage organic waste better.")

    st.markdown("---")
    st.caption("EcoTrace by Geetha Inaganti | Built with Streamlit & ML | v1.0")
