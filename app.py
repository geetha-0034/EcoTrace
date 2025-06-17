import streamlit as st
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load trained model
model = joblib.load("model.pkl")

# UI config
st.set_page_config(page_title="EcoTrace - Carbon Footprint Dashboard", layout="wide")

# ----- HEADER -----
st.markdown("""
    <style>
        .main-title {
            font-size: 36px;
            font-weight: 600;
            color: #1F2937;
        }
        .subtitle {
            font-size: 18px;
            color: #4B5563;
        }
        .metric-box {
            background-color: #F9FAFB;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            text-align: center;
        }
        .metric-box h3 {
            font-size: 24px;
            color: #111827;
        }
        .metric-box p {
            font-size: 16px;
            color: #6B7280;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">EcoTrace: Carbon Footprint Estimator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Predict your carbon impact and get actionable sustainability suggestions</div><hr>', unsafe_allow_html=True)

# ----- INPUTS -----
col1, col2, col3, col4 = st.columns(4)
with col1:
    transport_km = st.number_input("Transport (km)", min_value=0.0, value=100.0)
with col2:
    electricity_kWh = st.number_input("Electricity Usage (kWh)", min_value=0.0, value=50.0)
with col3:
    diet_type = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian"])
with col4:
    waste_kg = st.number_input("Waste Generated (kg)", min_value=0.0, value=5.0)

diet_encoded = 0 if diet_type == "Vegetarian" else 1

# ----- PREDICTION -----
if st.button("Calculate Footprint"):
    input_df = pd.DataFrame([[transport_km, electricity_kWh, diet_encoded, waste_kg]],
                             columns=["Transport_km", "Electricity_kWh", "Diet_Type", "Waste_kg"])
    log_prediction = model.predict(input_df)[0]
    final_prediction = np.expm1(log_prediction)

    st.subheader("Results")
    colA, colB = st.columns(2)
    with colA:
        st.markdown('<div class="metric-box"><h3>{:.2f} kgCO₂</h3><p>Your Carbon Footprint</p></div>'.format(final_prediction), unsafe_allow_html=True)
    with colB:
        st.markdown('<div class="metric-box"><h3>80 kgCO₂</h3><p>Sustainable Average</p></div>', unsafe_allow_html=True)

    # ----- PIE CHART -----
    st.subheader("Footprint Breakdown")
    labels = ['Transport', 'Electricity', 'Diet Impact', 'Waste']
    values = [transport_km, electricity_kWh, diet_encoded * 30, waste_kg]

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%',
                                      startangle=90, colors=['#60A5FA', '#FBBF24', '#10B981', '#EF4444'])
    ax.axis('equal')
    st.pyplot(fig)

    # ----- SUGGESTIONS -----
    st.subheader("Sustainability Suggestions")
    st.info("Here are ways to reduce your carbon footprint:")

    if transport_km > 150:
        st.markdown("- Consider using public transport, carpooling, or cycling for shorter distances.")
    if electricity_kWh > 60:
        st.markdown("- Reduce energy usage with energy-efficient appliances and LED lighting.")
    if diet_encoded == 1:
        st.markdown("- Shifting towards a vegetarian or plant-based diet significantly reduces emissions.")
    if waste_kg > 7:
        st.markdown("- Compost organic waste and reduce single-use plastics.")

# ----- FOOTER -----
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("© 2025 EcoTrace. All rights reserved. | Built for research and awareness purposes only.")
