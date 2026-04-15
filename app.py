import streamlit as st

st.set_page_config(page_title="iSFP Tool V2", layout="wide")

st.title("🏠 iSFP Tool – Version 2 (mit Dämmberechnung)")

# -------------------------
# Upload
# -------------------------
st.header("📂 Projekt")

uploaded_file = st.file_uploader("Bauplan hochladen", type=["pdf","png","jpg"])

# -------------------------
# Gebäudedaten
# -------------------------
st.header("Gebäudedaten")

baujahr = st.number_input("Baujahr", 1900, 2025, 1980)
wohnflaeche = st.number_input("Wohnfläche (m²)", 50, 500, 120)

# -------------------------
# U-Wert Logik
# -------------------------
def u_wert_wand(baujahr):
    if baujahr < 1978:
        return 1.3
    elif baujahr < 1995:
        return 0.8
    else:
        return 0.4

def u_wert_dach(baujahr):
    if baujahr < 1978:
        return 1.0
    elif baujahr < 1995:
        return 0.6
    else:
        return 0.3

# -------------------------
# Dämmstärke Berechnung
# -------------------------
def daemmstaerke(u_alt, u_ziel, lambda_wert=0.035):
    R_alt = 1 / u_alt
    d = lambda_wert * ((1 / u_ziel) - R_alt)
    return max(d, 0)

# -------------------------
# Maßnahmen
# -------------------------
st.header("Sanierungsmaßnahmen")

maßnahmen = st.multiselect(
    "Bauteile auswählen",
    ["Außenwand", "Dach"]
)

for m in maßnahmen:
    st.subheader(m)
    
    flaeche = st.number_input(f"Fläche {m} (m²)", 0, 500, 100, key=m)
    
    if m == "Außenwand":
        u_alt = u_wert_wand(baujahr)
        u_ziel = 0.20
    elif m == "Dach":
        u_alt = u_wert_dach(baujahr)
        u_ziel = 0.14
    
    d = daemmstaerke(u_alt, u_ziel)
    
    st.write(f"Alter U-Wert: {u_alt}")
    st.write(f"Ziel U-Wert: {u_ziel}")
    st.write(f"👉 erforderliche Dämmstärke: {round(d*100,1)} cm")
    
    if d > 0:
        st.error("❌ Anforderung aktuell NICHT erfüllt")
    else:
        st.success("✅ Anforderung erfüllt")

# -------------------------
# Hinweis
# -------------------------
st.info("Berechnung basiert auf vereinfachten Annahmen für die Energieberatung.")
