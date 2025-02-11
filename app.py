import streamlit as st
import datetime

st.set_page_config(page_title="Company Car TCO Calculator", layout="wide")

# Function to format a number in European format (e.g., € 1.200,50)
def format_euro(value):
    s = f"{value:,.2f}"       # Gives, for example: "30,000.00"
    s = s.replace(",", "X")   # Temporarily: "30X000.00"
    s = s.replace(".", ",")   # "30X000,00"
    s = s.replace("X", ".")   # "30.000,00"
    return "€ " + s

# --- Custom CSS for the input column ---
st.markdown(
    """
    <style>
    .left-col {
        background-color: #003366;
        color: white;
        padding: 20px;
        border-radius: 10px;
        width: 100%;
    }
    .stNumberInput input {
        text-align: right;
    }
    .stButton>button {
        background-color: #0066cc;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Use a wide column for input (left)
with st.container():
    st.markdown('<div class="left-col">', unsafe_allow_html=True)
    st.header("Company Car TCO Calculator")
    with st.form(key="tco_form"):
        st.subheader("Voertuig")
        # Brand and Model with pre-filled values
        brand = st.text_input("Merk", value="BMW", help="Example: BMW")
        model = st.text_input("Model", value="X5 45e", help="Example: X5 45e")
        # For the date, we use a text field with dd/mm/YYYY format.
        default_date = datetime.date.today().strftime("%d/%m/%Y")
        registration_date_str = st.text_input("Datum eerste registratie (DD/MM/YYYY)", value=default_date)
        fuel_type = st.selectbox("Type brandstof", options=["Benzine", "Diesel", "Hybride", "Elektrisch"])
        co2 = st.number_input("CO2/km in gram", min_value=0, value=120, step=1)
        if fuel_type == "Elektrisch":
            consumption_label = "Verbruik per 100 km in kWh"
        else:
            consumption_label = "Verbruik per 100 km in liter"
        consumption = st.number_input(consumption_label, min_value=0.0, value=6.5, step=0.1, format="%.2f")

