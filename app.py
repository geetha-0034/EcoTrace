import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("model.pkl")

# Set Streamlit page configuration
st.set_page_config(page_title="EcoTrace - Carbon Footprint Estimator", layout="centered")

# Inject CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1950&q=80");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .glass-box {
        background: rgba(255, 255, 255, 0.20);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        max-width: 500px;
        margin: 40px auto;
    }

    .hero-text {
        font-size: 2.5rem;
        font-weight: bold;
        color: white;
        text-align: left;
        margin-bottom: 1.2rem;
    }

    .highlight {
        color: #52c41a;
    }

    .footer {
        text-align: center;
        color: white;
        font-size: 14px;
        margin-top: 2rem;
    }

    .result-box {
        font-size: 1.2rem;
        color: #333;
        text-align: center;
        background-color: #ffffffd9;
        padding: 1rem;
        margin-top: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<div class="hero-text">What\'s the <span class="highlight">carbon footprint</span><br>of your lifestyle?</div>', unsafe_allow_html=True)

# Form Section
with st.container():
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)

    transport_km = st.number_input("Transport (km traveled)", min_value=0.0)
    electricity_kWh = st.number_input("Electricity usage (kWh)", min_value=0.0)
    diet_type = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian"])
    waste_kg = st.number_input("Waste generated (kg)", min_value=0.0)

    if st.button("Calculate My Emissions"):
        diet_encoded = 0 if diet_type == "Vegetarian" else 1
        input_data = pd.DataFrame([[transport_km, electricity_kWh, diet_encoded, waste_kg]],
                                  columns=["Transport_km", "Electricity_kWh", "Diet_Type", "Waste_kg"])
        log_prediction = model.predict(input_data)[0]
        final_prediction = np.expm1(log_prediction)

        # Suggestions
        suggestions = []
        if transport_km > 100:
            suggestions.append("Consider using public transport or carpooling to reduce emissions.")
        if electricity_kWh > 200:
            suggestions.append("Switch to energy-efficient appliances or renewable sources.")
        if diet_type == "Non-Vegetarian":
            suggestions.append("Try reducing meat consumption for a smaller diet footprint.")
        if waste_kg > 10:
            suggestions.append("Practice recycling and composting to reduce waste impact.")

        st.markdown(f'<div class="result-box"><strong>Your estimated carbon footprint:</strong> {round(final_prediction, 2)} kgCO₂</div>', unsafe_allow_html=True)

        if suggestions:
            st.markdown("### Recommendations to Reduce Footprint:")
            for tip in suggestions:
                st.markdown(f"- {tip}")
        else:
            st.success("Awesome! Your choices already support sustainability.")

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">Want to know how we calculate this? <a href="#" style="color: #FFD700;">Learn more</a></div>', unsafe_allow_html=True)
