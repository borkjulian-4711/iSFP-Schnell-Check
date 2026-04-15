import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt

# -------------------------
# PDF FUNKTION
# -------------------------
def create_full_pdf(projektname, baujahr, bauteile_daten, kosten_gesamt, foerder_gesamt):

    # Diagramm erzeugen
    energie_alt = 200
    energie_neu = 120

    plt.figure()
    plt.bar(["Vorher","Nachher"], [energie_alt, energie_neu])
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
            f"{b['name']}: U alt {b['u_alt']} → U neu {b['u_neu']} | Dämmung {b['d']} cm",
            styles["Normal"]
        ))

    content.append(Spacer(1,12))

    content.append(Paragraph("Kosten & Förderung:", styles["Heading2"]))
    content.append(Paragraph(f"Gesamtkosten: {int(kosten_gesamt)} €", styles["Normal"]))
    content.append(Paragraph(f"Förderung: {int(foerder_gesamt)} €", styles["Normal"]))
    content.append(Paragraph(f"Eigenanteil: {int(kosten_gesamt - foerder_gesamt)} €", styles["Normal"]))

    doc.build(content)

# -------------------------
# APP START
# -------------------------
st.set_page_config(page_title="iSFP Tool", layout="wide")

st.title("🏠 iSFP Beratungs-Tool (Profi)")

# -------------------------
# PROJEKT
# -------------------------
st.header("Projekt")

projektname = st.text_input("Projektname", "Musterprojekt")
baujahr = st.number_input("Baujahr", 1900, 2025, 1980)

# -------------------------
# DATEN INITIALISIEREN
# -------------------------
bauteile_daten = []
kosten_gesamt = 0
foerder_gesamt = 0

# -------------------------
# BAUTEILE
# -------------------------
st.header("Bauteile")

bauteile = st.multiselect(
    "Bauteile auswählen",
    ["Außenwand", "Dach", "Fenster", "Kellerdecke"]
)

for b in bauteile:
    st.subheader(b)

    kosten = st.number_input(f"Kosten {b} (€)", 0, 50000, 10000, key=b)

    # Beispielwerte (später durch deine Version 7 Logik ersetzen!)
    u_alt = 1.0
    u_neu = 0.2
    d = 12  # cm

    foerder = kosten * 0.2

    kosten_gesamt += kosten
    foerder_gesamt += foerder

    st.write(f"U-Wert alt: {u_alt}")
    st.write(f"U-Wert neu: {u_neu}")
    st.write(f"Dämmung: {d} cm")
    st.write(f"Förderung: {int(foerder)} €")

    # 🔥 DATEN SAMMELN (WICHTIG!)
    bauteile_daten.append({
        "name": b,
        "u_alt": u_alt,
        "u_neu": u_neu,
        "d": d,
        "kosten": kosten
    })

# -------------------------
# GESAMT
# -------------------------
st.header("Gesamt")

st.write(f"💰 Investition: {int(kosten_gesamt)} €")
st.write(f"💶 Förderung: {int(foerder_gesamt)} €")
st.write(f"🏦 Eigenanteil: {int(kosten_gesamt - foerder_gesamt)} €")

# -------------------------
# PDF BUTTON
# -------------------------
st.header("Bericht")

if st.button("📄 iSFP Bericht erstellen"):

    create_full_pdf(
        projektname,
        baujahr,
        bauteile_daten,
        kosten_gesamt,
        foerder_gesamt
    )

    with open("isfp_profi_bericht.pdf", "rb") as f:
        st.download_button(
            "Download Bericht",
            f,
            file_name="iSFP_Bericht.pdf"
        )
