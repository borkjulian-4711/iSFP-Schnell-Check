from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_isfp_pdf(projektname, baujahr, bauteil, konstruktion, u_alt, u_ziel, d_opt, kosten, foerder):

    doc = SimpleDocTemplate("isfp_bericht.pdf")
    styles = getSampleStyleSheet()
    content = []

    # Titel
    content.append(Paragraph("Individueller Sanierungsfahrplan (iSFP)", styles["Title"]))
    content.append(Spacer(1,12))

    # Gebäude
    content.append(Paragraph("1. Gebäudeübersicht", styles["Heading2"]))
    content.append(Paragraph(f"Projekt: {projektname}", styles["Normal"]))
    content.append(Paragraph(f"Baujahr: {baujahr}", styles["Normal"]))
    
    content.append(Spacer(1,12))

    # IST
    content.append(Paragraph("2. Energetischer Ist-Zustand", styles["Heading2"]))
    content.append(Paragraph(f"Bauteil: {bauteil}", styles["Normal"]))
    content.append(Paragraph(f"Konstruktion: {konstruktion}", styles["Normal"]))
    content.append(Paragraph(f"U-Wert Bestand: {u_alt}", styles["Normal"]))

    content.append(Spacer(1,12))

    # Maßnahme
    content.append(Paragraph("3. Empfohlene Maßnahme", styles["Heading2"]))
    content.append(Paragraph(f"Ziel U-Wert: {u_ziel}", styles["Normal"]))
    content.append(Paragraph(f"Erforderliche Dämmstärke: {round(d_opt*100,1)} cm", styles["Normal"]))

    content.append(Spacer(1,12))

    # Fahrplan
    content.append(Paragraph("4. Sanierungsfahrplan", styles["Heading2"]))
    content.append(Paragraph("Schritt 1: Gebäudehülle verbessern", styles["Normal"]))
    content.append(Paragraph("Schritt 2: Anlagentechnik optimieren", styles["Normal"]))

    content.append(Spacer(1,12))

    # Wirtschaftlichkeit
    content.append(Paragraph("5. Wirtschaftlichkeit", styles["Heading2"]))
    content.append(Paragraph(f"Kosten: {int(kosten)} €", styles["Normal"]))
    content.append(Paragraph(f"Förderung: {int(foerder)} €", styles["Normal"]))

    content.append(Spacer(1,12))

    # Fazit
    content.append(Paragraph("6. Fazit", styles["Heading2"]))
    content.append(Paragraph("Die Maßnahme verbessert die Energieeffizienz deutlich und ist förderfähig.", styles["Normal"]))

    doc.build(content)
