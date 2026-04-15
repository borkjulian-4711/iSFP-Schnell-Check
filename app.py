import streamlit as st
import json

st.set_page_config(page_title="iSFP Tool V5", layout="wide")

st.title("🏠 iSFP Tool – Version 5 (Profi)")

# -------------------------
# PROJEKT SPEICHERN
# -------------------------
def save_project(data):
    with open("projekt.json", "w") as f:
        json.dump(data, f)

# -------------------------
# Gebäudedaten
# -------------------------
st.header("Gebäude")

baujahr = st.number_input("Baujahr", 1900, 2025, 1980)
wohnflaeche = st.number_input("Wohnfläche (m²)", 50, 500, 120)

# -------------------------
# U-Wert Funktion
# -------------------------
def u_wert(baujahr):
    if baujahr < 1978:
        return 1.3
    elif baujahr < 1995:
        return 0.8
    else:
        return 0.4

u_alt = u_wert(baujahr)

# -------------------------
# Energiebedarf (vereinfacht)
# -------------------------
energie_alt = u_alt * 100  # grobe Näherung
energie_neu = energie_alt * 0.6

einsparung_kwh = energie_alt - energie_neu

# CO2 (0.2 kg/kWh)
co2 = einsparung_kwh * 0.2

# -------------------------
# Maßnahmen
# -------------------------
st.header("Sanierung")

kosten = st.number_input("Gesamtkosten (€)", 0, 200000, 50000)

foerder = 0.20
zuschuss = kosten * foerder

# -------------------------
# Wirtschaftlichkeit
# -------------------------
st.header("📊 Ergebnisse")

st.write(f"Endenergie vorher: {int(energie_alt)} kWh/m²a")
st.write(f"Endenergie nachher: {int(energie_neu)} kWh/m²a")

st.write(f"Einsparung: {int(einsparung_kwh)} kWh/m²a")

st.write(f"CO₂-Ersparnis: {int(co2)} kg/m²a")

st.write(f"Förderung: {int(zuschuss)} €")

if einsparung_kwh > 0:
    amortisation = (kosten - zuschuss) / (einsparung_kwh * wohnflaeche * 0.1)
    st.write(f"Amortisation: {round(amortisation,1)} Jahre")

# -------------------------
# Projekt speichern
# -------------------------
if st.button("💾 Projekt speichern"):
    save_project({
        "baujahr": baujahr,
        "wohnflaeche": wohnflaeche,
        "kosten": kosten
    })
    st.success("Projekt gespeichert!")

# -------------------------
# Bericht
# -------------------------
st.header("📄 Bericht")

st.write("Gebäudeanalyse, Maßnahmen und Empfehlung werden hier dargestellt.")

if st.button("📄 Bericht anzeigen"):
    st.write("Sanierung empfohlen – große Einsparpotenziale vorhanden.")
