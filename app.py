import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load the model
model = joblib.load("model.pkl")

# ----- PAGE SETUP -----
st.set_page_config(page_title="EcoTrace Landing", layout="centered")

# ----- CUSTOM CSS -----
st.markdown("""
    <style>
    body {
        margin: 0;
        padding: 0;
        font-family: Arial, sans-serif;
    }
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1598670859841-0b9f9e2c9d9a?auto=format&fit=crop&w=1950&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: white;
    }
    .form-card {
        background: rgba(0, 128, 128, 0.8); /* Teal with transparency */
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(7px);
        -webkit-backdrop-filter: blur(7px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        max-width: 400px;
        margin: auto;
        margin-top: 50px;
    }
    .hero {
        font-size: 2.5rem;
        font-weight: 700;
        color: #fff;   
        text-align: left;
        margin-bottom: 1.5rem;
    }
    .highlight {
        color: #ff914d;
    }
    .footer {
        text-align: center;
        color: #fff;
        margin-top: 40px;
        font-size: 16px;
    }
    input {
        border-radius: 10px !important;
        padding: 10px;
        width: 100%;
        margin-bottom: 15px;
        background-color: rgba(255, 255, 255, 0.2);
        border: none;
        color: white;
    }
    button {
        background-color: #FFD700;
        color: black;
        border: none;
        padding: 10px 20px;
        border-radius: 10px;
        cursor: pointer;
        font-size: 16px;
    }
    button:hover {
        background-color: #FCD975;
    }
    </style>
""", unsafe_allow_html=True)

# ----- HERO HEADER -----
st.markdown('<div class="hero">What\'s the <span class="highlight">carbon footprint</span><br>of your lifestyle?</div>', unsafe_allow_html=True)

# ----- FORM CARD -----
with st.container():
    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    # Form inputs
    transport_km = st.number_input("Transport (km traveled)", min_value=0.0, step=1.0, format="%.2f")
    electricity_kWh = st.number_input("Electricity usage (kWh)", min_value=0.0, step=1.0, format="%.2f")
    diet_type = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian"])
    waste_kg = st.number_input("Waste generated (kg)", min_value=0.0, step=1.0, format="%.2f")

    if st.button("Calculate My Emissions"):
        diet_encoded = 0 if diet_type == "Vegetarian" else 1
        input_data = pd.DataFrame([[transport_km, electricity_kWh, diet_encoded, waste_kg]],
                                  columns=["Transport_km", "Electricity_kWh", "Diet_Type", "Waste_kg"])
        log_prediction = model.predict(input_data)[0]
        final_prediction = np.expm1(log_prediction)
        st.success(f"🌱 Your estimated carbon footprint: {round(final_prediction, 2)} kgCO₂")

    st.markdown('</div>', unsafe_allow_html=True)

# ----- FOOTER -----
st.markdown('<div class="footer">Not ready to get started? <a style="color:#FFD700" href="#">Learn more</a></div>', unsafe_allow_html=True)
