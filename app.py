import streamlit as st
import datetime

# Configure the page layout
st.set_page_config(page_title="TCO Calculator", layout="wide")

st.title("Total Cost of Ownership (TCO) Calculator")
st.write("Vul de onderstaande gegevens in om uw TCO te berekenen.")

# Use a form to let the user fill in all the fields before submission
with st.form(key="tco_form"):
    # ------------------------------
    # Algemeen & Voertuiggegevens
    # ------------------------------
    st.subheader("Algemene Voertuiggegevens")
    col1, col2 = st.columns(2)
    with col1:
        merk = st.text_input("Merk", placeholder="Bijv. Toyota")
        model = st.text_input("Model", placeholder="Bijv. Corolla")
        catalogusprijs = st.number_input(
            "Catalogusprijs inclusief opties inclusief btw",
            min_value=0.0, value=30000.0, step=1000.0, format="%.2f"
        )
        aankoopprijs = st.number_input(
            "Aankoopprijs inclusief btw",
            min_value=0.0, value=25000.0, step=1000.0, format="%.2f"
        )
        datum_eerste_registratie = st.date_input(
            "Datum eerste registratie",
            value=datetime.date.today()
        )
    with col2:
        brandstoftype = st.selectbox(
            "Brandstoftype",
            options=["Benzine", "Diesel", "Elektrisch", "Hybride", "Andere"]
        )
        co2 = st.number_input(
            "CO2/km in gram",
            min_value=0, value=120, step=1
        )
        verbruik = st.number_input(
            "KWh of liter per 100 km",
            min_value=0.0, value=6.5, step=0.1, format="%.2f"
        )
        contractduur = st.number_input(
            "Contractduur in maanden",
            min_value=0, value=36, step=1
        )
        restwaarde = st.number_input(
            "Restwaarde (%)",
            min_value=0.0, max_value=100.0, value=40.0, step=0.1, format="%.2f"
        )

    # ------------------------------
    # Financiële Gegevens
    # ------------------------------
    st.subheader("Financiële Gegevens")
    col3, col4, col5 = st.columns(3)
    with col3:
        jaarlijkse_rente = st.number_input(
            "Jaarlijkse rente (%)",
            min_value=0.0, max_value=100.0, value=5.0, step=0.1, format="%.2f"
        )
        biv = st.number_input(
            "BIV",
            min_value=0.0, value=0.0, step=10.0, format="%.2f"
        )
        verkeersbelasting = st.number_input(
            "Verkeersbelasting",
            min_value=0.0, value=0.0, step=10.0, format="%.2f"
        )
    with col4:
        verzekering_ba = st.number_input(
            "Verzekering BA",
            min_value=0.0, value=0.0, step=10.0, format="%.2f"
        )
        verzekering_omnium = st.number_input(
            "Verzekering omnium",
            min_value=0.0, value=0.0, step=10.0, format="%.2f"
        )
    with col5:
        rechtsbijstand = st.number_input(
            "Rechtsbijstand",
            min_value=0.0, value=0.0, step=10.0, format="%.2f"
        )
        nummerplaat_div = st.number_input(
            "Nummerplaat DIV",
            min_value=0.0, value=0.0, step=10.0, format="%.2f"
        )
        fleetsoftware = st.number_input(
            "Fleetsoftware",
            min_value=0.0, value=0.0, step=10.0, format="%.2f"
        )

    # ------------------------------
    # Onderhoud en Gebruiksgegevens
    # ------------------------------
    st.subheader("Onderhoud en Gebruiksgegevens")
    col6, col7 = st.columns(2)
    with col6:
        onderhoud_per_jaar = st.number_input(
            "Onderhoud per jaar",
            min_value=0.0, value=1000.0, step=50.0, format="%.2f"
        )
    with col7:
        geschatte_km_per_jaar = st.number_input(
            "Geschatte kilometers per jaar",
            min_value=0, value=15000, step=100
        )

    # ------------------------------
    # Belastingen
    # ------------------------------
    st.subheader("Belastingen")
    col8, col9, col10 = st.columns(3)
    with col8:
        btw_aftrekbaarheid = st.number_input(
            "BTW aftrekbaarheid (%)",
            min_value=0.0, max_value=100.0, value=21.0, step=0.1, format="%.2f"
        )
    with col9:
        vennootschapsbelasting = st.number_input(
            "Vennootschapsbelasting (%)",
            min_value=0.0, max_value=100.0, value=25.0, step=0.1, format="%.2f"
        )
    with col10:
        marginale_personenbelasting = st.number_input(
            "Marginale personenbelasting (%)",
            min_value=0.0, max_value=100.0, value=40.0, step=0.1, format="%.2f"
        )

    # Submit button for the form
    submit_button = st.form_submit_button(label="Bereken TCO")

# After submission, you can process the data.
if submit_button:
    st.success("De gegevens zijn succesvol ingevuld!")
    # Here you would call your TCO-berekening. For now, we geven een overzicht terug.
    st.subheader("Overzicht Ingevoerde Gegevens")
    st.write({
        "Merk": merk,
        "Model": model,
        "Catalogusprijs inclusief btw": catalogusprijs,
        "Aankoopprijs inclusief btw": aankoopprijs,
        "Datum eerste registratie": datum_eerste_registratie,
        "Brandstoftype": brandstoftype,
        "CO2/km": co2,
        "Verbruik (KWh of liter/100 km)": verbruik,
        "Contractduur (maanden)": contractduur,
        "Restwaarde (%)": restwaarde,
        "Jaarlijkse rente (%)": jaarlijkse_rente,
        "BIV": biv,
        "Verkeersbelasting": verkeersbelasting,
        "Verzekering BA": verzekering_ba,
        "Verzekering omnium": verzekering_omnium,
        "Rechtsbijstand": rechtsbijstand,
        "Nummerplaat DIV": nummerplaat_div,
        "Fleetsoftware": fleetsoftware,
        "Onderhoud per jaar": onderhoud_per_jaar,
        "Geschatte kilometers per jaar": geschatte_km_per_jaar,
        "BTW aftrekbaarheid (%)": btw_aftrekbaarheid,
        "Vennootschapsbelasting (%)": vennootschapsbelasting,
        "Marginale personenbelasting (%)": marginale_personenbelasting
    })

