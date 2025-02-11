import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time  # For loading effect

# --- Connect to Google Sheets ---
def connect_to_gsheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("gcp_credentials.json", scope)
    client = gspread.authorize(creds)
    return client

# Open the sheet (replace YOUR_SHEET_ID with your actual sheet ID)
SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
client = connect_to_gsheets()
sheet = client.open_by_url(SHEET_URL).sheet1  # Open first sheet

# Function to fetch car models from Column A (skip the header)
def fetch_car_models():
    models = sheet.col_values(1)[1:]
    return models

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

    # TCO Calculation: prijs divided by lease_maanden
    tco = prijs / lease_maanden if lease_maanden > 0 else 0

    # Display result in a stylish container
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">Maandelijkse Total Cost of Ownership</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">€ {tco:,.2f}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
