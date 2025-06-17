import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# Load model
model = joblib.load("model.pkl")

# Page config
st.set_page_config(page_title="EcoTrace", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #e0f7fa, #ffffff);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .hero {
            background-image: url('https://images.unsplash.com/photo-1508780709619-79562169bc64');
            background-size: cover;
            background-position: center;
            padding: 3rem;
            border-radius: 10px;
            color: white;
            text-shadow: 1px 1px 2px black;
        }
        .title-text {
            font-size: 2.5rem;
            font-weight: 700;
        }
        .sub-text {
            font-size: 1.2rem;
        }
        .stButton>button {
            background-color: #007200;
            color: white;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Header Hero Banner
st.markdown("""
    <div class="hero">
        <div class="title-text">🌍 EcoTrace</div>
        <div class="sub-text">AI-Powered Carbon Footprint Estimator</div>
    </div>
""", unsafe_allow_html=True)

# Input Section
st.markdown("### 🔍 Enter Your Details")

transport_km = st.number_input("🚗 Kilometers Travelled (Transport)", min_value=0.0, step=1.0)
electricity_kWh = st.number_input("⚡ Electricity Consumed (kWh)", min_value=0.0, step=1.0)
diet_type = st.selectbox("🍽️ Diet Type", ["Vegetarian", "Non-Vegetarian"])
waste_kg = st.number_input("🗑️ Waste Produced (kg)", min_value=0.0, step=1.0)

diet_encoded = 0 if diet_type == "Vegetarian" else 1

# Prediction logic
if st.button("Predict My Carbon Footprint"):
    input_data = pd.DataFrame([[transport_km, electricity_kWh, diet_encoded, waste_kg]],
                               columns=["Transport_km", "Electricity_kWh", "Diet_Type", "Waste_kg"])
    log_prediction = model.predict(input_data)[0]
    final_prediction = np.expm1(log_prediction)
    
    st.markdown("## ✅ Result Summary")
    col1, col2 = st.columns(2)
    col1.metric("🌿 Your Carbon Footprint", f"{round(final_prediction, 2)} kgCO₂")
    col2.metric("♻️ Global Sustainable Avg", "80 kgCO₂")

    # Pie chart
    st.markdown("### 📊 Footprint Breakdown")
    labels = ['Transport', 'Electricity', 'Diet', 'Waste']
    values = [transport_km, electricity_kWh, diet_encoded*20, waste_kg]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # Suggestions
    st.markdown("### 🧠 Smart Suggestions for Sustainability")

    if transport_km > 100:
        st.warning("🚴‍♀️ Try cycling, public transport, or carpooling to reduce travel emissions.")
    if electricity_kWh > 70:
        st.info("💡 Consider switching to LED bulbs and turning off unused appliances.")
    if diet_encoded == 1:
        st.warning("🌱 Switching to a vegetarian or plant-based diet significantly lowers carbon footprint.")
    if waste_kg > 8:
        st.info("♻️ Reduce single-use plastics and compost organic waste when possible.")

    st.markdown("---")
    st.caption("📘 EcoTrace helps raise awareness of your environmental impact. Think, Act, Change.")

