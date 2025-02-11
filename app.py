import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time  # For loading effect

# --- Load Google Sheets credentials securely from Streamlit Secrets ---
try:
    # st.secrets["gcp_credentials"] should be a dictionary if configured correctly.
    gcp_credentials = dict(st.secrets["gcp_credentials"])
except Exception as e:
    st.error("Error loading gcp_credentials from secrets: " + str(e))
    st.stop()

# Ensure the private key has actual newlines
if "private_key" in gcp_credentials:
    gcp_credentials["private_key"] = gcp_credentials["private_key"].strip().replace('\\n', '\n')
else:
    st.error("private_key not found in gcp_credentials. Please check your secrets.")
    st.stop()

# Verify that all required keys are present
required_keys = [
    "type", "project_id", "private_key_id", "private_key", "client_email",
    "client_id", "auth_uri", "token_uri", "auth_provider_x509_cert_url", "client_x509_cert_url"
]
missing_keys = [key for key in required_keys if key not in gcp_credentials]
if missing_keys:
    st.error("Missing keys in gcp_credentials: " + ", ".join(missing_keys))
    st.stop()

# --- Connect to Google Sheets ---
def connect_to_gsheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_dict(gcp_credentials, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error("Error connecting to Google Sheets: " + str(e))
        st.stop()

# Open the Google Sheet using your provided URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1oczFh_1CRNZE2zdpyUyLSJvOU0AYAjlQBLd8VFpkX_w/edit"
client = connect_to_gsheets()
try:
    # Explicitly open the worksheet named "Sheet1"
    sheet = client.open_by_url(SHEET_URL).worksheet("Sheet1")
except Exception as e:
    st.error("Error opening worksheet 'Sheet1': " + str(e))
    st.stop()

# --- Function to fetch car models from Column A (skip the header) ---
def fetch_car_models():
    try:
        models = sheet.col_values(1)[1:]  # Skip header row
        return models if models else ["Geen modellen beschikbaar"]
    except Exception as e:
        st.error("Error fetching car models: " + str(e))
        return ["Error"]

# --- Set up page configuration ---
st.set_page_config(page_title="TCO Calculator", layout="centered")

# --- Custom CSS for styling ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f5f5;
    }
    .sidebar .sidebar-content {
        background-color: #003366;
        color: white;
    }
    .stNumberInput input {
        text-align: right;
    }
    .stButton>button {
        background-color: #0066cc;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .metric-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #003366;
    }
    .metric-label {
        font-size: 16px;
        color: gray;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# --- Sidebar (Dark Blue) ---
with st.sidebar:
    st.markdown("## 🚗 Voertuiggegevens", unsafe_allow_html=True)
    
    # Fetch models from Google Sheets and use a selectbox for the model input
    car_models = fetch_car_models()
    model = st.selectbox("Model", options=car_models, index=0, help="Selecteer het model (bijv. X5 45e)")
    
    prijs = st.number_input(
        "Prijs (€)", 
        min_value=0.0, 
        value=50000.0, 
        step=1000.0, 
        format="%.2f"
    )

    lease_maanden = st.number_input(
        "Aantal maanden leasing", 
        min_value=1, 
        value=36, 
        step=1
    )

    bereken = st.button("Bereken TCO")

# --- TCO Calculation and Display ---
st.markdown("## 📊 TCO Berekening", unsafe_allow_html=True)

if bereken:
    with st.spinner("Bezig met berekenen..."):
        time.sleep(1)  # Simulate processing time

    # TCO Calculation: price divided by lease months
    tco = prijs / lease_maanden if lease_maanden > 0 else 0

    # Display result in a stylish container
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Maandelijkse Total Cost of Ownership</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">€ {tco:,.2f}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
