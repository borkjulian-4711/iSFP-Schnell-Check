import streamlit as st

st.header("🧱 Bauteile nach Bekanntmachung (Tabelle 2)")

# -------------------------
# Baualtersklassen
# -------------------------
baualter = {
    "vor 1978": 0,
    "1979–1995": 1,
    "1996–2001": 2,
    "ab 2002": 3
}

# -------------------------
# Tabelle 2 (vereinfacht aber strukturiert)
# -------------------------
konstruktionen = {
    "Außenwand": {
        "Massivbau": [1.4, 0.8, 0.5, 0.35],
        "Holzbau": [0.9, 0.6, 0.4, 0.28],
        "Zweischalig": [1.2, 0.7, 0.45, 0.30]
    },
    "Dach": {
        "Steildach ungedämmt": [1.0, 0.8, 0.6, 0.4],
        "Steildach gedämmt": [0.6, 0.4, 0.3, 0.2],
        "Flachdach": [0.8, 0.6, 0.4, 0.25]
    },
    "Kellerdecke": {
        "Massiv": [1.0, 0.8, 0.6, 0.4]
    },
    "Bodenplatte": {
        "gegen Erdreich": [0.9, 0.7, 0.5, 0.35]
    },
    "Fenster": {
        "2-fach": [2.7, 1.9, 1.5, 1.3],
        "3-fach": [1.5, 1.3, 1.1, 0.9]
    },
    "Tür": {
        "Standard": [3.0, 2.5, 2.0, 1.5]
    }
}

# Zielwerte
zielwerte = {
    "Außenwand": 0.20,
    "Dach": 0.14,
    "Kellerdecke": 0.25,
    "Bodenplatte": 0.30,
    "Fenster": 0.95,
    "Tür": 1.30
}

# WLG
wlg_dict = {
    "032": 0.032,
    "035": 0.035,
    "040": 0.040
}

# -------------------------
# Auswahl
# -------------------------
bauteil = st.selectbox("Bauteil", list(konstruktionen.keys()))

konstruktion = st.selectbox(
    "Konstruktion",
    list(konstruktionen[bauteil].keys())
)

baujahr_klasse = st.selectbox(
    "Baualtersklasse",
    list(baualter.keys())
)

index = baualter[baujahr_klasse]

u_alt = konstruktionen[bauteil][konstruktion][index]
u_ziel = zielwerte[bauteil]

st.write(f"👉 U-Wert Ist: {u_alt}")
st.write(f"👉 Ziel U-Wert: {u_ziel}")

# -------------------------
# Dämmung
# -------------------------
st.subheader("Dämmung")

wlg = st.selectbox("Wärmeleitgruppe", list(wlg_dict.keys()))
lambda_wert = wlg_dict[wlg]

# optimale Dämmstärke berechnen
R_alt = 1 / u_alt
d_opt = lambda_wert * ((1 / u_ziel) - R_alt)
d_opt = max(d_opt, 0)

st.write(f"👉 erforderliche Dämmstärke: {round(d_opt*100,1)} cm")

# manuelle Anpassung
d_cm = st.slider("Dämmstärke anpassen (cm)", 0, 30, int(d_opt*100))
d = d_cm / 100

U_neu = 1 / (R_alt + d / lambda_wert)

st.write(f"👉 neuer U-Wert: {round(U_neu,3)}")

# Bewertung
if U_neu <= u_ziel:
    st.success("✅ Anforderung erfüllt")
else:
    st.error("❌ Anforderung nicht erfüllt")
