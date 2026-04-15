import streamlit as st
import json
import os

st.set_page_config(page_title="iSFP Tool V6", layout="wide")

st.title("🏠 iSFP Tool – Version 6 (Profi-Level)")

# -------------------------
# PROJEKTVERWALTUNG
# -------------------------
DB_FILE = "projekte.json"

def load_projects():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def save_project(data):
    projects = load_projects()
    projects.append(data)
    with open(DB_FILE, "w") as f:
        json.dump(projects, f)

# -------------------------
# Gebäudedaten
# -------------------------
st.header("Gebäude")

projektname = st.text_input("Projektname")

baujahr = st.number_input("Baujahr", 1900, 2025, 1980)
wohnflaeche = st.number_input("Wohnfläche (m²)", 50, 500, 120)
volumen = st.number_input("Gebäudevolumen (m³)", 100, 2000, 400)

luftwechsel = st.slider("Luftwechselrate (1/h)", 0.3, 1.5, 0.7)

# -------------------------
# Bauteile
# -------------------------
st.header("Bauteile")

bauteile = {
    "Außenwand": {"U_alt": 1.3, "U_ziel": 0.20},
    "Dach": {"U_alt": 1.0, "U_ziel": 0.14},
    "Fenster": {"U_alt": 2.7, "U_ziel": 0.95},
    "Kellerdecke": {"U_alt": 1.0, "U_ziel": 0.25}
}

H_alt = 0
H_neu = 0

for b in bauteile:
    st.subheader(b)
    
    flaeche = st.number_input(f"Fläche {b}", 0, 500, 100, key=b)
    
    U_alt = bauteile[b]["U_alt"]
    U_ziel = bauteile[b]["U_ziel"]
    
    H_alt += U_alt * flaeche
    H_neu += U_ziel * flaeche
    
    st.write(f"U-Wert alt: {U_alt}")
    st.write(f"U-Wert neu: {U_ziel}")

# -------------------------
# Energie (vereinfacht)
# -------------------------
st.header("Energie")

# Transmission
Q_trans_alt = H_alt * 0.024
Q_trans_neu = H_neu * 0.024

# Lüftung
Q_luft = 0.34 * luftwechsel * volumen * 0.024

energie_alt = (Q_trans_alt + Q_luft) / wohnflaeche * 1000
energie_neu = (Q_trans_neu + Q_luft) / wohnflaeche * 1000

einsparung = energie_alt - energie_neu

# CO2
co2 = einsparung * 0.2

# -------------------------
# Kosten & Förderung
# -------------------------
st.header("Kosten & Förderung")

kosten = st.number_input("Gesamtkosten (€)", 0, 200000, 50000)
foerder = kosten * 0.20

# -------------------------
# Ergebnisse
# -------------------------
st.header("📊 Ergebnisse")

st.write(f"Endenergie vorher: {int(energie_alt)} kWh/m²a")
st.write(f"Endenergie nachher: {int(energie_neu)} kWh/m²a")
st.write(f"Einsparung: {int(einsparung)} kWh/m²a")

st.write(f"CO₂-Ersparnis: {int(co2)} kg/m²a")

st.write(f"Förderung: {int(foerder)} €")

if einsparung > 0:
    amortisation = (kosten - foerder) / (einsparung * wohnflaeche * 0.1)
    st.write(f"Amortisation: {round(amortisation,1)} Jahre")

# -------------------------
# Projekt speichern
# -------------------------
if st.button("💾 Projekt speichern"):
    save_project({
        "name": projektname,
        "baujahr": baujahr,
        "energie_alt": energie_alt,
        "energie_neu": energie_neu
    })
    st.success("Projekt gespeichert!")

# -------------------------
# Projekte anzeigen
# -------------------------
st.header("📁 Gespeicherte Projekte")

projects = load_projects()
for p in projects:
    st.write(p)
