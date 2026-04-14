import streamlit as st

st.set_page_config(page_title="iSFP Pro Tool", layout="wide")

st.title("🏠 iSFP Beratungs-Tool (Pro)")

# -------------------------
# Eingaben
# -------------------------
st.header("Gebäudedaten")

col1, col2 = st.columns(2)

with col1:
    baujahr = st.number_input("Baujahr", 1900, 2025, 1990)
    wohnflaeche = st.number_input("Wohnfläche (m²)", 50, 500, 120)

with col2:
    heizung = st.selectbox("Heizung", ["Gas", "Öl", "Wärmepumpe"])
    einkommensbonus = st.checkbox("Einkommensbonus berücksichtigen")

# -------------------------
# Maßnahmen
# -------------------------
st.header("Sanierungsmaßnahmen")

maßnahmen = st.multiselect(
    "Maßnahmen auswählen",
    ["Außenwand", "Dach", "Fenster", "Wärmepumpe"]
)

kosten_gesamt = 0
foerder_gesamt = 0
einsparung_gesamt = 0

# -------------------------
# Berechnung
# -------------------------
for m in maßnahmen:
    st.subheader(m)
    
    kosten = st.number_input(f"Kosten {m} (€)", 0, 100000, 20000, key=m)
    
    # Förderlogik
    if m == "Wärmepumpe":
        foerder = 0.30 + 0.20  # Basis + Klimabonus
        if einkommensbonus:
            foerder += 0.30
    else:
        foerder = 0.15 + 0.05  # Einzelmaßnahme + iSFP
    
    foerder = min(foerder, 0.70)  # Deckel
    
    zuschuss = kosten * foerder
    eigenanteil = kosten - zuschuss
    
    # Einsparung (vereinfacht)
    einsparung = kosten * 0.05
    
    # CO2 (grob)
    co2 = einsparung * 0.2
    
    # Summen
    kosten_gesamt += kosten
    foerder_gesamt += zuschuss
    einsparung_gesamt += einsparung
    
    # Anzeige
    st.write(f"Fördersatz: {int(foerder*100)} %")
    st.write(f"Zuschuss: {int(zuschuss)} €")
    st.write(f"Eigenanteil: {int(eigenanteil)} €")
    st.write(f"Einsparung/Jahr: {int(einsparung)} €")

# -------------------------
# Ergebnis
# -------------------------
st.header("📊 Gesamtbewertung")

st.write(f"💰 Investition: {int(kosten_gesamt)} €")
st.write(f"💸 Förderung: {int(foerder_gesamt)} €")
st.write(f"🏦 Eigenanteil: {int(kosten_gesamt - foerder_gesamt)} €")

st.write(f"📉 Einsparung/Jahr: {int(einsparung_gesamt)} €")

if einsparung_gesamt > 0:
    amortisation = (kosten_gesamt - foerder_gesamt) / einsparung_gesamt
    st.write(f"⏱️ Amortisation: {round(amortisation,1)} Jahre")

st.write(f"🌱 CO₂-Ersparnis: {int(einsparung_gesamt * 0.2)} kg/Jahr")

# -------------------------
# Empfehlung
# -------------------------
st.header("📌 Empfehlung")

if "Wärmepumpe" in maßnahmen:
    st.success("Sehr gute Förderung – Heizungstausch priorisieren!")
elif len(maßnahmen) > 2:
    st.success("Ganzheitliche Sanierung sinnvoll")
else:
    st.info("Einzelmaßnahmen möglich – Einsparung begrenzt")
