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

build_cockpit()
build_claudecode()
print("ALL DONE")
