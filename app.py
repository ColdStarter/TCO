import streamlit as st
import datetime

st.set_page_config(page_title="TCO Calculator", layout="wide")

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
    st.header("TCO Calculator – Input Data")
    with st.form(key="tco_form"):
        st.subheader("Vehicle")
        # Brand and Model with pre-filled values
        brand = st.text_input("Brand", value="BMW", help="Example: BMW")
        model = st.text_input("Model", value="X5 45e", help="Example: X5 45e")
        # For the date, we use a text field with dd/mm/YYYY format.
        default_date = datetime.date.today().strftime("%d/%m/%Y")
        registration_date_str = st.text_input("Registration Date (DD/MM/YYYY)", value=default_date)
        fuel_type = st.selectbox("Fuel Type", options=["Petrol", "Diesel", "Hybrid", "Electric"])
        co2 = st.number_input("CO2/km in grams", min_value=0, value=120, step=1)
        if fuel_type == "Electric":
            consumption_label = "Consumption per 100 km (kWh)"
        else:
            consumption_label = "Consumption per 100 km (liters)"
        consumption = st.number_input(consumption_label, min_value=0.0, value=6.5, step=0.1, format="%.2f")
        # Price fields with euro sign
        catalog_price = st.number_input("Catalog Price incl. options and VAT (€)", 
                                        min_value=0.0, value=30000.0, step=100.0, format="€ %0,.2f")
        purchase_price_incl = st.number_input("Purchase Price incl. VAT (€)", 
                                              min_value=0.0, value=25000.0, step=100.0, format="€ %0,.2f")
        # Purchase price excl. VAT is automatically calculated (not editable)
        
        st.markdown("---")
        st.subheader("Usage")
        annual_kilometers = st.number_input("Estimated annual kilometers (km)", 
                                            min_value=0, value=15000, step=100, format="%d")
        
        st.markdown("---")
        st.subheader("User Taxation")
        vat_deductibility = st.number_input("VAT Deductibility (%)", 
                                            min_value=0.0, max_value=100.0, value=35.0, step=0.1, format="%.2f")
        corporate_tax = st.number_input("Marginal Corporate Tax (%)", 
                                        min_value=0.0, max_value=100.0, value=25.0, step=0.1, format="%.2f")
        income_tax = st.number_input("Marginal Income Tax (%)", 
                                     min_value=0.0, max_value=100.0, value=50.0, step=0.1, format="%.2f")
        
        submit_button = st.form_submit_button(label="Calculate TCO")
    st.markdown('</div>', unsafe_allow_html=True)

# When the "Calculate TCO" button is clicked...
if submit_button:
    # Try to convert the date string to a date object.
    try:
        registration_date = datetime.datetime.strptime(registration_date_str, "%d/%m/%Y").date()
    except ValueError:
        registration_date = None
        st.error("Registration date is not in the correct format (DD/MM/YYYY).")
    
    # Calculate the purchase price excl. VAT (automatically, not editable)
    purchase_price_excl = purchase_price_incl / 1.21
    
    # Dummy TCO calculation (adjust this logic to your own formula)
    tco_dummy = catalog_price + purchase_price_excl + (annual_kilometers * 0.1)
    
    st.markdown("### Calculations")
    st.write(f"**Purchase Price excl. VAT:** {format_euro(purchase_price_excl)}")
    st.write(f"**Estimated TCO:** {format_euro(tco_dummy)}")
