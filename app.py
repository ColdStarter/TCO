import streamlit as st
import pandas as pd

st.set_page_config(page_title="TCO Calculator", layout="wide")

st.title("TCO Calculator")
st.write("Enter your costs below to see the total cost of ownership.")

col1, col2 = st.columns(2)

with col1:
    hardware_cost = st.number_input("Hardware Cost", min_value=0.0, value=5000.0, help="One-time purchase cost")
    down_payment = st.number_input("Down Payment (if any)", min_value=0.0, value=0.0)
    other_one_time = st.number_input("Other One-time Costs", min_value=0.0, value=1000.0)

with col2:
    licensing_cost = st.number_input("Licensing (per year)", min_value=0.0, value=200.0)
    maintenance_cost = st.number_input("Maintenance (per year)", min_value=0.0, value=300.0)
    other_annual = st.number_input("Other Annual Costs", min_value=0.0, value=100.0)

years = st.slider("Number of years to consider", min_value=1, max_value=10, value=3)

# Simple TCO Calculation:
# TCO = (One-time costs) + (Annual costs * years)
one_time_total = hardware_cost + down_payment + other_one_time
annual_total = licensing_cost + maintenance_cost + other_annual
tco = one_time_total + (annual_total * years)

st.subheader("Results")

# Headline metric
st.metric("Total Cost of Ownership", f"${tco:,.2f}")

# Breakdown
breakdown = {
    "Cost Type": ["One-Time", "Recurring (Over Time)"],
    "Amount": [one_time_total, annual_total * years]
}
df_breakdown = pd.DataFrame(breakdown)
st.table(df_breakdown)

# Optionally, a bar chart
chart_data = pd.DataFrame({
    "Amount": [one_time_total, annual_total * years]
}, index=["One-Time", "Recurring"])
st.bar_chart(chart_data)
