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
    .stNumberInput input, .stTextInput input, .stDateInput input {
        text-align: left;
        color: grey;
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
        # Brand and Model with placeholder values
        brand = st.text_input("Merk", placeholder="Example: BMW", help="Example: BMW")
        model = st.text_input("Model", placeholder="Example: X5 45e", help="Example: X5 45e")
        # Use a date input for the registration date
        default_date = datetime.date.today()
        registration_date = st.date_input("Datum eerste registratie", value=default_date, help="Selecteer de datum")
        fuel_type = st.selectbox("Type brandstof", options=["Benzine", "Diesel", "Hybride", "Elektrisch"])
        co2 = st.number_input("CO2/km in gram", min_value=0, value=120, step=1)
        if fuel_type == "Elektrisch":
            consumption_label = "Verbruik per 100 km in kWh"
        else:
            consumption_label = "Verbruik per 100 km in liter"
        consumption = st.number_input(consumption_label, min_value=0.0, value=6.5, step=0.1, format="%.2f")

        st.markdown("---")
        st.subheader("Gebruik")
        annual_kilometers = st.number_input("Geschat aantal jaarlijkse kilometers (km)", 
                                            min_value=0, value=15000, step=100, format="%d")
        
        st.markdown("---")
        st.subheader("Fiscaliteit gebruiker")
        vat_deductibility = st.number_input("BTW aftrekbaarheid (%)", 
                                            min_value=0.0, max_value=100.0, value=35.0, step=0.1, format="%.2f")
        corporate_tax = st.number_input("Marginale vennootschapsbelasting (%)", 
                                        min_value=0.0, max_value=100.0, value=25.0, step=0.1, format="%.2f")
        income_tax = st.number_input("Marginale inkomensbelasting (%)", 
                                     min_value=0.0, max_value=100.0, value=50.0, step=0.1, format="%.2f")
        
        submit_button = st.form_submit_button(label="Calculate TCO")
    st.markdown('</div>', unsafe_allow_html=True)

# When the "Calculate TCO" button is clicked...
if submit_button:
    # Calculate the purchase price excl. VAT (automatically, not editable)
    purchase_price_excl = purchase_price_incl / 1.21
    
    # Dummy TCO calculation (adjust this logic to your own formula)
    tco_dummy = catalog_price + purchase_price_excl + (annual_kilometers * 0.1)
    
    st.markdown("### Calculations")
    st.write(f"**Purchase Price excl. VAT:** {format_euro(purchase_price_excl)}")
    st.write(f"**Estimated TCO:** {format_euro(tco_dummy)}")
