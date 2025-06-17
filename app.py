import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load your trained model (replace with actual model path)
model = joblib.load("model.pkl")

st.set_page_config(page_title="Carbon Footprint Calculator", layout="centered")

# Custom CSS styling to match your exact reference
st.markdown("""
<style>
body, .main {
    background-image: url('https://images.unsplash.com/photo-1552089123-2a5387e8e6df');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

h1 {
    font-size: 2.8rem;
    color: white;
    font-weight: bold;
    padding-top: 2rem;
    text-align: center;
}

.box {
    background-color: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 2rem;
    width: 100%;
    max-width: 500px;
    margin: 2rem auto;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

button[kind="primary"] {
    background-color: #f77f00;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1rem;
}

.stTextInput > div > input, .stNumberInput input, .stSelectbox > div {
    background-color: #f1f1f1;
    border-radius: 8px;
    padding: 0.5rem;
    border: 1px solid #ccc;
}

ul {
    margin-left: 1.5rem;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>What's the <span style='color:#f77f00;'>carbon footprint</span> of your lifestyle?</h1>", unsafe_allow_html=True)

# Glass-styled container
tab = st.container()
with tab:
    st.markdown('<div class="box">', unsafe_allow_html=True)

    transport = st.number_input("Transport (km traveled)", min_value=0.0, format="%.2f")
    electricity = st.number_input("Electricity usage (kWh)", min_value=0.0, format="%.2f")
    diet = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian"])
    waste = st.number_input("Waste generated (kg)", min_value=0.0, format="%.2f")

    if st.button("Calculate my emissions"):
        encoded_diet = 0 if diet == "Vegetarian" else 1
        input_df = pd.DataFrame([[transport, electricity, encoded_diet, waste]],
                                 columns=["Transport_km", "Electricity_kWh", "Diet_Type", "Waste_kg"])
        log_prediction = model.predict(input_df)[0]
        result = round(np.expm1(log_prediction), 2)

        st.success(f"Your estimated carbon footprint is {result} kgCO₂")

        # Show suggestions based on input
        tips = []
        if transport > 100:
            tips.append("Consider using public transport or carpooling more often.")
        if electricity > 200:
            tips.append("Switch to energy-efficient appliances or reduce electricity use.")
        if diet == "Non-Vegetarian":
            tips.append("Incorporate plant-based meals to reduce dietary impact.")
        if waste > 10:
            tips.append("Reduce, reuse, and recycle to manage waste more effectively.")

        if tips:
            st.markdown("""<div class='box'><strong>Suggestions:</strong><ul>""", unsafe_allow_html=True)
            for tip in tips:
                st.markdown(f"<li>{tip}</li>", unsafe_allow_html=True)
            st.markdown("</ul></div>", unsafe_allow_html=True)
        else:
            st.info("Your lifestyle already aligns well with sustainability goals! 🌱")

    st.markdown('</div>', unsafe_allow_html=True)
