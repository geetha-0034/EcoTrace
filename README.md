# EcoTrace


# 🌍 EcoTrace: Predict Your Carbon Footprint

EcoTrace is a user-friendly carbon footprint prediction tool built using machine learning. It empowers individuals to understand the environmental impact of their daily habits and provides actionable suggestions to adopt a more sustainable lifestyle.

---

## 📌 Problem Statement

As climate change continues to accelerate, people are often unaware of how their personal choices contribute to carbon emissions. EcoTrace bridges this gap by calculating a user's carbon footprint based on simple lifestyle inputs and offering recommendations to reduce it.

---

## ⚙️ How It Works

You provide 4 simple inputs:
- 🚗 **Transport**: Distance traveled (in kilometers)
- 🍽 **Diet Type**: Vegetarian or Non-Vegetarian
- ⚡ **Electricity Usage**: Monthly consumption (in kWh)
- 🗑 **Waste Generated**: Monthly waste (in kilograms)

EcoTrace then:
- ✅ Predicts your carbon footprint using a trained **Random Forest** model
- 📊 Visualizes your emission breakdown in a pie chart
- 💡 Provides sustainable living tips

---

## 🚀 Tech Stack

| Tool           | Purpose                        |
|----------------|--------------------------------|
| `Streamlit`    | Web app interface              |
| `scikit-learn` | Machine Learning (RandomForest)|
| `pandas`       | Data processing                |
| `numpy`        | Numerical computations         |
| `matplotlib`   | Pie chart for results          |
| `joblib`       | Model persistence              |

---

## 📸 Screenshots

_Include screenshots of your app UI and pie chart here if available._  
To add them, save your images in the repo and use:

```markdown
![App Screenshot](images/app_screenshot.png)
