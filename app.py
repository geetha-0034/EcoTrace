import streamlit as st
import numpy as np
import pandas as pd
import joblib
import base64
from PIL import Image
import matplotlib.pyplot as plt

# Load trained model
model = joblib.load("model.pkl")

# Set page config
st.set_page_config(page_title="EcoTrace - Carbon Footprint", layout="centered")

# Set background image
def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .card {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 15px;
            max-width: 600px;
            margin: 2rem auto;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }}
        .header-title {{
            text-align: center;
            font-size: 2.5rem;
            color: #1a1a1a;
            font-weight: 700;
        }}
        .orange-text {{
            color: orange;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# Apply background
set_background("green_bg.png")  # Replace with your own greenery image

# Title Header
st.markdown('<div class="header-title">What\'s the <span class="orange-text">carbon footprint</span><br>of your lifestyle?</div>', unsafe_allow_html=True)

# Input Form Card
st.markdown('<div class="card">', unsafe_allow_html=True)

transport_km = st.number_input("Transport (km traveled)", min_value=0.0, value=0.0)
electricity_kWh = st.number_input("Electricity usage (kWh)", min_value=0.0, value=0.0)
diet_type = st.selectbox("Diet Type", options=["Vegetarian", "Non-Vegetarian"])
waste_kg = st.number_input("Waste generated (kg)", min_value=0.0, value=0.0)

if st.button("Calculate My Emissions"):
    diet_encoded = 0 if diet_type == "Vegetarian" else 1
    input_df = pd.DataFrame([[transport_km, electricity_kWh, diet_encoded, waste_kg]],
                            columns=["Transport_km", "Electricity_kWh", "Diet_Type", "Waste_kg"])
    log_prediction = model.predict(input_df)[0]
    final_prediction = round(np.expm1(log_prediction), 2)

    st.subheader("Results")
    st.metric("Your Carbon Footprint", f"{final_prediction} kgCO₂")
    sustainable_avg = 80.0
    st.metric("Sustainable Average", f"{sustainable_avg} kgCO₂")

    # Pie Chart
    transport_pct = transport_km * 0.2
    electricity_pct = electricity_kWh * 0.5
    diet_pct = (diet_encoded * 30) + 10
    waste_pct = waste_kg * 0.3

    labels = ['Transport', 'Electricity', 'Diet Impact', 'Waste']
    sizes = [transport_pct, electricity_pct, diet_pct, waste_pct]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # Suggestions
    st.subheader("Suggestions to Reduce Carbon Footprint")
    if diet_encoded == 1:
        st.write("- Consider reducing meat consumption; plant-based diets produce fewer emissions.")
    if transport_km > 50:
        st.write("- Use public transport, biking or walking when possible.")
    if electricity_kWh > 100:
        st.write("- Use energy-efficient appliances and switch off unused electronics.")
    if waste_kg > 5:
        st.write("- Reduce, reuse, and recycle your household waste.")

st.markdown('</div>', unsafe_allow_html=True)
