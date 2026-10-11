#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bringt die vier SKILL.md der Salespage-Designs auf Patricias Regeln.

Die Vorlagen sind für einen allgemeinen deutschen Markt geschrieben. Vier
Stellen widersprechen dem, was in diesem Arbeitsbereich verbindlich gilt:

  1. Anrede    Vorlage: „Kunden statt Kundinnen, generisches Maskulinum"
               Patricia schreibt Kundinnen — ihre Leute sind Mamas.
  2. Beweise   Vorlage: fehlende Zahlen mit „plausiblen Beispielen" fuellen
               Patricia: keine erfundenen Zahlen, nie. Auch nicht als Platzhalter
               mit Kommentar — im Layout steht dann trotzdem eine Zahl, die
               jemand versehentlich live schaltet.
  3. Garantie  Vorlage: Garantie/Widerruf optional einbaubar
               Patricia: keine Geld-zurück-Garantie auf digitale Produkte.
  4. ss/ss     Vorlage: deutsches Eszett. Patricia schreibt Schweizer ss.

Dazu kommt ein Kopfblock, der auf ihre echten Quellen zeigt statt auf die
leeren Vorlagen BRAND-VOICE.md / ZIELGRUPPE.md.

Aufruf (aus dem Projekt-Stammverzeichnis):

    python scripts/salespage-design/regeln-anpassen.py

Wiederholbar: Quelle ist immer reference/salespage-designs-original/.
"""

import re
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
ORIGINAL = WURZEL / "reference" / "salespage-designs-original"
ZIEL = WURZEL / ".claude" / "skills"
VORLAGEN = Path(__file__).resolve().parent / "vorlagen"

DESIGNS = [
    "minikurs-salespage",
    "signature-kurs-salespage",
    "skill-salespage",
    "ki-salespage",
]

# Was im Kopf jeder Datei steht, bevor irgendetwas gebaut wird.
KOPF = """
---

## 🚨 Patricia-Vorrang (gilt über allem, was weiter unten steht)

Dieses Design kam als allgemeine Vorlage. Vier Regeln darin widersprechen dem,
was hier verbindlich gilt. **Bei jedem Widerspruch gewinnt dieser Block.**

### Pflicht-Lese vor dem ersten Satz
- `context/patricia-vollprofil.md` — Stimme, Werte, Geschichte, Beweis-Linien. Ohne diese Lese nicht bauen.
- `context/brand-voice.md` — Tonalität, Verbote, Kernbotschaft
- `context/business-info.md` — die zwei Profile (Mentoring vs. doTERRA)
- `context/kern-painpoint.md` — „viel rein, wenig raus" + die drei Bedingungen
- `context/link-uebersicht.md` — echte Checkout- und Angebots-Links (nie raten)
- `context/active-funnels.json` — was gerade läuft
- Bei doTERRA zusätzlich: `context/doterra/patricia-wendepunkt-story.md` + die Compliance-Regeln

Die Dateien `BRAND-VOICE.md` und `ZIELGRUPPE.md` in diesem Ordner sind nur Wegweiser
auf die Quellen oben — der Inhalt steht in `context/`, nicht hier.

### 1. Anrede: Kundinnen, nicht Kunden
Patricias Leute sind Mamas. Es heisst **Kundinnen, Teilnehmerinnen, Mentees** —
nicht das generische Maskulinum. Die Regel weiter unten („Kunden statt Kundinnen,
vor Abgabe auf -innen scannen") ist hier **ungültig**.

**Ausnahme:** Wenn es um die Kundschaft *ihrer* Kundinnen geht, ist die Zielgruppe
nicht zwingend weiblich oder Mama — dort „Person", „Interessent", „Leute".

### 2. Keine erfundenen Zahlen, keine erfundenen Stimmen
Die Vollständigkeits-Regel weiter unten erlaubt, fehlende Zahlen und Testimonials
mit „plausiblen Beispielen" zu füllen. **Das gilt hier nicht.** Eine erfundene Zahl,
die als Platzhalter im Layout steht, geht irgendwann live.

Stattdessen:
- Zahlen ausschliesslich aus `context/patricia-expertise.md`, `context/patricia-vollprofil.md`
  oder aus dem, was Patricia im Auftrag nennt.
- Fehlt eine Zahl: **den Satz ohne Zahl formulieren** („mehrere Mamas", „seit über
  einem Jahr") statt eine zu erfinden.
- Fehlt eine Kundenstimme: die Sektion weglassen oder eine sichtbar leere Karte mit
  `<!-- HIER ECHTE STIMME EINSETZEN -->` — nie einen erfundenen Namen.
- Beim Ausliefern jede Stelle benennen, an der eine Angabe fehlt.

Ein ehrlich leerer Block schlägt einen schön erfundenen.

### 3. Keine Geld-zurück-Garantie
Auf digitale Produkte gibt Patricia **keine Garantie** — das Produkt lässt sich
kopieren. Die Garantie-/Widerrufs-Sektion bleibt draussen, auch wenn die Vorlage
sie als Option anbietet. Das gesetzliche Widerrufsrecht regelt der Zahlungsanbieter,
darüber wird auf der Seite nichts versprochen.

### 4. Schweizer ss und echte Umlaute
Durchgehend **ss** statt ß (dass, heisst, Strasse, weisst, gross).
Und echte Umlaute — ä, ö, ü — nie als ae/oe/ue geschrieben.

### 5. Was sonst noch gilt
- **Kein Stakkato.** Nie drei abgehackte Mini-Sätze hintereinander — mit „und",
  „weil", „aber", „bis" verbinden. Gilt auch für Überschriften. Ausnahme:
  ausdrückliche Aufzählungen („Was du bekommst").
- **Freundin-Ton.** Geschrieben wie am Küchentisch zu einer Mama-Freundin, auch
  auf einer Verkaufsseite.
- **Keine fremden Namen.** Mentorinnen, Kurse und Programme Dritter kommen in
  keinem Kundendokument vor. Vor der Abgabe danach suchen.
- **Design ist gesetzt.** Farben und Schriften stehen in `BRAND-CONFIG.md` und in
  der Vorlage. Keine neuen Farben, kein Gold, kein Pink, kein Gelb.
- **Sicht-Prüfung vor der Abgabe** (CLAUDE.md): rendern, anschauen, prüfen —
  bricht keine Überschrift unschön um, verdeckt kein Text-Kasten ein Gesicht,
  wechseln die Sektionsfarben, trägt jede Schrift genug Kontrast?

---
"""

# --- Textersetzungen, die in allen vier Dateien greifen ----------------------

GENDER = re.compile(
    r"[-*] +\*?\*?[\"„]?Kunden[\"“]? *statt.*?-innen scannen\.",
    re.DOTALL,
)
GENDER_NEU = (
    "- **„Kundinnen\" statt „Kunden\"** — Patricias Leute sind Mamas, also die\n"
    "  weibliche Form (Kundinnen, Teilnehmerinnen, Leserinnen). Kein Doppelpunkt-Gendern\n"
    "  (Kund:innen), kein Sternchen. Geht es um die Kundschaft *ihrer* Kundinnen:\n"
    "  neutral bleiben („Person\", „Interessent\", „Leute\")."
)

ERFINDEN = re.compile(
    r"[-*] +(?:Liegen keine vor|Sonst mit).*?(?=\n[-*] |\n\n|\n#)",
    re.DOTALL,
)
ERFINDEN_NEU = (
    "- Liegen keine vor: **nichts erfinden.** Den Satz ohne Zahl formulieren, die\n"
    "  Sektion weglassen oder eine sichtbar leere Karte mit\n"
    "  `<!-- HIER ECHTE ANGABE EINSETZEN -->` stehen lassen — nie eine plausible\n"
    "  Zahl und nie eine erfundene Kundenstimme mit Namen.\n"
)

GUARDRAIL = re.compile(
    r"[-*] +\*\*Guardrail:\*\*.*?(?=\n[-*] |\n\n|\n#)",
    re.DOTALL,
)
GUARDRAIL_NEU = (
    "- **Kontrolle beim Ausliefern:** jede Stelle benennen, an der eine echte Angabe\n"
    "  fehlt — damit Patricia sie nachträgt, bevor die Seite live geht.\n"
)

GARANTIE_ZEILE = re.compile(
    r"[-*] +\*?\*?Garantie/Widerruf.*?(?=\n[-*] |\n\n|\n#)",
    re.DOTALL,
)
GARANTIE_NEU = (
    "- **Garantie/Widerruf: bleibt draussen.** Auf digitale Produkte gibt Patricia\n"
    "  keine Geld-zurück-Garantie. Die Sektion nicht einbauen.\n"
)

GARANTIE_ABSCHNITT = re.compile(
    r"## Garantie \(optional\).*?(?=\n## )",
    re.DOTALL,
)
GARANTIE_ABSCHNITT_NEU = (
    "## Garantie — bleibt draussen\n"
    "Die Vorlage kennt eine Garantie-/Widerrufs-Sektion (`.guar`). **Sie wird nicht\n"
    "gebaut.** Auf digitale Produkte gibt Patricia keine Geld-zurück-Garantie, weil\n"
    "sich das Produkt kopieren lässt. Das gesetzliche Widerrufsrecht regelt der\n"
    "Zahlungsanbieter — auf der Seite steht dazu nichts.\n\n"
)

# Die Design-Beschreibungen nennen noch die Farben der Vorlage. Sie muessen
# beschreiben, was nach marke-anpassen.py tatsaechlich in der reference-page steht —
# sonst baut Claude nach der Beschreibung statt nach der Datei.
# Diese Ersetzungen laufen NACH der ss-Umschrift, deshalb hier „gross" statt „groß".
DESIGN_TEXTE = {
    "signature-kurs-salespage": [
        (
            "Design-System — Cream/Blush/Pink/Gold, viel",
            "Design-System — Creme/Petrol/Orange, viel",
        ),
        (
            "- **Farben:** Cream `#fbf4ef` / Cream2 `#f6e9e1` / Blush `#fbe7ec` / Weiss `#ffffff` (helle Sektionen) ·\n"
            "  Ink `#2a1620` (Text; **und** eine dunkle Sektion `.bg-ink` als Kontrast-Break) · Gold `#bd8f3f`\n"
            "  (Eyebrows, Wert-Anker) · Pink `#ff3f86` / Pink-deep `#d21e66` (CTA + Akzent)\n"
            "- **Akzent-Ton (variabel!):** das Pink `--pink` darf pro Kurs leicht wechseln (Standard `#ff3f86`).\n"
            "  Andere passende Töne: `#f5356f`, `#e83a7a`, `#ff4d78`. **Cream, Blush, Weiss und Gold bleiben immer\n"
            "  gleich** — nur das Pink/der Akzent darf sich verschieben. Der Blush-Grundton `--blush` darf minimal\n"
            "  mitwandern.",
            "- **Farben:** Creme `#f1ecdd` / Creme2 `#e7e0cd` / zartes Petrol `#dfe9e8` / Weiss `#ffffff`\n"
            "  (helle Sektionen) · Text `#0c1c30` (**und** die dunkle Sektion `.bg-ink` als Kontrast-Break) ·\n"
            "  Petrol `#12828c` (Eyebrows, Wert-Anker) · Orange `#dc822e` / Orange-tief `#b4661f` (CTA + Akzent)\n"
            "- **Die Farben sind gesetzt.** Anders als in der Ursprungs-Vorlage wird hier **kein** Akzent-Ton\n"
            "  pro Kurs verschoben — Patricias Marke kennt genau vier Farben, und die stehen oben. Kein Gold,\n"
            "  kein Pink, kein Gelb. Variiert wird über Anordnung, Grösse und Bildanteil, nicht über Farbe.",
        ),
        (
            "- **CTA:** Pink-Button, `.btn` / `.btn-lg` (gross) / `.btn-outline` (Raten-Option). Immer Pink.",
            "- **CTA:** Orange-Button, `.btn` / `.btn-lg` (gross) / `.btn-outline` (Raten-Option). Immer Orange.",
        ),
        (
            "- **Akzent-Pink** leicht verschieben (Standard `#ff3f86`).",
            "- **Nicht die Farbe** verschieben — die ist gesetzt. Stattdessen den Bildanteil ändern:\n"
            "  mal ein Parallax-Band mehr, mal eine ruhige Creme-Strecke.",
        ),
    ],
    "skill-salespage": [
        (
            "Neon-Design — schwarzer Hintergrund, Neon-Gradient, Archivo + Playfair-Italic + Space Mono +\n"
            "  Inter,",
            "Design — Dunkelblau-Grund, leuchtendes Petrol, Philosopher + Space Mono +\n"
            "  Source Sans 3,",
        ),
        (
            "- **Basis dunkel:** `--bg:#09090f` · `--bg2:#0f0f18` · `--card:#15151f` · `--card2:#1c1c28` ·\n"
            "  `--line:rgba(255,255,255,.09)` · Text `--ink:#f5eef2` / `--muted:#a9a2ae`.\n"
            "- **Neon-Akzent (variabel!):** Standard Pink `--pink:#ff3d8b` / `--pink-2:#ff74ad` /\n"
            "  `--pink-deep:#c2185b` + Gradient `--grad:linear-gradient(100deg,#ff2e86,#ff5fa2,#ff9ecb)`.\n"
            "  Der **Akzent-Hue darf pro Skill wechseln** — z.B. Violett (`#a63bff`), Cyan (`#41e7ff`) oder ein\n"
            "  anderes Pink. **Die dunkle Basis bleibt immer** — nur der Neon-Ton verschiebt sich (Gradient +\n"
            "  Glow + Akzentfarben mitziehen).",
            "- **Basis dunkelblau:** `--bg:#0c1c30` · `--bg2:#12283d` · `--card:#17324a` · `--card2:#1d3d58` ·\n"
            "  `--line:rgba(255,255,255,.09)` · Text `--ink:#f1ecdd` / `--muted:#9aa8b3`.\n"
            "- **Petrol leuchtet:** `--pink:#2ba7b3` / `--pink-2:#6fd0d6` / `--pink-deep:#12828c` + Verlauf\n"
            "  `--grad:linear-gradient(100deg,#0d626a,#12828c,#17949f)`. (Die Variablen heissen historisch\n"
            "  noch `--pink` — der Wert ist Petrol.) **Die Farben sind gesetzt**, anders als in der\n"
            "  Ursprungs-Vorlage wird der Akzent nicht pro Produkt verschoben. Der Verlauf bleibt dunkel\n"
            "  genug, damit weisse Schrift auf dem Knopf trägt.",
        ),
        (
            "- **Neon-Akzent** leicht verschieben (Pink Standard; Violett/Cyan möglich).",
            "- **Nicht die Farbe** verschieben — stattdessen Kartendichte und Abschnittshöhe variieren.",
        ),
        (
            "die Archivo-Uppercase-Headline mit Playfair-Italic-Highlight",
            "die Philosopher-Uppercase-Headline mit kursivem Philosopher-Highlight",
        ),
    ],
    "ki-salespage": [
        (
            "futuristischen Neon-Design — Fast-Schwarz mit\n"
            "  Pink/Violett/Cyan-Triade, Anton + Orbitron + Montserrat,",
            "futuristischen Design — Dunkelblau mit\n"
            "  leuchtendem Orange und Petrol, Philosopher + Source Sans 3,",
        ),
        (
            "## Design (fest — nur die Neon-Gewichtung variiert)",
            "## Design (fest — die Farben stehen, variiert wird die Anordnung)",
        ),
        (
            "- **Basis fast-schwarz:** `--bg:#08060f` · `--bg2:#0d0a18` · `--card:#150f22` ·\n"
            "  `--line:rgba(255,120,220,0.16)` · Text `--ink:#f3e9f4` / `--muted:#a99cb5`. Dezentes Grid- +\n"
            "  Glow-Backdrop im `body::before`.\n"
            "- **Neon-Triade (Gewichtung variabel!):** Pink `--neon:#ff2fb0` · Violett `--violet:#a63bff` ·\n"
            "  Cyan `--cyan:#41e7ff`. Gold-/Highlight-Gradient `--goldgrad:linear-gradient(90deg,#ff2fb0,#ff86e0,#c04bff)`,\n"
            "  CTA `--cta:linear-gradient(100deg,#7a1bd8,#c11bd0,#ff2fb0)`. Die **Gewichtung der Triade darf pro\n"
            "  Produkt wechseln** (mal pink-dominant, mal mehr violett oder cyan). **Die dunkle Basis + die drei\n"
            "  Neon-Töne bleiben** — nur ihr Mischverhältnis/Akzent verschiebt sich.",
            "- **Basis dunkelblau:** `--bg:#0c1c30` · `--bg2:#122a42` · `--card:#16324c` ·\n"
            "  `--line:rgba(220,130,46,0.20)` · Text `--ink:#f1ecdd` / `--muted:#9aa8b3`. Dezentes Grid- +\n"
            "  Glow-Backdrop im `body::before`.\n"
            "- **Orange leuchtet, Petrol stützt:** `--neon:#dc822e` · `--violet:#12828c` (Petrol) ·\n"
            "  `--cyan:#4fc9d1` (helles Petrol). Highlight-Verlauf\n"
            "  `--goldgrad:linear-gradient(90deg,#dc822e,#f0a45e,#f7c08f)` — bleibt bewusst warm, sonst\n"
            "  verschwindet das Ende der Überschrift im dunklen Grund. CTA\n"
            "  `--cta:linear-gradient(100deg,#b4661f,#dc822e,#f0a45e)` mit **dunkler** Schrift `#0c1c30`.\n"
            "  **Die Farben sind gesetzt** — variiert wird die Anordnung, nicht der Ton.",
        ),
        (
            "- **CTA:** Gradient-Button `.btn` (Violett→Magenta→Pink) mit Glow; `.btn.ghost` als Zweit-CTA.",
            "- **CTA:** Verlauf-Button `.btn` (Orange, dunkle Schrift) mit Glow; `.btn.ghost` als Zweit-CTA.",
        ),
        (
            "- **Neon-Gewichtung** verschieben (mal pink-, mal violett-, mal cyan-betont).",
            "- **Nicht die Farbe** verschieben — stattdessen Tools-Grid und Zahlenband anders gewichten.",
        ),
        (
            "Die Neon-Akzente (Karten-Ränder, Glows, Gold-Gradient-\nSpans)",
            "Die leuchtenden Akzente (Karten-Ränder, Glows, Orange-Verlauf-\nSpans)",
        ),
        (
            "die Anton-Uppercase-Headline mit Gold-Gradient-Highlight",
            "die Philosopher-Uppercase-Headline mit Orange-Verlauf-Highlight",
        ),
    ],
}

# Der Abschnitts-Katalog (references/section-guide.md) nennt die Farben im
# Klartext („Auf Pink", „Gold-Kreise"). Nach dem Umfaerben stimmt das nicht mehr.
# Laengere Begriffe zuerst, sonst frisst „Gold" das „Gold-Gradient" weg.
KATALOG_WOERTER = {
    "minikurs-salespage": [
        ("Gold-Fortschrittslinie", "Orange-Fortschrittslinie"),
        ("Gold-Kreise", "Orange-Kreise"),
        ("Gold- oder Beere-Band", "Orange- oder Petrol-Band"),
        ("Pink, Beere oder Weiß", "Petrol, Petrol-Ton 2 oder Weiss"),
        ("Beere", "Petrol-Ton 2"),
        ("Immer Gold", "Immer Orange"),
        ("(✓, Gold)", "(✓, Orange)"),
        ("Auf Pink", "Auf Petrol"),
        ("Hintergrund immer Pink", "Hintergrund immer Petrol"),
        ("Pink(", "Petrol("),
        ("Weiß", "Weiss"),
    ],
    "signature-kurs-salespage": [
        ("Cream", "Creme"),
        ("Blush", "zartes Petrol"),
        ("Pink-deep", "Orange-tief"),
        ("Pink", "Orange"),
        ("Gold", "Petrol"),
        ("Weiß", "Weiss"),
    ],
    "skill-salespage": [
        ("Neon-Karten-Look", "Petrol-Karten-Look"),
        ("Neon-Gradient", "Petrol-Verlauf"),
        ("Neon-Band", "Petrol-Band"),
        ("Neon-Glow", "Petrol-Glow"),
        ("Neon-Akzent", "Petrol-Akzent"),
        ("Neon-Ton", "Petrol-Ton"),
        ("Neon", "Petrol"),
        ("Archivo", "Philosopher"),
        ("Playfair", "Philosopher kursiv"),
        ("Inter", "Source Sans 3"),
        ("Weiß", "Weiss"),
    ],
    "ki-salespage": [
        ("Gold-Gradient-Highlight", "Orange-Verlauf-Highlight"),
        ("Gold-Gradient", "Orange-Verlauf"),
        ("Neon-Triade", "Orange + Petrol"),
        ("Neon-Karten-Look", "Orange-Karten-Look"),
        ("Neon-Band", "Orange-Band"),
        ("Neon-Glow", "Orange-Glow"),
        ("Neon", "leuchtend"),
        ("Anton-Uppercase-Headline", "Philosopher-Uppercase-Headline"),
        ("Anton-Headline", "Philosopher-Headline"),
        ("Anton-Zeile", "Philosopher-Zeile"),
        ("Anton", "Philosopher"),
        ("Orbitron-/Mono-Ton", "gesperrtes Source Sans 3"),
        ("Orbitron", "Source Sans 3"),
        ("Montserrat", "Source Sans 3"),
        ("Weiß", "Weiss"),
    ],
}

# Im Katalog stehen dieselben zwei Regeln wie im Bauplan — und muessen dieselbe
# Antwort bekommen, sonst widersprechen sich die zwei Dateien.
KATALOG_REGELN = [
    (
        re.compile(
            r"Echte bevorzugt, sonst Beispiel-Stimmen mit\s*\n?\s*Namen[^.]*\.",
            re.DOTALL,
        ),
        "Nur echte Stimmen. Liegt keine vor, faellt die Sektion weg — "
        "keine erfundenen Namen.",
    ),
    (
        re.compile(
            r"Wert-Angaben: echte nutzen, sonst plausible Beispiel-Werte einsetzen und den\s*\n?"
            r"Gegenwert daraus aufsummieren \(im Code als Platzhalter markieren\)\.",
            re.DOTALL,
        ),
        "Wert-Angaben: nur echte. Fehlt eine, bleibt die Zeile weg statt "
        "geschaetzt zu werden — und ohne echte Werte kein aufsummierter Gegenwert.",
    ),
    (
        re.compile(
            r"- \*\*Garantie\*\* — `\.guar`.*?(?=\n- \*\*)",
            re.DOTALL,
        ),
        "- **Garantie** — `.guar` (Siegel + Text). **Wird nicht gebaut.** Auf digitale\n"
        "  Produkte gibt Patricia keine Geld-zurueck-Garantie.\n",
    ),
    (
        re.compile(r"CTA, Garantie-Zeile\."),
        "CTA (ohne Garantie-Zeile — die gibt es hier nicht).",
    ),
    # Dieselbe Erlaubnis taucht im Katalog in mehreren Formulierungen auf.
    (
        re.compile(
            r"Echte Zahlen bevorzugt,\s*\n?\s*sonst plausible Beispielwerte\s*\n?\s*"
            r"\(als Platzhalter markieren\)\.",
            re.DOTALL,
        ),
        "Nur echte Zahlen. Fehlt eine, wird die Kachel weggelassen — "
        "keine geschaetzten Werte.",
    ),
    (
        re.compile(
            r"Echte Stimmen\s*\n?\s*bevorzugt; sonst Beispiel-Stimmen mit Namen\s*\n?\s*"
            r"\(als Platzhalter markieren\)\.",
            re.DOTALL,
        ),
        "Nur echte Stimmen. Liegt keine vor, faellt die Sektion weg — "
        "keine erfundenen Namen.",
    ),
    # Auffangnetz fuer jede weitere Formulierung derselben Erlaubnis.
    (
        re.compile(
            r"sonst (?:realistische|plausible) Beispielwerte[^.]*\.",
            re.DOTALL,
        ),
        "sonst gar keine Zahl — lieber eine Kachel weniger als eine erfundene.",
    ),
]

# Schriften und Farben, die in der Beschreibung noch aus der Vorlage stammen
SCHRIFT_TEXTE = [
    ("`Instrument Serif`", "`Philosopher`"),
    ("`Playfair Display`", "`Philosopher`"),
    ("`DM Sans`", "`Source Sans 3`"),
    ("`Caveat`", "`Philosopher` (kursiv)"),
    ("`Anton`", "`Philosopher`"),
    ("`Archivo`", "`Philosopher`"),
    ("`Montserrat`", "`Source Sans 3`"),
    ("`Orbitron`", "`Source Sans 3` (gesperrt)"),
    ("`Inter`", "`Source Sans 3`"),
    ("`Poppins`", "`Source Sans 3`"),
    ("Instrument-Serif-Headlines", "Philosopher-Headlines"),
]


def eszett_zu_ss(text: str) -> str:
    """Deutsches Eszett zu Schweizer ss — aber nicht in Code, Pfaden oder
    CSS-Klassen, die in Backticks stehen."""
    teile = re.split(r"(`[^`]*`)", text)
    for i, teil in enumerate(teile):
        if not teil.startswith("`"):
            teile[i] = teil.replace("ß", "ss").replace("ẞ", "SS")
    return "".join(teile)


def kopf_einsetzen(text: str) -> str:
    """Der Vorrang-Block kommt direkt nach dem YAML-Kopf und der H1-Zeile,
    damit er vor jeder Bauanweisung gelesen wird."""
    treffer = re.search(r"^---\n.*?\n---\n", text, re.DOTALL)
    if not treffer:
        return KOPF.lstrip("\n") + text
    schnitt = treffer.end()
    rest = text[schnitt:]
    h1 = re.search(r"^#[^#].*$", rest, re.MULTILINE)
    if h1:
        schnitt += h1.end()
        rest = text[schnitt:]
    return text[:schnitt] + "\n" + KOPF + rest


def main() -> int:
    fehler = 0
    for design in DESIGNS:
        quelle = ORIGINAL / design / "SKILL.md"
        ziel = ZIEL / design / "SKILL.md"
        if not quelle.is_file():
            print(f"  fehlt: {quelle}")
            fehler += 1
            continue

        text = quelle.read_text(encoding="utf-8")
        angewandt = []

        text, n = GENDER.subn(GENDER_NEU, text)
        if n:
            angewandt.append(f"Anrede({n})")
        text, n = ERFINDEN.subn(ERFINDEN_NEU, text)
        if n:
            angewandt.append(f"Zahlen({n})")
        text, n = GUARDRAIL.subn(GUARDRAIL_NEU, text)
        if n:
            angewandt.append(f"Kontrolle({n})")
        text, n = GARANTIE_ZEILE.subn(GARANTIE_NEU, text)
        if n:
            angewandt.append(f"Garantie-Zeile({n})")
        text, n = GARANTIE_ABSCHNITT.subn(GARANTIE_ABSCHNITT_NEU, text)
        if n:
            angewandt.append(f"Garantie-Abschnitt({n})")

        # Dieselben Regeln gelten im Bauplan wie im Katalog — sonst steht in der
        # einen Datei erlaubt, was die andere verbietet.
        for muster, ersatz in KATALOG_REGELN:
            text = muster.sub(ersatz, text)

        for alt, neu in SCHRIFT_TEXTE:
            text = text.replace(alt, neu)

        text = eszett_zu_ss(text)

        for alt, neu in DESIGN_TEXTE.get(design, []):
            if alt not in text:
                print(f"  {design}: Design-Text nicht gefunden — {alt[:60]!r}")
                fehler += 1
                continue
            text = text.replace(alt, neu)

        text = kopf_einsetzen(text)
        ziel.write_text(text, encoding="utf-8")

        print(f"{design:26s} {', '.join(angewandt) if angewandt else 'nur Kopf + Schriften'}")

        # Der Abschnitts-Katalog gehoert zum Bauplan und muss dasselbe sagen
        katalog_quelle = ORIGINAL / design / "references" / "section-guide.md"
        katalog_ziel = ZIEL / design / "references" / "section-guide.md"
        if not katalog_quelle.is_file():
            print(f"  {design}: section-guide.md fehlt im Original")
            fehler += 1
            continue

        katalog = katalog_quelle.read_text(encoding="utf-8")
        for muster, ersatz in KATALOG_REGELN:
            katalog = muster.sub(ersatz, katalog)
        for alt, neu in KATALOG_WOERTER.get(design, []):
            katalog = katalog.replace(alt, neu)
        katalog = eszett_zu_ss(katalog)
        katalog_ziel.parent.mkdir(parents=True, exist_ok=True)
        katalog_ziel.write_text(katalog, encoding="utf-8")

        # BRAND-CONFIG / BRAND-VOICE / ZIELGRUPPE sind von Hand geschrieben und
        # liegen versioniert in vorlagen/. Sie werden mitkopiert, damit ein
        # Neuaufbau nach dem Loeschen der Skill-Ordner wirklich vollstaendig ist.
        for quelle_name, ziel_name in (
            (f"{design}.BRAND-CONFIG.md", "BRAND-CONFIG.md"),
            ("BRAND-VOICE.md", "BRAND-VOICE.md"),
            ("ZIELGRUPPE.md", "ZIELGRUPPE.md"),
        ):
            vorlage = VORLAGEN / quelle_name
            if not vorlage.is_file():
                print(f"  {design}: Vorlage fehlt — {quelle_name}")
                fehler += 1
                continue
            (ZIEL / design / ziel_name).write_text(
                vorlage.read_text(encoding="utf-8"), encoding="utf-8"
            )

        (ZIEL / design / "references" / "assets").mkdir(parents=True, exist_ok=True)
        (ZIEL / design / "references" / "assets" / ".gitkeep").touch()

    return fehler


if __name__ == "__main__":
    sys.exit(main())
