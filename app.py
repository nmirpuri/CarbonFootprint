import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Carbon Footprint Calculator", layout="centered")

st.title("🌍 Carbon Footprint Calculator")
st.write("Answer a few questions about your lifestyle to estimate your annual carbon emissions.")

# --------------------- Quiz Questions ---------------------
st.header("🚗 Transportation")
car_miles = st.number_input("How many miles do you drive per year?", min_value=0, value=10000)
air_flights = st.number_input("How many round-trip flights do you take per year (domestic)?", min_value=0, value=2)

st.header("🍽 Diet")
diet_type = st.selectbox("What best describes your diet?", ["Meat-heavy", "Average (mixed) diet", "Vegetarian", "Vegan"])

st.header("🏠 Home Energy")
household_size = st.number_input("How many people live in your household?", min_value=1, value=1)
electricity_kwh = st.number_input("How much electricity do you use per year (in kWh)?", min_value=0, value=8000)

st.header("🛍 Consumption & Waste")
shop_frequency = st.selectbox("How often do you buy new clothes?", ["Every week", "Every month", "Every few months", "Rarely"])
recycling = st.selectbox("Do you regularly recycle paper, plastics, and metals?", ["Always", "Sometimes", "Rarely", "Never"])

# --------------------- Emission Factors ---------------------
def calculate_emissions():
    car_emissions = car_miles * 0.404  # kg CO2 per mile
    flight_emissions = air_flights * 900  # kg CO2 per round-trip

    diet_emissions = {
        "Meat-heavy": 2500,
        "Average (mixed) diet": 2000,
        "Vegetarian": 1700,
        "Vegan": 1500
    }[diet_type]

    electric_emissions = electricity_kwh * 0.417 / household_size  # kg CO2 per kWh (US avg)

    shop_emissions = {
        "Every week": 600,
        "Every month": 400,
        "Every few months": 200,
        "Rarely": 100
    }[shop_frequency]

    recycling_savings = {
        "Always": -200,
        "Sometimes": -100,
        "Rarely": -50,
        "Never": 0
    }[recycling]

    total = car_emissions + flight_emissions + diet_emissions + electric_emissions + shop_emissions + recycling_savings
    return round(total, 2)

if st.button("Calculate My Carbon Footprint"):
    total_emissions = calculate_emissions()
    st.success(f"Your estimated annual carbon footprint is **{total_emissions} kg CO₂**.")

    # --------------------- Benchmark Chart ---------------------
    st.subheader("📊 How Do You Compare?")
    benchmarks = pd.DataFrame({
        'Category': ['You', 'US Average', 'Global Average', 'Low Impact Goal'],
        'CO2 (kg)': [total_emissions, 16000, 4500, 2000]
    })

    fig, ax = plt.subplots()
    bars = ax.bar(benchmarks['Category'], benchmarks['CO2 (kg)'], color=['green', 'red', 'blue', 'gray'])
    ax.set_ylabel("Annual CO₂ Emissions (kg)")
    ax.set_title("Carbon Footprint Comparison")
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:,.0f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points", ha='center', va='bottom')
    st.pyplot(fig)

    # --------------------- Suggestions ---------------------
    st.subheader("💡 Tips to Reduce Your Emissions")
    st.markdown("- Consider reducing car travel or switching to public transport.")
    st.markdown("- Fly less or offset your flights through verified programs.")
    st.markdown("- Shift toward more plant-based meals.")
    st.markdown("- Improve home efficiency (LEDs, insulation, smart thermostats).")
    st.markdown("- Recycle consistently and buy fewer fast fashion items.")
