import streamlit as st
import datetime

# --- Custom CSS voor achtergrondkleuren ---
st.markdown(
    """
    <style>
    .left-col {
        background-color: #003366;
        color: white;
        padding: 20px;
        border-radius: 10px;
    }
    .center-col, .right-col {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
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

# --- Indeling: 3 kolommen ---
left_col, center_col, right_col = st.columns(3)

# --- Linker Kolom: Invoerformulier met donkerblauwe achtergrond ---
with left_col:
    st.markdown('<div class="left-col">', unsafe_allow_html=True)
    st.header("Voer uw gegevens in")
    with st.form(key="tco_form"):
        # Sectie: Voertuig
        st.subheader("Voertuig")
        merk = st.text_input("Merk (bijv. BMW)", value="", help="Voer hier het merk in, bijvoorbeeld 'BMW'")
        model = st.text_input("Model (bijv. X5 45e)", value="", help="Voer hier het model in, bijvoorbeeld 'X5 45e'")
        datum_eerste_registratie = st.date_input("Datum eerste registratie (DD/MM/YYYY)", value=datetime.date.today())
        brandstoftype = st.selectbox("Brandstoftype", options=["Benzine", "Diesel", "Hybride", "Elektrisch"])
        co2 = st.number_input("CO2/km in gram", min_value=0, value=120, step=1)
        # Dynamische label voor verbruik afhankelijk van brandstoftype
        if brandstoftype == "Elektrisch":
            verbruik_label = "Verbruik per 100 km (kWh)"
        else:
            verbruik_label = "Verbruik per 100 km (liter)"
        verbruik = st.number_input(verbruik_label, min_value=0.0, value=6.5, step=0.1, format="%.2f")
        catalogusprijs = st.number_input("Catalogusprijs inclusief opties en btw (€)", min_value=0.0, value=30000.0, step=100.0, format="%.2f")
        aankoopprijs_incl = st.number_input("Aankoopprijs inclusief btw (€)", min_value=0.0, value=25000.0, step=100.0, format="%.2f")
        # Aankoopprijs exclusief btw wordt automatisch berekend (niet aanpasbaar)
        
        st.markdown("---")
        # Sectie: Gebruik
        st.subheader("Gebruik")
        jaarlijkse_kilometers = st.number_input("Geschat aantal jaarlijkse kilometers (km)", min_value=0, value=15000, step=100)
        
        st.markdown("---")
        # Sectie: Fiscaliteit gebruiker
        st.subheader("Fiscaliteit gebruiker")
        btw_aftrekbaarheid = st.number_input("BTW aftrekbaarheid (%)", min_value=0.0, max_value=100.0, value=35.0, step=0.1, format="%.2f")
        vennootschapsbelasting = st.number_input("Marginale vennootschapsbelasting (%)", min_value=0.0, max_value=100.0, value=25.0, step=0.1, format="%.2f")
        inkomensbelasting = st.number_input("Marginale inkomensbelasting (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1, format="%.2f")
        
        submit_button = st.form_submit_button(label="Bereken TCO")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Wanneer de gebruiker op "Bereken TCO" klikt, worden in het centrum en rechts de resultaten getoond ---
if submit_button:
    # Automatische berekening: aankoopprijs exclusief btw (aankoopprijs inclusief btw gedeeld door 1,21)
    aankoopprijs_excl = aankoopprijs_incl / 1.21

    # Dummy TCO-berekening voor demonstratie (pas deze logica aan voor jouw werkelijke TCO-berekening)
    # Bijvoorbeeld: som van catalogusprijs, aankoopprijs exclusief btw en een fictieve kostenfactor op basis van jaarlijkse km.
    tco_dummy = catalogusprijs + aankoopprijs_excl + (jaarlijkse_kilometers * 0.1)
    
    # --- Centraal: Berekeningen met lichte achtergrond ---
    with center_col:
        st.markdown('<div class="center-col">', unsafe_allow_html=True)
        st.header("Berekeningen")
        st.write(f"**Aankoopprijs exclusief btw:** €{aankoopprijs_excl:,.2f}")
        st.write(f"**Geschatte TCO:** €{tco_dummy:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # --- Rechts: Overzicht van de ingevoerde gegevens ---
    with right_col:
        st.markdown('<div class="right-col">', unsafe_allow_html=True)
        st.header("Overzicht Voertuiggegevens")
        st.write(f"**Merk:** {merk}")
        st.write(f"**Model:** {model}")
        st.write(f"**Datum eerste registratie:** {datum_eerste_registratie.strftime('%d/%m/%Y')}")
        st.write(f"**Brandstoftype:** {brandstoftype}")
        st.write(f"**CO2/km:** {co2} g")
        st.write(f"**Verbruik:** {verbruik} {'kWh' if brandstoftype == 'Elektrisch' else 'liter'} per 100 km")
        st.write(f"**Catalogusprijs:** €{catalogusprijs:,.2f}")
        st.write(f"**Aankoopprijs incl. btw:** €{aankoopprijs_incl:,.2f}")
        st.write(f"**Aankoopprijs excl. btw:** €{aankoopprijs_excl:,.2f}")
        st.markdown("---")
        st.header("Gebruik & Fiscaliteit")
        st.write(f"**Geschatte jaarlijkse kilometers:** {jaarlijkse_kilometers} km")
        st.write(f"**BTW aftrekbaarheid:** {btw_aftrekbaarheid}%")
        st.write(f"**Marginale vennootschapsbelasting:** {vennootschapsbelasting}%")
        st.write(f"**Marginale inkomensbelasting:** {inkomensbelasting}%")
        st.markdown('</div>', unsafe_allow_html=True)
