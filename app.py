import streamlit as st
import time  # For loading effect

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

    model = st.text_input("Model", value="X5 45e", help="Voer het model in (bijv. X5 45e)")
    
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

    # TCO Calculation
    tco = prijs / lease_maanden if lease_maanden > 0 else 0

    # Display result
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">Maandelijkse Total Cost of Ownership</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">€ {tco:,.2f}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
