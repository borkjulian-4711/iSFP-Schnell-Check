import streamlit as st

st.set_page_config(page_title="iSFP Tool V4", layout="wide")

st.title("🏠 iSFP Tool – Version 4 (Profi Energieberatung)")

# -------------------------
# Gebäudedaten
# -------------------------
st.header("Gebäude")

baujahr_global = st.number_input("Baujahr Gebäude", 1900, 2025, 1980)

# -------------------------
# U-Wert Tabellen (vereinfacht nach Bekanntmachung)
# -------------------------
def u_wert_lookup(baujahr, bauteil, bauart=None):
    if bauteil == "Außenwand":
        return 1.3 if baujahr < 1978 else 0.8 if baujahr < 1995 else 0.4
    
    if bauteil == "Dach":
        if bauart == "Steildach":
            return 1.0 if baujahr < 1978 else 0.6
        if bauart == "Flachdach":
            return 0.8 if baujahr < 1978 else 0.5
    
    if bauteil == "Fenster":
        return 2.7 if baujahr < 1995 else 1.5
    
    if bauteil == "Kellerdecke":
        return 1.0 if baujahr < 1978 else 0.8
    
    if bauteil == "Bodenplatte":
        return 0.9
    
    if bauteil == "Tür":
        return 3.0

# Zielwerte BAFA
zielwerte = {
    "Außenwand": 0.20,
    "Dach": 0.14,
    "Fenster": 0.95,
    "Kellerdecke": 0.25,
    "Bodenplatte": 0.30,
    "Tür": 1.30
}

# -------------------------
# IST-ZUSTAND
# -------------------------
st.header("🔍 Ist-Zustand")

bauteile = ["Außenwand","Dach","Fenster","Kellerdecke","Bodenplatte","Tür"]

ist_daten = {}

for b in bauteile:
    st.subheader(b)
    
    use_global = st.checkbox(f"Baujahr Gebäude verwenden ({b})", value=True, key=b)
    
    if use_global:
        baujahr = baujahr_global
    else:
        baujahr = st.number_input(f"Baujahr {b}", 1900, 2025, 1980, key=b+"jahr")
    
    bauart = None
    if b == "Dach":
        bauart = st.selectbox("Dachart", ["Steildach","Flachdach"], key=b+"art")
    
    u_alt = u_wert_lookup(baujahr, b, bauart)
    
    ist_daten[b] = u_alt
    
    st.write(f"👉 U-Wert Ist: {u_alt}")

# -------------------------
# SANIERUNG
# -------------------------
st.header("🧱 Sanierung")

kosten_gesamt = 0
foerder_gesamt = 0

for b in bauteile:
    st.subheader(b)
    
    flaeche = st.number_input(f"Fläche {b} (m²)", 0, 500, 100, key=b+"f")
    
    lambda_wert = st.number_input(f"Wärmeleitfähigkeit λ {b}", 0.02, 0.08, 0.035, key=b+"l")
    
    u_alt = ist_daten[b]
    u_ziel = zielwerte[b]
    
    # Dämmstärke
    R_alt = 1 / u_alt
    d = lambda_wert * ((1 / u_ziel) - R_alt)
    d = max(d, 0)
    
    kosten = flaeche * 150
    foerder = kosten * 0.20
    
    kosten_gesamt += kosten
    foerder_gesamt += foerder
    
    st.write(f"Ziel U-Wert: {u_ziel}")
    st.write(f"👉 Dämmstärke: {round(d*100,1)} cm")
    st.write(f"💰 Kosten: {int(kosten)} €")
    
    if d > 0:
        st.error("❌ nicht erfüllt")
    else:
        st.success("✅ erfüllt")

# -------------------------
# Gesamtbewertung
# -------------------------
st.header("📊 Gesamtbewertung")

st.write(f"💰 Investition: {int(kosten_gesamt)} €")
st.write(f"💶 Förderung: {int(foerder_gesamt)} €")
st.write(f"🏦 Eigenanteil: {int(kosten_gesamt - foerder_gesamt)} €")
