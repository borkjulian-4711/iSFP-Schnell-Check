import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt

# -------------------------
# PDF FUNKTION
# -------------------------
def create_full_pdf(projektname, baujahr, bauteile_daten, kosten_gesamt, foerder_gesamt):

    plt.figure()
    plt.bar(["Vorher","Nachher"], [200,120])
    plt.savefig("energie.png")
    plt.close()

    doc = SimpleDocTemplate("isfp_profi_bericht.pdf")
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Individueller Sanierungsfahrplan (iSFP)", styles["Title"]))
    content.append(Spacer(1,12))

    content.append(Paragraph(f"Projekt: {projektname}", styles["Normal"]))
    content.append(Paragraph(f"Baujahr: {baujahr}", styles["Normal"]))

    content.append(Spacer(1,12))

    content.append(Paragraph("Bauteile:", styles["Heading2"]))

    for b in bauteile_daten:
        content.append(Paragraph(
            f"{b['name']} ({b['konstruktion']}): "
            f"{b['material']} WLG {b['wlg']} | "
            f"U alt {b['u_alt']} → U neu {b['u_neu']} | "
            f"Dämmung {b['d']} cm",
            styles["Normal"]
        ))

    content.append(Spacer(1,12))

    content.append(Paragraph("Kosten & Förderung:", styles["Heading2"]))
    content.append(Paragraph(f"Gesamtkosten: {int(kosten_gesamt)} €", styles["Normal"]))
    content.append(Paragraph(f"Förderung: {int(foerder_gesamt)} €", styles["Normal"]))

    doc.build(content)

# -------------------------
# DATEN
# -------------------------
baualter = {
    "vor 1978": 0,
    "1979–1995": 1,
    "1996–2001": 2,
    "ab 2002": 3
}

konstruktionen = {
    "Außenwand": {
        "Massivbau": [1.4, 0.8, 0.5, 0.35],
        "Holzbau": [0.9, 0.6, 0.4, 0.28]
    },
    "Dach": {
        "Steildach": [1.0, 0.6, 0.3, 0.2],
        "Flachdach": [0.8, 0.5, 0.3, 0.2]
    },
    "Fenster": {
        "2-fach": [2.7, 1.9, 1.5, 1.3],
        "3-fach": [1.5, 1.3, 1.1, 0.9]
    }
}

zielwerte = {
    "Außenwand": 0.20,
    "Dach": 0.14,
    "Fenster": 0.95
}

# Materialien + WLG
materialien = {
    "Mineralwolle": [0.035, 0.040],
    "EPS": [0.032, 0.035, 0.040],
    "XPS": [0.032, 0.035],
    "PUR/PIR": [0.024, 0.028],
    "Holzweichfaser": [0.040, 0.045]
}

# -------------------------
# APP
# -------------------------
st.set_page_config(page_title="iSFP Tool 9.2", layout="wide")
st.title("🏠 iSFP Tool – Version 9.2 (Materialvergleich)")

projektname = st.text_input("Projektname", "Musterprojekt")
baujahr = st.number_input("Baujahr", 1900, 2025, 1980)

bauteile_daten = []
kosten_gesamt = 0
foerder_gesamt = 0

# -------------------------
# BAUTEIL AUSWAHL
# -------------------------
st.header("Bauteil")

bauteil = st.selectbox("Bauteil", list(konstruktionen.keys()))
konstruktion = st.selectbox("Konstruktion", list(konstruktionen[bauteil].keys()))
baujahr_klasse = st.selectbox("Baualtersklasse", list(baualter.keys()))

index = baualter[baujahr_klasse]
u_alt = konstruktionen[bauteil][konstruktion][index]
u_ziel = zielwerte[bauteil]

st.write(f"U-Wert Bestand: {u_alt}")
st.write(f"Ziel U-Wert: {u_ziel}")

# -------------------------
# MATERIALVERGLEICH
# -------------------------
st.header("Materialvergleich")

vergleich = []

for mat, wlg_list in materialien.items():
    for lam in wlg_list:

        R_alt = 1 / u_alt
        d = lam * ((1 / u_ziel) - R_alt)
        d = max(d, 0)

        vergleich.append({
            "Material": mat,
            "λ": lam,
            "Dämmstärke (cm)": round(d * 100,1)
        })

st.write("### Vergleich optimale Dämmstärke")
st.dataframe(vergleich)

# -------------------------
# AUSWAHL EINER VARIANTE
# -------------------------
st.header("Auswahl")

material = st.selectbox("Material wählen", list(materialien.keys()))
lambda_wert = st.selectbox("λ wählen", materialien[material])

d_cm = st.slider("Dämmstärke (cm)", 0, 30, 12)
d = d_cm / 100

U_neu = 1 / ((1/u_alt) + d / lambda_wert)

st.write(f"Neuer U-Wert: {round(U_neu,3)}")

if U_neu <= u_ziel:
    st.success("✅ erfüllt")
else:
    st.error("❌ nicht erfüllt")

# -------------------------
# KOSTEN
# -------------------------
kosten = st.number_input("Kosten (€)", 0, 100000, 20000)
foerder = kosten * 0.20

kosten_gesamt += kosten
foerder_gesamt += foerder

# -------------------------
# BAUTEIL SPEICHERN
# -------------------------
if st.button("➕ Bauteil hinzufügen"):
    bauteile_daten.append({
        "name": bauteil,
        "konstruktion": konstruktion,
        "material": material,
        "wlg": lambda_wert,
        "u_alt": round(u_alt,2),
        "u_neu": round(U_neu,2),
        "d": d_cm,
        "kosten": kosten
    })
    st.success("Bauteil hinzugefügt")

# -------------------------
# ÜBERSICHT
# -------------------------
st.header("Übersicht")

st.write(bauteile_daten)

st.write(f"💰 Investition: {int(kosten_gesamt)} €")
st.write(f"💶 Förderung: {int(foerder_gesamt)} €")

# -------------------------
# PDF
# -------------------------
if st.button("📄 Bericht erstellen"):
    create_full_pdf(
        projektname,
        baujahr,
        bauteile_daten,
        kosten_gesamt,
        foerder_gesamt
    )

    with open("isfp_profi_bericht.pdf", "rb") as f:
        st.download_button("Download Bericht", f)
