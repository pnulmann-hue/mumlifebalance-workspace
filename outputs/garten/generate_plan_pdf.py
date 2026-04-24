"""Generate a beautiful PDF of Patricia's 2026 garden plan for visitors."""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
)
from datetime import datetime

# Garden color palette
FOREST = colors.HexColor("#2d6a4f")
LEAF = colors.HexColor("#588157")
LIGHT = colors.HexColor("#a7c957")
CREAM = colors.HexColor("#f0f4e8")
EARTH = colors.HexColor("#6b4f3b")
TOMATO = colors.HexColor("#c1292e")
SUN = colors.HexColor("#e9c46a")

OUT = "C:/Users/pnulm/Desktop/Mein Business/outputs/garten/Garten-Plan-2026.pdf"

doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    topMargin=2*cm, bottomMargin=2*cm,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    title="Patricias Garten-Plan 2026",
    author="Patricia Nulmann"
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "Title", parent=styles["Title"],
    fontSize=28, textColor=FOREST, alignment=TA_CENTER,
    spaceAfter=6, leading=34, fontName="Helvetica-Bold"
)
subtitle_style = ParagraphStyle(
    "Subtitle", parent=styles["Normal"],
    fontSize=14, textColor=LEAF, alignment=TA_CENTER,
    spaceAfter=20, leading=18, fontName="Helvetica-Oblique"
)
h1_style = ParagraphStyle(
    "H1", parent=styles["Heading1"],
    fontSize=18, textColor=FOREST, fontName="Helvetica-Bold",
    spaceBefore=12, spaceAfter=10
)
h2_style = ParagraphStyle(
    "H2", parent=styles["Heading2"],
    fontSize=13, textColor=LEAF, fontName="Helvetica-Bold",
    spaceBefore=10, spaceAfter=6
)
body_style = ParagraphStyle(
    "Body", parent=styles["Normal"],
    fontSize=10.5, leading=14, textColor=colors.HexColor("#333333"),
    alignment=TA_LEFT, spaceAfter=6
)
quote_style = ParagraphStyle(
    "Quote", parent=body_style,
    fontSize=11, textColor=EARTH, fontName="Helvetica-Oblique",
    leftIndent=20, rightIndent=20, spaceBefore=8, spaceAfter=12,
    alignment=TA_CENTER
)
caption_style = ParagraphStyle(
    "Caption", parent=body_style,
    fontSize=9, textColor=colors.HexColor("#777777"),
    alignment=TA_CENTER, spaceBefore=2
)

story = []

# ============= COVER =============
story.append(Spacer(1, 3*cm))
story.append(Paragraph("Patricias Garten-Plan", title_style))
story.append(Paragraph("2026", ParagraphStyle(
    "Year", parent=title_style, fontSize=56, textColor=LEAF, spaceAfter=4
)))
story.append(Paragraph("Appenzellerland &middot; 920 m &uuml;.M. &middot; Permakultur", subtitle_style))
story.append(Spacer(1, 1*cm))
story.append(Paragraph(
    "&laquo;Ein Garten ist kein Ort. Er ist eine Beziehung. "
    "Zwischen dir, dem Boden, den Pflanzen und den Jahreszeiten.&raquo;",
    quote_style
))
story.append(Spacer(1, 2*cm))

# Quick facts table
facts_data = [
    ["Standort", "Appenzellerland, 920 m &uuml;.M."],
    ["Klimazone", "Alpin/voralpin &middot; USDA 6b"],
    ["Vegetationsperiode", "Mitte Mai bis Ende September (ca. 130 Tage)"],
    ["Anbaufl&auml;che", "ca. 16-17 m&sup2; aktiv &middot; 6 Zonen-Rotation"],
    ["Philosophie", "Permakultur &middot; Mischkultur &middot; Mondkalender"],
    ["Vorbild", "Marie Diederich (Wurzelwerk)"],
]
facts_tbl = Table(
    [[Paragraph(k, ParagraphStyle("fk", parent=body_style, fontName="Helvetica-Bold", textColor=FOREST)),
      Paragraph(v, body_style)] for k, v in facts_data],
    colWidths=[5*cm, 11*cm]
)
facts_tbl.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("LINEBELOW", (0, 0), (-1, -2), 0.5, LIGHT),
]))
story.append(facts_tbl)
story.append(Spacer(1, 2*cm))
story.append(Paragraph(f"Stand: {datetime.now().strftime('%d. %B %Y')}", caption_style))

story.append(PageBreak())

# ============= PHILOSOPHY =============
story.append(Paragraph("Das 6-Zonen-System", h1_style))
story.append(Paragraph(
    "Nach Marie Diederichs Prinzip wandert jede Pflanzenfamilie jedes Jahr "
    "ein Beet weiter. So kann sich der Boden erholen, Krankheiten bauen "
    "sich nicht auf, und jede Familie findet die N&auml;hrstoffe vor, die sie braucht.",
    body_style
))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Die Rotation folgt dem Bodenbed&uuml;rfnis: <b>Starkzehrer</b> zehren "
    "den Boden aus &rarr; <b>Mittelzehrer</b> arbeiten moderat &rarr; "
    "<b>Schwachzehrer</b> lassen den Boden sich erholen &rarr; "
    "<b>H&uuml;lsenfr&uuml;chte</b> binden Stickstoff und bauen ihn wieder auf. "
    "Dann beginnt der Kreislauf von vorn.",
    body_style
))

story.append(Paragraph("Pflanzenfamilien &amp; ihre Rolle", h2_style))

family_data = [
    ["Familie", "Zehrer", "Beispiele"],
    ["Kreuzbl&uuml;tler", "Starkzehrer", "Kohl, Broccoli, Radieschen, Rucola"],
    ["Nachtschatten", "Starkzehrer", "Tomaten, Peperoni, Kartoffeln"],
    ["K&uuml;rbisgew&auml;chse", "Starkzehrer", "Zucchini, Gurken, K&uuml;rbis"],
    ["Zwiebelgew&auml;chse", "Mittelzehrer", "Zwiebeln, Lauch, Knoblauch"],
    ["Doldenbl&uuml;tler", "Mittelzehrer", "Karotten, Fenchel, Sellerie, Pastinake"],
    ["Korbbl&uuml;tler", "Schwachzehrer", "Salate, Radicchio, Chicor&eacute;e"],
    ["Fuchsschwanz", "Schwachzehrer", "Mangold, Rande, Spinat"],
    ["H&uuml;lsenfr&uuml;chte", "Stickstoffbinder", "Bohnen, Erbsen, Kefe"],
]
family_tbl = Table(
    [[Paragraph(cell, ParagraphStyle(
        "ft", parent=body_style,
        fontName="Helvetica-Bold" if i == 0 else "Helvetica",
        textColor=colors.white if i == 0 else colors.HexColor("#333333"),
        fontSize=10
    )) for cell in row] for i, row in enumerate(family_data)],
    colWidths=[4.5*cm, 4*cm, 8*cm]
)
family_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), FOREST),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CREAM, colors.white]),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
]))
story.append(family_tbl)

story.append(PageBreak())

# ============= OVERVIEW =============
story.append(Paragraph("Der Plan 2026 &mdash; auf einen Blick", h1_style))

overview_data = [
    ["Beet", "2025 war...", "2026 wird..."],
    ["Hochbeet 1", "Kreuzbl&uuml;tler + Doldenbl&uuml;tler\n(Kohl, Broccoli, Karotten)", "Korbbl&uuml;tler\n(Salate in Staffelaussaat)"],
    ["Hochbeet 2", "Korbbl&uuml;tler\n(Salate, Mangold, Rande)", "H&uuml;lsenfr&uuml;chte\n(Buschbohne, Kefe, Erbsen)"],
    ["Hochbeet 3 links", "H&uuml;lsenfr&uuml;chte\n(Buschbohne, Kefe)", "Starkzehrer K&uuml;rbis\n(Zucchini, Gurke, Zuckermelone)"],
    ["Hochbeet 3 rechts", "Kreuzbl&uuml;tler + Doldenbl&uuml;tler", "Zwiebelgew&auml;chse + Kr&auml;uter\n(Zwiebel, Lauch, Basilikum)"],
    ["L&auml;ngsbeet 1", "Nachtschatten\n(Tomaten, Peperoni, Gurke)", "Kreuzbl&uuml;tler\n(Kohl, Broccoli, Kohlrabi)"],
    ["L&auml;ngsbeet 2", "Nachtschatten\n(Tomaten, Peperoni, Zucchini)", "Doldenbl&uuml;tler + Rande\n(Karotten, Fenchel, Sellerie)"],
    ["Tomatenbereich\n(12 Beete, Ost)", "Neu angelegt", "Tomaten + Peperoni\n(10 + 2 + 7 + 4 Pflanzen)"],
]
overview_tbl = Table(
    [[Paragraph(cell, ParagraphStyle(
        "ot", parent=body_style,
        fontName="Helvetica-Bold" if i == 0 else "Helvetica",
        textColor=colors.white if i == 0 else colors.HexColor("#333333"),
        fontSize=9.5, leading=12
    )) for cell in row] for i, row in enumerate(overview_data)],
    colWidths=[4*cm, 6*cm, 6.5*cm]
)
overview_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), FOREST),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CREAM, colors.white]),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("LINEABOVE", (0, 1), (-1, 1), 1, LEAF),
]))
story.append(overview_tbl)

story.append(PageBreak())

# ============= BEET DETAILS =============
story.append(Paragraph("Beet f&uuml;r Beet", h1_style))
story.append(Paragraph(
    "Hier steht detailliert, was 2026 in jedem Beet w&auml;chst &mdash; "
    "inklusive Sortennamen, Pflegehinweisen und dem &Uuml;bergang ins n&auml;chste Jahr.",
    body_style
))

beet_data = [
    {
        "name": "Hochbeet 1 &mdash; Salate",
        "family": "Korbbl&uuml;tler (Schwachzehrer)",
        "plants": "Kopfsalat Pirat, Batavia, Eichblatt, Schnittsalat, Buttersalat",
        "tipp": "<b>Staffelaussaat:</b> Alle 2-3 Wochen neu nachs&auml;en, damit immer Salat bereit ist. Mulch ab Juni spart Wasser.",
        "next": "2027: H&uuml;lsenfr&uuml;chte"
    },
    {
        "name": "Hochbeet 2 &mdash; Stickstoff-Werk",
        "family": "H&uuml;lsenfr&uuml;chte (N-Binder)",
        "plants": "Buschbohne la Victoire, Kefe, Erbsen",
        "tipp": "<b>Kein N-D&uuml;nger!</b> Die Bohnen binden Luftstickstoff und bauen den Boden auf. Nach der Ernte Gr&uuml;nd&uuml;ngung (Phacelia) bis Winter.",
        "next": "2027: Starkzehrer K&uuml;rbisgew&auml;chse"
    },
    {
        "name": "Hochbeet 3 links &mdash; Kletterei",
        "family": "K&uuml;rbisgew&auml;chse (Starkzehrer)",
        "plants": "Zucchini, Gurke mexikanische mini, Zuckermelone",
        "tipp": "Profitiert vom Stickstoff der Vorkultur. <b>Reichlich Kompost</b> einarbeiten, Mulch ab Juni, sch&ouml;n giessen.",
        "next": "2027: Kreuzbl&uuml;tler (Kohl)"
    },
    {
        "name": "Hochbeet 3 rechts &mdash; Duft &amp; W&uuml;rze",
        "family": "Zwiebelgew&auml;chse + Kr&auml;uter (Mittel-/Schwach)",
        "plants": "W&auml;denswiler Zwiebeln, Hilarich Herbstlauch, Basilikum, Petersilie",
        "tipp": "<b>Wenig giessen</b>, kein Frischkompost. Basilikum mag Sonne und etwas W&auml;rme &mdash; sp&auml;ter auspflanzen (Juni).",
        "next": "2027: Korbbl&uuml;tler (Salate)"
    },
    {
        "name": "L&auml;ngsbeet 1 &mdash; Kohlparade",
        "family": "Kreuzbl&uuml;tler (Starkzehrer)",
        "plants": "Blumenkohl, Broccoli Calabrese, Kohlrabi, Rosenkohl rubine, Chinakohl, Radieschen (Staffelsaat)",
        "tipp": "<b>3-Jahres-Pause von Nachtschatten!</b> Kompost vor Anbau. Kohl braucht viel Wasser. Radieschen als Zwischenkultur.",
        "next": "2027: Doldenbl&uuml;tler (Karotten, Sellerie)"
    },
    {
        "name": "L&auml;ngsbeet 2 &mdash; Wurzeln &amp; Knollen",
        "family": "Doldenbl&uuml;tler + Rande (Mittelzehrer)",
        "plants": "Karotten Amiva, Bunte M&ouml;hrenmischung, Fenchel Bianco, Fenchel Selma, Knollensellerie, Pastinake, Rande Chioggia, Rande Golden",
        "tipp": "Karotten 5 cm Abstand in Reihe (Reihenabstand 20 cm), Pastinaken 10 cm. Moderate D&uuml;ngung, geduldig bleiben &mdash; Ernte ab Herbst.",
        "next": "2027: H&uuml;lsenfr&uuml;chte"
    },
]

for b in beet_data:
    story.append(Spacer(1, 6))
    story.append(Paragraph(b["name"], h2_style))
    info_rows = [
        ["Familie", b["family"]],
        ["Pflanzen 2026", b["plants"]],
        ["Tipp", b["tipp"]],
        ["Danach", b["next"]],
    ]
    tbl = Table(
        [[Paragraph(k, ParagraphStyle("bk", parent=body_style, fontName="Helvetica-Bold", textColor=FOREST, fontSize=9.5)),
          Paragraph(v, ParagraphStyle("bv", parent=body_style, fontSize=9.5))] for k, v in info_rows],
        colWidths=[3*cm, 13.5*cm]
    )
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, LIGHT),
    ]))
    story.append(tbl)

story.append(PageBreak())

# ============= TOMATEN =============
story.append(Paragraph("Der Tomatenbereich", h1_style))
story.append(Paragraph(
    "<b>12 Einzelbeete &agrave; 90 &times; 35 cm</b> an der Ost-Hausfassade unter Vordach &mdash; "
    "regengesch&uuml;tzt, morgensonnig, die <b>Prunk-Zone</b> des Gartens. "
    "Unter jeder Tomate w&auml;chst Basilikum (verbessert Geschmack, wehrt weisse Fliege ab).",
    body_style
))

tom_data = [
    ["Beet", "Pflanze", "Anzahl"],
    ["1-5", "Fleischtomate Tschernij", "10 Pflanzen (je 2)"],
    ["6", "Cherry Sweetie", "2 Pflanzen"],
    ["7-9", "Cocktail Black", "6 Pflanzen (je 2)"],
    ["10", "Cocktail Black", "1 Pflanze"],
    ["11-12", "Peperoni", "4 Pflanzen (je 2)"],
]
tom_tbl = Table(
    [[Paragraph(cell, ParagraphStyle(
        "tt", parent=body_style,
        fontName="Helvetica-Bold" if i == 0 else "Helvetica",
        textColor=colors.white if i == 0 else colors.HexColor("#333333"),
        fontSize=10.5
    )) for cell in row] for i, row in enumerate(tom_data)],
    colWidths=[2.5*cm, 7*cm, 7*cm]
)
tom_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), TOMATO),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CREAM, colors.white]),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
]))
story.append(tom_tbl)

story.append(Paragraph("Pflege-Fahrplan 2026", h2_style))
care_data = [
    ["Zeitpunkt", "Ma&szlig;nahme"],
    ["April", "Kompost einarbeiten, Vlies bereitlegen"],
    ["Anfang Mai", "1 Woche abh&auml;rten (tags&uuml;ber raus, nachts rein)"],
    ["19.-25. Mai", "Auspflanzen <b>nach den Eisheiligen</b>"],
    ["Juni", "Mulch (Stroh/Rasenschnitt) aufbringen"],
    ["W&ouml;chentlich", "Brennnesseljauche &middot; Ausgeizen &middot; Aufbinden"],
    ["Juli-Sept", "Ernte (angestrebt: 48-77 kg Tomaten)"],
    ["Okt", "Gr&uuml;nd&uuml;ngung (Roggen/Wicke) f&uuml;r den Winter"],
]
care_tbl = Table(
    [[Paragraph(cell, ParagraphStyle(
        "ct", parent=body_style,
        fontName="Helvetica-Bold" if i == 0 else "Helvetica",
        textColor=colors.white if i == 0 else colors.HexColor("#333333"),
        fontSize=10
    )) for cell in row] for i, row in enumerate(care_data)],
    colWidths=[4*cm, 12.5*cm]
)
care_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), FOREST),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CREAM, colors.white]),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
]))
story.append(care_tbl)

story.append(PageBreak())

# ============= DAUERKULTUREN =============
story.append(Paragraph("Die Dauerkulturen", h1_style))
story.append(Paragraph(
    "Nebst den rotierten Beeten wachsen auf dem Grundst&uuml;ck mehrere "
    "<b>mehrj&auml;hrige Pflanzen und Obstgeh&ouml;lze</b>, die zum Jahreszyklus geh&ouml;ren.",
    body_style
))

dauer_data = [
    ["Pflanze", "Ernte / Nutzen", "Saison"],
    ["B&auml;rlauch", "Frische Bl&auml;tter, Pesto", "M&auml;rz-April"],
    ["Kirschbaum", "Kirschen", "Juni-Juli"],
    ["Holderbaum", "Holunderbl&uuml;ten-Sirup, Beeren sp&auml;ter", "Mai-Juni / Aug-Sep"],
    ["3 Johannisbeerstauden", "Frische Beeren, Gelee, Likor", "Juli"],
    ["Zwetschgenbaum", "Zwetschgen, Kuchen, Einmachen", "August-September"],
    ["Apfelbaum", "&Auml;pfel, Mus, Saft, Lagerung", "September-Oktober"],
    ["Haselnussstrauch", "Haselnuss", "September-Oktober"],
    ["Brombeeren (Nachbarn)", "Frische Beeren, Konfit&uuml;re", "August-September"],
]
dauer_tbl = Table(
    [[Paragraph(cell, ParagraphStyle(
        "dt", parent=body_style,
        fontName="Helvetica-Bold" if i == 0 else "Helvetica",
        textColor=colors.white if i == 0 else colors.HexColor("#333333"),
        fontSize=10
    )) for cell in row] for i, row in enumerate(dauer_data)],
    colWidths=[5*cm, 6.5*cm, 5*cm]
)
dauer_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), EARTH),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CREAM, colors.white]),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
]))
story.append(dauer_tbl)

# ============= WHY =============
story.append(Paragraph("Warum das so?", h1_style))
story.append(Paragraph(
    "<b>Bodenleben:</b> Statt synthetischen D&uuml;ngern kommen Kompost, Mulch und Pflanzenjauchen zum Einsatz. "
    "Der Boden lebt &mdash; und bringt gesunde, widerstandsf&auml;hige Pflanzen hervor.",
    body_style
))
story.append(Paragraph(
    "<b>Mischkultur:</b> Tomaten + Basilikum. Karotten + Zwiebeln. Bohnen + Bohnenkraut. "
    "Gezielte Kombinationen, die sich gegenseitig st&auml;rken und Sch&auml;dlinge fernhalten.",
    body_style
))
story.append(Paragraph(
    "<b>Fruchtfolge:</b> Keine Pflanzenfamilie zwei Jahre auf demselben Beet. "
    "So bauen sich Krankheiten und Sch&auml;dlinge nicht auf und der Boden erholt sich.",
    body_style
))
story.append(Paragraph(
    "<b>Mondkalender:</b> Aussaat und Pflanzung nach Wurzel-, Blatt-, Frucht- und Bl&uuml;tentagen &mdash; "
    "subtile Einfl&uuml;sse, die sich &uuml;ber die Saison summieren.",
    body_style
))
story.append(Paragraph(
    "<b>Saisonverl&auml;ngerung:</b> Vorkultur unter Pflanzlampen ab M&auml;rz, "
    "Vlies &uuml;ber Junk-Kulturen, Nachsaat nach jeder Ernte &mdash; auf 920 m z&auml;hlt jeder Tag.",
    body_style
))

story.append(Spacer(1, 1*cm))
story.append(Paragraph(
    "&laquo;Gartenarbeit ist keine Last &mdash; es ist eine Sprache, in der die Welt zur&uuml;cksprechen kann.&raquo;",
    quote_style
))

# Build
doc.build(story)
print(f"PDF erstellt: {OUT}")
