# -*- coding: utf-8 -*-
"""Baut mentee-fertige .docx-Downloads aus den Bonus-Vorlagen (für ThriveCart / Google Drive)."""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = r"C:\Users\pnulm\Desktop\Mein Business\outputs\produkte\mama-ceo\bonus-vorlagen-saeule-4\_downloads"
os.makedirs(OUT, exist_ok=True)

PETROL = RGBColor(0x12, 0x82, 0x8C)
NAVY   = RGBColor(0x1A, 0x3A, 0x4A)
BODY   = RGBColor(0x2C, 0x3E, 0x50)
MUTED  = RGBColor(0x7A, 0x8A, 0x95)

def shade(p, hexfill):
    pPr = p._p.get_or_add_pPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), hexfill)
    pPr.append(sh)

def h1(doc, text, eyebrow=None):
    if eyebrow:
        p = doc.add_paragraph(); r = p.add_run(eyebrow.upper())
        r.font.name = "Calibri"; r.font.size = Pt(10); r.font.bold = True; r.font.color.rgb = PETROL
    p = doc.add_paragraph(); r = p.add_run(text)
    r.font.name = "Georgia"; r.font.size = Pt(22); r.font.bold = True; r.font.color.rgb = NAVY
    p.space_after = Pt(6)

def h2(doc, text):
    p = doc.add_paragraph(); r = p.add_run(text)
    r.font.name = "Calibri"; r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = PETROL
    p.paragraph_format.space_before = Pt(14); p.paragraph_format.space_after = Pt(4)

def body(doc, text, italic=False):
    p = doc.add_paragraph(); r = p.add_run(text)
    r.font.name = "Calibri"; r.font.size = Pt(11); r.font.italic = italic; r.font.color.rgb = BODY
    p.paragraph_format.space_after = Pt(6)
    return p

def step(doc, text):
    p = doc.add_paragraph(text, style=None)
    p.style = doc.styles['List Number']
    for r in p.runs: r.font.name="Calibri"; r.font.size=Pt(11); r.font.color.rgb=BODY
    return p

def bullet(doc, text):
    p = doc.add_paragraph(text, style='List Bullet')
    for r in p.runs: r.font.name="Calibri"; r.font.size=Pt(11); r.font.color.rgb=BODY
    return p

def codebox(doc, lines):
    """Kopier-Block: monospace, hellgrau hinterlegt, als EIN Absatz mit Zeilenumbrüchen."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.1); p.paragraph_format.right_indent = Inches(0.1)
    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(6)
    shade(p, "F4F1E8")
    for i, ln in enumerate(lines):
        r = p.add_run(ln)
        r.font.name = "Consolas"; r.font.size = Pt(10); r.font.color.rgb = BODY
        if i < len(lines)-1:
            r.add_break()

def footer(doc):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(18)
    r = p.add_run("Mama-CEO · Säule 4 · Mum Life Balance — Patricia Ulmann · mumlifebalance.ch")
    r.font.name="Calibri"; r.font.size=Pt(8); r.font.color.rgb=MUTED

# ===================== DOC 1: Cockpit-Bot-Vorlage =====================
COCKPIT = [
 "ROLLE",
 "Du bist mein persönlicher Cockpit-Bot — mein Morgenbriefing-Assistent.",
 "Dein Job ist, mir jeden Morgen in 30 Sekunden Klarheit zu geben, was heute dran ist.",
 "",
 "MEIN KONTEXT",
 "[Hier füge ich meinen Business-Brief aus Lektion 4.3 ein.]",
 "",
 "WAS DU BEKOMMST",
 "Du bist mit meinem Notion verbunden und liest meine aktuelle Woche",
 "(Wochenfokus, Tagesplaner, Aufgaben, Ziele). Wenn etwas fehlt, frag kurz nach, statt zu raten.",
 "",
 "WAS DU TUST, wenn ich „Was ist heute dran?\" frage:",
 "1. Nenne mir meinen TAGESFOKUS in einem Satz.",
 "2. Liste meine 3 WICHTIGSTEN AUFGABEN heute (Money-Making + Termine zuerst).",
 "3. Gib mir einen kurzen WOCHENBLICK (1-2 Sätze: wo stehe ich, was kommt noch).",
 "4. Schliesse mit EINEM motivierenden, ehrlichen Satz — kein Kitsch.",
 "",
 "REGELN",
 "- Halte dich kurz und konkret, keine Romane.",
 "- Sprich mich mit DU an, warm und direkt, wie eine gute Freundin.",
 "- Erfinde keine Termine oder Zahlen — nur was in meinem Notion steht.",
 "- Wenn ein Tag voll ist, hilf mir priorisieren, statt alles gleich wichtig zu machen.",
 "- [Meine Tabus aus dem Business-Brief gelten auch hier.]",
]

def build_cockpit():
    doc = Document()
    h1(doc, "🌅 Dein Cockpit-Bot — dein Business-Morgenbriefing", "Bonus · Säule 4 · Lektion 4.4")
    body(doc, "Deine fertige Vorlage. Du fügst sie in Claude Cowork ein (Stufe 1, kein Code) — oder später in Claude Code (Stufe 2, automatisch). Du schreibst nichts selbst, du füllst nur zwei Klammern aus.")
    h2(doc, "So setzt du ihn ein (Stufe 1 · Claude Cowork)")
    step(doc, "Claude Cowork (Desktop-App) öffnen → Einstellungen → Notion-Connector einstecken (einmal bei Notion einloggen, deine Planungs-Seiten freigeben).")
    step(doc, "Neuen Bot/Aufgabe anlegen → den System-Prompt unten einfügen.")
    step(doc, "Bei [ … ] deinen Business-Brief aus Lektion 4.3 eintragen.")
    step(doc, "Testen: „Was ist heute mein Fokus?\"")
    body(doc, "Stufe 0 ohne Bot: einfach in Notion die Ansicht „Diese Woche\" öffnen.")
    h2(doc, "👇 Das hier kopierst du in deinen Bot")
    codebox(doc, COCKPIT)
    h2(doc, "💡 Dieser Prompt bleibt derselbe — auch für Stufe 2")
    body(doc, "Wenn du später auf Claude Code + Telegram-Bot wechselst, schreibst du nichts neu. Du nimmst genau diesen Prompt mit — er ist das „Gehirn\" deines Bots. Claude Code baut nur die Hülle drumherum (Telegram, automatischer Versand morgens, Hosting).")
    body(doc, "Der Prompt ist das Rezept. Cowork ist der Herd zu Hause (du stehst dabei), Claude Code mit Telegram ist die Lieferung an die Haustür (kommt von selbst). Gleiches Rezept — nur ein anderer Weg, wie's zu dir kommt.", italic=True)
    footer(doc)
    path = os.path.join(OUT, "Cockpit-Bot-Vorlage.docx")
    doc.save(path); print("saved", path)

# ===================== DOC 2: Claude Code aktivieren =====================
def build_claudecode():
    doc = Document()
    h1(doc, "⚙️ Claude Code aktivieren — so legst du los", "Bonus · Säule 4 · Stufe 2 (für die Mutigen)")
    body(doc, "Das ist die Profi-Stufe — nur für dich, wenn du einen Bot willst, der von selbst läuft und dir morgens aufs Handy schreibt (auch wenn dein Laptop zu ist). Für die meisten reicht Cowork (Stufe 1) völlig. Wenn du neugierig bist: hier der ehrliche Überblick.")
    h2(doc, "Was Claude Code ist")
    body(doc, "Eine Werkzeug-Umgebung, in der du echte, automatische Bots bauen lässt — z.B. einen Telegram-Bot, der jeden Morgen dein Briefing schickt. Du programmierst nicht selbst: du sagst Claude Code in normaler Sprache, was du willst, und es baut + erklärt dir alles Schritt für Schritt.")
    h2(doc, "💡 Du fängst NICHT bei null an")
    body(doc, "Den Bot-Prompt hast du schon — den Cockpit-Prompt (bzw. den Haushalts-Prompt). Den nimmst du 1:1 mit, du schreibst nichts Neues. Claude Code baut nur die Hülle: Telegram-Verbindung, automatischer Versand am Morgen und Hosting.")
    h2(doc, "Was du dafür brauchst")
    bullet(doc, "Ein Claude-Abo")
    bullet(doc, "Etwas Zeit + die Bereitschaft, ein paar Dinge einmal einzurichten (du arbeitest in einem Fenster mit Texteingabe, dem „Terminal\" — klingt schlimmer als es ist)")
    bullet(doc, "Einen Telegram-Bot (kostenlos über @BotFather in Telegram angemeldet)")
    bullet(doc, "Einen Ort, wo der Bot rund um die Uhr läuft („Hosting\", z.B. Railway) — ~5 CHF/Monat")
    bullet(doc, "Dazu ein paar Franken KI-Kosten je nach Nutzung")
    h2(doc, "So aktivierst du Claude Code (Schritt für Schritt)")
    step(doc, "Claude Code installieren — die aktuelle Anleitung findest du auf claude.ai/code (bzw. in der Claude-Hilfe). Folge der Installation für dein System.")
    step(doc, "Claude Code öffnen und ihm einfach sagen: „Ich möchte einen Telegram-Bot, der morgens um 6:30 meine Notion-Wochenplanung liest und mir ein Briefing schickt. Führ mich Schritt für Schritt durch alles.\"")
    step(doc, "Claude Code fragt nach, was es braucht (Tokens, Zugänge) und richtet den Rest mit dir ein.")
    step(doc, "Zum Dauerbetrieb hilft dir Claude Code beim Hochladen auf ein Hosting (z.B. Railway).")
    h2(doc, "Ehrlich gesagt")
    bullet(doc, "Das ist mehr Aufwand als Cowork und braucht etwas Geduld beim ersten Mal.")
    bullet(doc, "Es ist kein Muss — dein Bot in Cowork (Stufe 1) trägt dich sehr weit.")
    bullet(doc, "Wenn du's angehen willst: bring deine Fragen in den Live-Call 3 (Bot-Bau-Werkstatt) — da machen wir's gemeinsam.")
    body(doc, "Faustregel: Cowork = du fragst, wenn du am Computer bist. Claude Code = der Bot kommt von selbst aufs Handy. Wähl nach deinem Bedürfnis, nicht nach Ehrgeiz.", italic=True)
    footer(doc)
    path = os.path.join(OUT, "Claude-Code-aktivieren-Anleitung.docx")
    doc.save(path); print("saved", path)

# ===================== DOC 3: Haushalts-Helfer-Vorlage =====================
HAUSHALT = [
 "ROLLE",
 "Du bist mein persönlicher Haushalts-Helfer — der Zwilling meines Cockpit-Bots,",
 "nur für zu Hause. Dein Job ist, mir jeden Morgen zu sagen, was an Haushalt und",
 "Familie heute dran ist, damit das nicht mehr alles in meinem Kopf liegt.",
 "",
 "MEIN KONTEXT",
 "Wir sind eine Familie mit [Anzahl] Kindern.",
 "Besonderheiten der Woche: [z.B. Mann Mo-Do auswärts, Mittwoch alle zu Hause].",
 "",
 "WAS DU BEKOMMST",
 "Du liest meine Notion-Haushalts-Liste. Darin stehen 4 Sorten Einträge:",
 "- WIEDERKEHREND mit Rhythmus + Wochentag (z.B. „Wäsche – wöchentlich\", „Müll – Mi\")",
 "- DATIERT mit festem Datum (z.B. „Frühlingskleider raussuchen – letzter Freitag im März\")",
 "- FAMILIEN-TERMINE / GEBURTSTAGE mit Datum (Geschenk ~10-14 Tage vorher erinnern)",
 "- SCHULE (Vorabend!) — Schwimmen/Turnen/Waldtag: am Abend VOR dem Datum erinnern",
 "Wenn etwas fehlt, frag kurz nach, statt zu raten.",
 "",
 "WAS DU TUST, wenn ich „Was ist heute zu Hause dran?\" frage:",
 "1. WIEDERKEHREND HEUTE: täglich + „wöchentlich\" deren Wochentag = heute. Monatlich/quartalsweise nur einmal pro Periode dezent anstossen.",
 "2. TERMINE & DATEN: alles mit Datum heute oder in den nächsten Tagen. Datumsregeln („letzter Freitag im März\") korrekt ausrechnen.",
 "3. SCHULE: am Vorabend ansagen („morgen Schwimmen für [Kind] — Sachen packen\"). Immer den Vornamen nennen.",
 "4. WER: „Wer = Kinder\" → „erinnere die Kinder an …\" · „Mann\" → „Mann: …\" · „Patricia/ich\" → meine Aufgabe.",
 "5. FORMAT: kurze Tagesliste, gruppiert: 🏠 Haushalt · 👨‍👩‍👧 Familie/Termine · 🎒 Schule (für morgen) · 🧒 Kinder-Ämtli · 🧘 Mein Slot.",
 "",
 "REGELN",
 "- Kurz und konkret, keine Romane. Sprich mich mit DU an, warm und alltagsnah.",
 "- Erfinde keine Aufgaben oder Termine — nur was in meiner Liste steht.",
 "- Me-Time-Slots erinnern, aber als Schutz, nie mit Druck/schlechtem Gewissen.",
 "- Wenn heute nichts ansteht, sag das ehrlich und gönn mir die Pause.",
]

def build_haushalt():
    doc = Document()
    h1(doc, "🏠 Dein Haushalts-Helfer — Mental Load raus aus dem Kopf", "Bonus · Säule 4 · Lektion 4.5 MASTERY")
    body(doc, "Deine fertige Vorlage. Du fügst sie in Claude Cowork ein (Stufe 1, kein Code). Der Bot liest deine Notion-Haushalts-Liste und sagt dir morgens, was zu Hause + für die Kinder ansteht.")
    h2(doc, "So setzt du ihn ein (Stufe 1 · Claude Cowork)")
    step(doc, "Deine Haushalts-Liste in Notion muss stehen (aus Lektion 4.5 — wiederkehrend, datiert, Familien-Termine).")
    step(doc, "In Claude Cowork ist dein Notion schon verbunden (vom Cockpit-Bot, Lektion 4.4).")
    step(doc, "Neuen Bot anlegen → System-Prompt unten einfügen → bei [ … ] deine Familie eintragen.")
    step(doc, "Testen: „Was ist heute zu Hause dran?\"")
    body(doc, "Stufe 0 ohne Bot: Notion-Ansicht „Kommende Termine\" + „nach Wochentag\" öffnen.")
    h2(doc, "👇 Das hier kopierst du in deinen Bot")
    codebox(doc, HAUSHALT)
    h2(doc, "💡 Gleiche Mechanik wie der Cockpit-Bot")
    body(doc, "Das ist exakt derselbe Weg wie beim Cockpit-Bot — nur eine andere Liste (Haushalt statt Business) und eine andere Vorlage. Und auch hier gilt: später als automatischer Telegram-Bot via Claude Code möglich, gleicher Prompt, kein Muss.")
    footer(doc)
    path = os.path.join(OUT, "Haushalts-Helfer-Vorlage.docx")
    doc.save(path); print("saved", path)

# ===================== DOC 4: Kochassistent =====================
KOCH = [
 "ROLLE",
 "Du bist mein persönlicher Kochassistent.",
 "Dein Job ist, mir das tägliche „was koch ich heute\" abzunehmen — mit Wochenplänen,",
 "Spontan-Ideen aus dem was da ist, und sortierten Einkaufslisten.",
 "",
 "MEINE FAMILIE (Kontext)",
 "Wir sind [Anzahl] Personen, davon [Anzahl] Kinder.",
 "Wir essen gern: [Lieblingsessen / Stil, z.B. proteinreich, frisch].",
 "Kommt NIE auf den Tisch: [no-gos / Allergien].",
 "Besonderheiten: [z.B. eigenes Brot, schnelle Gerichte unter der Woche].",
 "",
 "DEINE 3 AUFGABEN",
 "1. WOCHENPLAN: Wenn ich frage, gib mir einen Plan (Mittag/Abend nach Wunsch),",
 "   passend zu meiner Familie und meinem Stil.",
 "2. SPONTAN-KOCH: Wenn ich dir Zutaten nenne, schlag mir 1-2 konkrete Gerichte vor —",
 "   mit Mengen für meine Personenzahl.",
 "3. EINKAUFSLISTE: Auf Wunsch gib mir die Liste zum Plan, sortiert nach",
 "   Kategorien (Gemüse, Milchprodukte, …) oder nach Laden.",
 "",
 "REGELN",
 "- Frag nach, wenn dir Infos fehlen (z.B. wie viele Tage, Mittag oder Abend).",
 "- Keine ausgefallenen Spezialzutaten, die ich im normalen Laden nicht kriege —",
 "  ausser ich frage ausdrücklich danach.",
 "- Wenn ich sage „das mögen wir nicht\", merk es dir für nächste Vorschläge.",
 "- Sprich mich mit DU an, locker und alltagsnah.",
]

def build_koch():
    doc = Document()
    h1(doc, "🍳 Dein Kochassistent — Schluss mit „was koch ich heute\"", "Extra-Bonus · Säule 4 · Lektion 4.5")
    body(doc, "Gleiche Mechanik wie deine anderen Bots — du fügst die Vorlage in Claude Cowork ein und gibst deine Familie als Kontext.")
    h2(doc, "So setzt du ihn ein")
    step(doc, "In Claude Cowork neuen Bot anlegen → System-Prompt unten einfügen.")
    step(doc, "Bei [ … ] deine Familie eintragen (wie viele, was ihr mögt, was nie auf den Tisch kommt).")
    step(doc, "Loslegen: „Ich hab [Zutaten] — was koch ich?\" oder „Wochenplan für 5 Tage\".")
    h2(doc, "👇 Das hier kopierst du in deinen Bot")
    codebox(doc, KOCH)
    footer(doc)
    path = os.path.join(OUT, "Kochassistent-Vorlage.docx")
    doc.save(path); print("saved", path)

for fn in (build_cockpit, build_claudecode, build_haushalt, build_koch):
    try:
        fn()
    except PermissionError as e:
        print("SKIP (Datei offen in Word?):", e.filename)
print("ALL DONE")
