import streamlit as st
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load trained model
model = joblib.load("model.pkl")

st.set_page_config(page_title="EcoTrace - Carbon Footprint Dashboard", layout="wide")

# STYLING 

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
        .custom-title {
           font-size: 28px;
           color: white !important;
           font-weight: 700;
           margin-top: 2rem;
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
            .custom-suggestion {
        background-color: rgba(0, 0, 0, 0.4);
        color: white !important;
        padding: 10px;
        border-radius: 6px;
        margin-bottom: 8px;
    }
    ::selection {
        background: #2563eb; /* Keep the blue highlight */
        color: white; /* Force text to white */
    }
    </style>
""", unsafe_allow_html=True)

#TITLE

col_title, col_info = st.columns([2, 2])

with col_title:
    st.markdown('<div class="main-title">EcoTrace: Carbon Footprint Estimator</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Predict your carbon impact and receive actionable sustainability suggestions</div>', unsafe_allow_html=True)

with col_info:
    st.markdown("""
        <div style="background-color: rgba(255,255,255,0.85); padding: 20px; border-radius: 10px; margin-top: 20px;">
            <h2 style="color:#1f2937;"> What is a Carbon Footprint?</h2>
            <h4 style="color:#111827; font-size: 16px;">
                A <strong>carbon footprint</strong> is the total greenhouse gas emissions caused directly and indirectly by your activities —
                including transport, electricity usage, diet, and waste.</h4>
                <h3>Lowering your footprint helps combat climate change and builds a greener planet.
            </h3>
        </div>
    """, unsafe_allow_html=True)

# USER INPUT FORM 
st.markdown('<div class="glass-box">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    transport_km = st.number_input("Transport (km)", min_value=0.0, value=100.0)
    electricity_kWh = st.number_input("Electricity Usage (kWh)", min_value=0.0, value=50.0)
with col2:
    diet_type = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian"])
    waste_kg = st.number_input("Waste Generated (kg)", min_value=0.0, value=5.0)

diet_encoded = 0 if diet_type == "Vegetarian" else 1

#  CALCULATE FOOTPRINT 
if st.button("Calculate Footprint"):
    input_df = pd.DataFrame([[transport_km, electricity_kWh, diet_encoded, waste_kg]],
                             columns=["Transport_km", "Electricity_kWh", "Diet_Type", "Waste_kg"])
    log_prediction = model.predict(input_df)[0]
    final_prediction = np.expm1(log_prediction)

    st.markdown('<h2 class="custom-title">Results</h2>', unsafe_allow_html=True)
    colA, colB = st.columns(2)
    with colA:
        st.markdown(f'<div class="metric-box"><h3>{final_prediction:.2f} kgCO₂</h3><p>Your Carbon Footprint</p></div>', unsafe_allow_html=True)
    with colB:
        st.markdown(f'<div class="metric-box"><h3>80 kgCO₂</h3><p>Sustainable Average</p></div>', unsafe_allow_html=True)

    # ----- PIE CHART -----
    st.markdown('<h2 class="custom-title">Footprint Breakdown</h2>', unsafe_allow_html=True)
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
    centre_circle = plt.Circle((0, 0), 0.70, fc='black', alpha=0.6)
    fig.gca().add_artist(centre_circle)
    plt.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0.5), title="Categories")
    st.pyplot(fig)

    # SUSTAINABILITY SUGGESTIONS 
    st.markdown('<h2 class="custom-title">Sustainable Suggestions</h2>', unsafe_allow_html=True)
    suggestions = []

    sustainable_targets = {
        "Transport_km": 30,        # e.g., <30 km/week
        "Electricity_kWh": 20,     # e.g., <20 kWh/week
        "Waste_kg": 2              # e.g., <2 kg/week
    }

    # Transport
    if transport_km > sustainable_targets["Transport_km"] * 2:
        suggestions.append("Your transport footprint is high. Try reducing private car usage and consider biking or public transport.")
    elif transport_km > sustainable_targets["Transport_km"]:
        suggestions.append("Moderate transport emissions detected. Carpooling or occasional biking can help reduce this further.")

    # Electricity
    if electricity_kWh > sustainable_targets["Electricity_kWh"] * 2:
        suggestions.append("High electricity usage. Consider energy-saving appliances and turning off devices when not needed.")
    elif electricity_kWh > sustainable_targets["Electricity_kWh"]:
        suggestions.append("You're using a fair amount of electricity. Use LED lights and monitor high-power devices.")

    # Diet
    if diet_encoded == 1:
        suggestions.append("A non-vegetarian diet typically has a higher carbon footprint. Consider adding more plant-based meals.")

    # Waste
    if waste_kg > sustainable_targets["Waste_kg"] * 2:
        suggestions.append("High waste levels. Recycle, compost, and reduce single-use plastics.")
    elif waste_kg > sustainable_targets["Waste_kg"]:
        suggestions.append("Moderate waste detected. Try composting and reducing packaged products.")
        
    if final_prediction > 100:
        suggestions.append("Your total carbon footprint is above the sustainable average. Try making changes across multiple areas.")
    elif final_prediction < 50:
        suggestions.append("Excellent! Your overall footprint is low. Keep up the eco-friendly habits!")
    if suggestions:
        suggestion_html = """
        <div style="background-color: rgba(0,0,0,0.4); padding: 20px; border-radius: 10px;">
            <ul style="color: white; font-size: 20px;">
        """
        for tip in suggestions:
            suggestion_html += f"<li>{tip}</li>"
        suggestion_html += "</ul></div>"

        st.markdown(suggestion_html, unsafe_allow_html=True)
    else:
        st.success("Your footprint is already quite low. Keep it up!")

# FOOTER
st.markdown("<hr>", unsafe_allow_html=True)
