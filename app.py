import streamlit as st

st.title("iSFP Schnell-Check")

# Eingaben
baujahr = st.number_input("Baujahr", 1900, 2025, 1990)
wohnflaeche = st.number_input("Wohnfläche (m²)", 50, 500, 120)

heizung = st.selectbox("Heizung", ["Gas", "Öl", "Wärmepumpe"])

maßnahme = st.selectbox("Maßnahme", [
    "Außenwand",
    "Dach",
    "Fenster",
    "Wärmepumpe"
])

kosten = st.number_input("Investitionskosten (€)", 0, 100000, 20000)

# Förderlogik
foerder = 0

if maßnahme == "Wärmepumpe":
    foerder = 0.30 + 0.20  # Basis + Klimabonus
else:
    foerder = 0.15 + 0.05  # Einzelmaßnahme + iSFP

# Deckel
foerder = min(foerder, 0.70)

zuschuss = kosten * foerder

# Ergebnis
st.subheader("Ergebnis")

st.write(f"Fördersatz: {int(foerder*100)} %")
st.write(f"Zuschuss: {int(zuschuss)} €")
st.write(f"Eigenanteil: {int(kosten - zuschuss)} €")

# einfache Einsparung
einsparung = kosten * 0.05
st.write(f"geschätzte jährliche Einsparung: {int(einsparung)} €")