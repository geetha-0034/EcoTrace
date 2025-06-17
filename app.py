import streamlit as st
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load trained model
model = joblib.load("model.pkl")

# UI config
st.set_page_config(page_title="EcoTrace - Carbon Footprint Dashboard", layout="wide")

# ----- STYLING -----
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://www.aprildialog.com/wp-content/uploads/2014/02/forest-photo.jpg");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        .main-title {
            font-size: 52px;
            font-weight: 800;
            color: #ffffff;
            text-align: center;
        }
        .subtitle {
            font-size: 32px;
            color: #e5e7eb;
            text-align: center;
            margin-bottom: 1rem;
        }
        label[data-testid="stWidgetLabel"] {
           font-size: 24px !important;
           font-weight: 600;
           color: #ffffff; 
        }
        .metric-box {
            background-color: #F9FAFB;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            text-align: center;
        }
        .metric-box h3 {
            font-size: 28px;
            color: #111827;
        }
        .metric-box p {
            font-size: 28px;
            color: #6B7280;
        }
    </style>
""", unsafe_allow_html=True)

# ----- TITLE -----
st.markdown('<div class="main-title">EcoTrace: Carbon Footprint Estimator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Predict your carbon impact and receive actionable sustainability suggestions</div>', unsafe_allow_html=True)

# ----- USER INPUT FORM -----
st.markdown('<div class="glass-box">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    transport_km = st.number_input("Transport (km)", min_value=0.0, value=100.0)
    electricity_kWh = st.number_input("Electricity Usage (kWh)", min_value=0.0, value=50.0)
with col2:
    diet_type = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian"])
    waste_kg = st.number_input("Waste Generated (kg)", min_value=0.0, value=5.0)

diet_encoded = 0 if diet_type == "Vegetarian" else 1

# ----- CALCULATE FOOTPRINT -----
if st.button("Calculate Footprint"):
    input_df = pd.DataFrame([[transport_km, electricity_kWh, diet_encoded, waste_kg]],
                             columns=["Transport_km", "Electricity_kWh", "Diet_Type", "Waste_kg"])
    log_prediction = model.predict(input_df)[0]
    final_prediction = np.expm1(log_prediction)

    # ----- METRICS DISPLAY -----
    st.subheader("Results")
    colA, colB = st.columns(2)
    with colA:
        st.markdown(f'<div class="metric-box"><h3>{final_prediction:.2f} kgCO₂</h3><p>Your Carbon Footprint</p></div>', unsafe_allow_html=True)
    with colB:
        st.markdown(f'<div class="metric-box"><h3>80 kgCO₂</h3><p>Sustainable Average</p></div>', unsafe_allow_html=True)

    # ----- PIE CHART -----
    st.subheader("Footprint Breakdown")
    labels = ['Transport', 'Electricity', 'Diet Impact', 'Waste']
    values = [transport_km, electricity_kWh, 30 if diet_encoded else 10, waste_kg]

    fig, ax = plt.subplots(figsize=(7, 5))
    wedges, texts, autotexts = ax.pie(values,
                                      labels=None,
                                      autopct='%1.1f%%',
                                      startangle=90,
                                      wedgeprops={'edgecolor': 'white'},
                                      pctdistance=0.85)
    ax.axis('equal')
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    plt.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0.5), title="Categories")
    st.pyplot(fig)

    # ----- SUSTAINABILITY SUGGESTIONS -----
    st.subheader("Sustainability Suggestions")
    suggestions = []

    if transport_km >= 50:
        suggestions.append("🚗 Reduce private vehicle usage by opting for public transport or carpooling.")
    if electricity_kWh >= 40:
        suggestions.append("⚡ Upgrade to energy-efficient appliances and turn off unused devices.")
    if diet_encoded == 1:
        suggestions.append("🥦 Incorporate more plant-based meals to reduce dietary emissions.")
    if waste_kg >= 4:
        suggestions.append("🗑️ Practice composting and minimize single-use plastics.")

    if suggestions:
        for tip in suggestions:
            st.markdown(f"- {tip}")
    else:
        st.success("Your footprint is already quite low. Keep it up!")

st.markdown('</div>', unsafe_allow_html=True)

# ----- FOOTER -----
st.markdown("<hr>", unsafe_allow_html=True)
