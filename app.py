import streamlit as st
import datetime

st.set_page_config(page_title="TCO Calculator", layout="wide")

# Functie om een getal in Europees formaat weer te geven (bijvoorbeeld: € 1.200,50)
def format_euro(value):
    s = f"{value:,.2f}"       # Geeft bijvoorbeeld: "30,000.00"
    s = s.replace(",", "X")   # Tijdelijk: "30X000.00"
    s = s.replace(".", ",")   # "30X000,00"
    s = s.replace("X", ".")   # "30.000,00"
    return "€ " + s

# --- Custom CSS voor de invoerkolom ---
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

st.set_page_config(page_title="TCO Calculator", layout="wide")

# We gebruiken hier één brede kolom voor de invoer (links)
with st.container():
    st.markdown('<div class="left-col">', unsafe_allow_html=True)
    st.header("TCO Calculator – Invoergegevens")
    with st.form(key="tco_form"):
        st.subheader("Voertuig")
        # Merk en Model met vooraf ingevulde waarden
        merk = st.text_input("Merk", value="BMW", help="Voorbeeld: BMW")
        model = st.text_input("Model", value="X5 45e", help="Voorbeeld: X5 45e")
        # Voor de datum gebruiken we een tekstveld met dd/mm/YYYY-formaat.
        default_date = datetime.date.today().strftime("%d/%m/%Y")
        datum_eerste_registratie_str = st.text_input("Datum eerste registratie (DD/MM/YYYY)", value=default_date)
        brandstoftype = st.selectbox("Brandstoftype", options=["Benzine", "Diesel", "Hybride", "Elektrisch"])
        co2 = st.number_input("CO2/km in gram", min_value=0, value=120, step=1)
        if brandstoftype == "Elektrisch":
            verbruik_label = "Verbruik per 100 km in kWh"
        else:
            verbruik_label = "Verbruik per 100 km in liter"
        verbruik = st.number_input(verbruik_label, min_value=0.0, value=6.5, step=0.1, format="%.2f")
        # Prijsvelden met euroteken (let op: de notatie kan iets afwijken van '€ 1.200,50')
        catalogusprijs = st.number_input("Catalogusprijs inclusief opties en btw (€)", 
                                          min_value=0.0, value=30000.0, step=100.0, format="€ %0,.2f")
        aankoopprijs_incl = st.number_input("Aankoopprijs inclusief btw (€)", 
                                            min_value=0.0, value=25000.0, step=100.0, format="€ %0,.2f")
        # Aankoopprijs exclusief btw wordt automatisch berekend (niet aanpasbaar)
        
        st.markdown("---")
        st.subheader("Gebruik")
        jaarlijkse_kilometers = st.number_input("Geschat aantal jaarlijkse kilometers (km)", 
                                                min_value=0, value=20000, step=100, format="%d")
        
        st.markdown("---")
        st.subheader("Fiscaliteit gebruiker")
        btw_aftrekbaarheid = st.number_input("BTW aftrekbaarheid (%)", 
                                             min_value=0.0, max_value=100.0, value=35.0, step=0.1, format="%.2f")
        vennootschapsbelasting = st.number_input("Marginale vennootschapsbelasting (%)", 
                                                 min_value=0.0, max_value=100.0, value=25.0, step=0.1, format="%.2f")
        inkomensbelasting = st.number_input("Marginale inkomensbelasting (%)", 
                                            min_value=0.0, max_value=100.0, value=50.0, step=0.1, format="%.2f")
        
        submit_button = st.form_submit_button(label="Bereken TCO")
    st.markdown('</div>', unsafe_allow_html=True)

# Wanneer op de knop "Bereken TCO" wordt geklikt...
if submit_button:
    # Probeer de datum-string om te zetten naar een date-object.
    try:
        datum_eerste_registratie = datetime.datetime.strptime(datum_eerste_registratie_str, "%d/%m/%Y").date()
    except ValueError:
        datum_eerste_registratie = None
        st.error("Datum eerste registratie is niet in het juiste formaat (DD/MM/YYYY).")
    
    # Bereken de aankoopprijs exclusief btw (automatisch, niet aanpasbaar)
    aankoopprijs_excl = aankoopprijs_incl / 1.21
    
    # Dummy TCO-berekening (pas deze logica aan je eigen formule aan)
    tco_dummy = catalogusprijs + aankoopprijs_excl + (jaarlijkse_kilometers * 0.1)
    
    st.markdown("### Berekeningen")
    st.write(f"**Aankoopprijs exclusief btw:** {format_euro(aankoopprijs_excl)}")
    st.write(f"**Geschatte TCO:** {format_euro(tco_dummy)}")
