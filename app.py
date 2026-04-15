import streamlit as st

st.set_page_config(page_title="iSFP Tool V3", layout="wide")

st.title("🏠 iSFP Tool – Version 3 (Profi)")

# -------------------------
# Gebäudedaten
# -------------------------
st.header("Gebäude")

baujahr = st.number_input("Baujahr", 1900, 2025, 1980)
wohnflaeche = st.number_input("Wohnfläche (m²)", 50, 500, 120)

# -------------------------
# Materialien
# -------------------------
materialien = {
    "EPS": 0.035,
    "Mineralwolle": 0.040,
    "Holzfaser": 0.045
}

preise = {
    "Außenwand": 150,
    "Dach": 200,
    "Kellerdecke": 80,
    "Fenster": 600
}

# -------------------------
# U-Werte (vereinfacht)
# -------------------------
def u_wert(baujahr, bauteil):
    if bauteil == "Außenwand":
        return 1.3 if baujahr < 1978 else 0.8
    if bauteil == "Dach":
        return 1.0 if baujahr < 1978 else 0.6
    if bauteil == "Kellerdecke":
        return 1.0 if baujahr < 1978 else 0.8
    if bauteil == "Fenster":
        return 2.7 if baujahr < 1995 else 1.5

# Zielwerte BAFA
zielwerte = {
    "Außenwand": 0.20,
    "Dach": 0.14,
    "Kellerdecke": 0.25,
    "Fenster": 0.95
}

# -------------------------
# Dämmstärke
# -------------------------
def daemmstaerke(u_alt, u_ziel, lambda_wert):
    R_alt = 1 / u_alt
    d = lambda_wert * ((1 / u_ziel) - R_alt)
    return max(d, 0)

# -------------------------
# Maßnahmen
# -------------------------
st.header("Maßnahmen")

bauteile = st.multiselect("Bauteile auswählen", list(zielwerte.keys()))

kosten_gesamt = 0
foerder_gesamt = 0

for b in bauteile:
    st.subheader(b)
    
    flaeche = st.number_input(f"Fläche {b} (m²)", 0, 500, 100, key=b)
    
    material = st.selectbox(f"Dämmstoff {b}", list(materialien.keys()), key=b+"mat")
    lambda_wert = materialien[material]
    
    u_alt = u_wert(baujahr, b)
    u_ziel = zielwerte[b]
    
    d = daemmstaerke(u_alt, u_ziel, lambda_wert)
    
    kosten = flaeche * preise[b]
    
    # Förderung
    foerder = 0.20
    zuschuss = kosten * foerder
    
    kosten_gesamt += kosten
    foerder_gesamt += zuschuss
    
    # Anzeige
    st.write(f"Alter U-Wert: {u_alt}")
    st.write(f"Ziel U-Wert: {u_ziel}")
    st.write(f"👉 Dämmstärke: {round(d*100,1)} cm")
    st.write(f"💰 Kosten: {int(kosten)} €")
    st.write(f"💶 Förderung: {int(zuschuss)} €")
    
    if d > 0:
        st.error("❌ nicht erfüllt")
    else:
        st.success("✅ erfüllt")

# -------------------------
# Gesamt
# -------------------------
st.header("Gesamt")

st.write(f"💰 Investition: {int(kosten_gesamt)} €")
st.write(f"💶 Förderung: {int(foerder_gesamt)} €")
st.write(f"🏦 Eigenanteil: {int(kosten_gesamt - foerder_gesamt)} €")
