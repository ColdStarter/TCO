import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import time  # Voor de loading-effect

# --- Laad de Google Sheets credentials uit st.secrets ---
# Je secrets zijn al correct geconfigureerd via triple quotes
gcp_credentials = st.secrets["gcp_credentials"]

# Definieer de benodigde scopes
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Maak de credentials met google-auth (deze functie verwacht een dict)
credentials = Credentials.from_service_account_info(gcp_credentials, scopes=scopes)

# Verbind met Google Sheets via gspread
client = gspread.authorize(credentials)

# Open de Google Sheet (vervang de URL indien nodig)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1oczFh_1CRNZE2zdpyUyLSJvOU0AYAjlQBLd8VFpkX_w/edit"
try:
    sheet = client.open_by_url(SHEET_URL).worksheet("Sheet1")
except Exception as e:
    st.error("Error opening worksheet 'Sheet1': " + str(e))
    st.stop()

# --- Functie om automodellen uit kolom A op te halen (sla de header over) ---
def fetch_car_models():
    try:
        models = sheet.col_values(1)[1:]  # Sla de header over
        return models if models else ["Geen modellen beschikbaar"]
    except Exception as e:
        st.error("Error fetching car models: " + str(e))
        return ["Error"]

# --- Pagina Configuratie ---
st.set_page_config(page_title="TCO Calculator", layout="centered")

# --- Custom CSS voor styling ---
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

# --- Sidebar (Donkerblauw) ---
with st.sidebar:
    st.markdown("## 🚗 Voertuiggegevens", unsafe_allow_html=True)
    
    # Haal modellen op uit Google Sheets en toon ze in een selectbox
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

# --- TCO Berekening en Weergave ---
st.markdown("## 📊 TCO Berekening", unsafe_allow_html=True)

if bereken:
    with st.spinner("Bezig met berekenen..."):
        time.sleep(1)  # Simuleer verwerkingstijd

    # TCO Berekening: prijs gedeeld door lease_maanden
    tco = prijs / lease_maanden if lease_maanden > 0 else 0

    # Resultaat weergeven in een stijlvolle container
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Maandelijkse Total Cost of Ownership</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">€ {tco:,.2f}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
