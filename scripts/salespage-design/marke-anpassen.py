#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Faerbt die vier Salespage-Design-Vorlagen auf Patricias Marke um.

Ausgangslage: Die Vorlagen kommen im Original in Rose/Gold/Pink/Neon.
Patricias Marke kennt nur vier Farben — Petrol, Dunkelblau, Creme, Orange —
und zwei Schriften: Philosopher (Headlines) + Source Sans 3 (Fliesstext).
Kein Gelb, kein Gold, kein Pink.

Damit die vier Designs trotzdem unterscheidbar bleiben, traegt jedes eine
eigene Rolle statt einer eigenen Fremdfarbe:

    minikurs          hell + verspielt   Petrol auf Weiss, Orange als Knopf
    signature-kurs    hell + editorial   Creme + Foto, Orange als Knopf, Petrol als Anker
    skill             dunkel + technisch Dunkelblau-Grund, Petrol leuchtet
    ki                dunkel + laut      Dunkelblau-Grund, Orange leuchtet

Aufruf (aus dem Projekt-Stammverzeichnis):

    python scripts/salespage-design/marke-anpassen.py

Das Skript arbeitet auf .claude/skills/<design>/references/reference-page.html
und ist wiederholbar: Quelle ist immer reference/salespage-designs-original/,
also richtet ein zweiter Lauf keinen Schaden an.

Achtung bei der Erweiterung: In den Vorlagen stehen HTML-Entities wie
&#128247; (Emoji) und &#215; (Mal-Zeichen). Die sehen wie Farbwerte aus.
Deshalb wird ausschliesslich ersetzt, was hier ausdruecklich aufgelistet
ist — nie per Muster ueber alle #-Werte.
"""

import re
import shutil
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
ORIGINAL = WURZEL / "reference" / "salespage-designs-original"
ZIEL = WURZEL / ".claude" / "skills"

# --- Patricias Marke (context/brand-voice.md, scripts/karussell-render/brand-stories.css) ---
PETROL = "#12828c"
PETROL_HELL = "#2ba7b3"
PETROL_LEUCHTEND = "#6fd0d6"
PETROL_DUNKEL = "#0d626a"
DUNKELBLAU = "#29556d"
CREME = "#f1ecdd"
ORANGE = "#dc822e"
ORANGE_HELL = "#f0a45e"
ORANGE_DUNKEL = "#b4661f"
TEXT = "#0c1c30"

SCHRIFT_LINK = (
    "https://fonts.googleapis.com/css2?"
    "family=Philosopher:ital,wght@0,400;0,700;1,400;1,700"
    "&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700;1,400;1,600"
    "&display=swap"
)

# Schriften, die aus den Original-Vorlagen verschwinden.
# Alles Editoriale/Display wird Philosopher, alles Lesbare Source Sans 3.
SCHRIFT_ERSATZ = [
    ("'Instrument Serif'", "'Philosopher'"),
    ("'Playfair Display'", "'Philosopher'"),
    ("'Sacramento'", "'Philosopher'"),
    ("'Caveat'", "'Philosopher'"),
    ("'Anton'", "'Philosopher'"),
    ("'Archivo'", "'Philosopher'"),
    ("'Orbitron'", "'Source Sans 3'"),
    ("'Montserrat'", "'Source Sans 3'"),
    ("'Poppins'", "'Source Sans 3'"),
    ("'DM Sans'", "'Source Sans 3'"),
    ("'Inter'", "'Source Sans 3'"),
]

# 'Space Mono' bleibt bewusst stehen: Das Skill-Design hat einen Terminal-Block,
# der ohne Festbreiten-Schrift zerfaellt. Das ist eine Funktion, keine Marken-Schrift.

# Nachtrag je Design: Was die Vorlage nicht ueber eine Variable regelt.
# Das minikurs-Design hatte nur EINE Schrift (Poppins) fuer Text und
# Ueberschriften. Nach dem Tausch saessen die Ueberschriften in Source Sans 3 —
# in Patricias Marke gehoeren sie in Philosopher.
NACHTRAG = {
    # Das KI-Design traegt Orange als Leuchtfarbe. Weisse Schrift auf Orange
    # unterschreitet den Kontrast-Richtwert (2,9:1), dunkle Schrift auf Orange
    # liegt bei 6:1 — und entspricht ausserdem Patricias Karussell-Optik.
    "ki-salespage": (
        "\n  /* Marken-Nachtrag: Knopf orange mit dunkler Schrift */\n"
        "  :root{--cta:linear-gradient(100deg,#b4661f 0%,#dc822e 45%,#f0a45e 100%);}\n"
        "  .btn,.topbar .cta{color:#0c1c30;}\n"
        "  .btn.ghost{color:#f1ecdd;}\n"
    ),
    "minikurs-salespage": (
        "\n  /* Marken-Nachtrag: Ueberschriften in Philosopher */\n"
        "  h1,h2,h3,.disp,.display{font-family:'Philosopher',Georgia,serif;}\n"
        "  /* Knopf orange mit dunkler Schrift — weiss auf Orange traegt nur 2,9:1 */\n"
        "  a.cta,.cta{color:#0c1c30;}\n"
        "  /* Highlight-Wort auf Petrol-Flaeche aufhellen: volles Orange auf Petrol\n"
        "     traegt nur 1,6:1, das helle Orange rund 2,8:1. Auf hellen Sektionen\n"
        "     bleibt das volle Orange. */\n"
        "  .sec-dark .gold{color:#f7c08f;}\n"
    ),
    # Gleiches Kontrast-Thema wie beim KI-Design: Der Knopf ist orange, also
    # bekommt er dunkle Schrift statt weisser.
    "signature-kurs-salespage": (
        "\n  /* Marken-Nachtrag: Knopf orange mit dunkler Schrift */\n"
        "  .btn,.btn-lg{color:#0c1c30;}\n"
        "  .btn-ghost{color:#b4661f;}\n"
        "  .bg-ink .btn-ghost,.parallax .btn-ghost{color:#f1ecdd;}\n"
    ),
}

# --- Farbzuordnung je Design -------------------------------------------------
# Links der Original-Wert, rechts Patricias Wert. Kleinschreibung.

MINIKURS = {
    # Haupt- und Akzentfarben
    "#e8477e": PETROL,          # kraeftige Hauptfarbe (war Pink)
    "#c92f63": PETROL_DUNKEL,
    "#d05a86": "#17949f",
    "#e0b73c": ORANGE,          # Knopf-Farbe (war Gold)
    "#c99a1e": ORANGE_DUNKEL,
    "#f6db8e": "#f2c08a",
    # zarte Rosa-Flaechen -> zarte Petrol-Flaechen
    "#ffe6f0": "#e4f0f0",
    "#fbe0ea": "#ddebeb",
    "#ffd9e8": "#dcecec",
    "#f5eaf0": "#e9f1f1",
    "#f4c9dd": "#c9e2e3",
    "#f2d6e0": "#d6e7e7",
    "#f0e0e8": "#dfeaea",
    "#efc2d6": "#c2dedf",
    "#c98aa8": "#8ab8bb",
    "#cf8aa8": "#8ab8bb",
    "#de9ab5": "#9ac4c7",
    "#d49cb8": "#9cc2c5",
    "#b8919f": "#91a8b0",
    # Gold-Tints -> Orange-Tints
    "#fbf0d0": "#fae7d3",
    "#fdf7ea": "#fcf2e6",
    # Creme + Text
    "#eadfce": CREME,
    "#f0e6d8": "#eee8d8",
    "#ece2d3": "#e9e3d2",
    "#ded8cf": "#ddd6c6",
    "#faf3ec": "#f7f3e9",
    "#2a2110": TEXT,
    "#2a1a20": TEXT,
    "#6b5560": "#5c6b75",
}
MINIKURS_RGB = {
    "232,71,126": "18,130,140",
    "224,183,60": "220,130,46",
    "246,219,142": "242,192,138",
    "168, 147, 95": "41, 85, 109",
}

SIGNATURE = {
    # Pink-Familie -> Orange (Knopf + Akzent)
    "#ff3f86": ORANGE,
    "#d21e66": ORANGE_DUNKEL,
    "#ffe1ec": "#f7e2cd",
    "#ff5c98": "#e8913f",
    "#ff6aa0": "#eb9c50",
    "#ff9dc0": "#f2bd8a",
    "#ff4d8d": "#e08733",
    "#ff3d9c": ORANGE,
    "#ff2e9a": ORANGE,
    # Gold -> Petrol (Eyebrows, Wert-Anker)
    "#bd8f3f": PETROL,
    "#e7d4a6": "#9ecdd0",
    "#1a9e8c": "#17949f",
    "#7a2bd6": DUNKELBLAU,
    "#173257": DUNKELBLAU,
    # Creme + Blush -> Creme + zartes Petrol
    "#fbf4ef": CREME,
    "#f6e9e1": "#e7e0cd",
    "#f7f3f1": "#f4f1e8",
    "#fbe7ec": "#dfe9e8",
    "#fdf3f6": "#eef4f3",
    "#fbecf1": "#e8f0ef",
    "#fdf4f7": "#eef4f3",
    "#fdf0f5": "#eaf2f1",
    "#f4ebef": "#e9efee",
    "#f3e7ec": "#e6eeed",
    "#eadfe4": "#dfe9e8",
    "#e6d7dd": "#d8e5e4",
    "#dfd3d9": "#d2e0df",
    "#d9b9c4": "#aecdcd",
    # dunkle Flaechen -> Dunkelblau-Familie
    "#2a1620": TEXT,
    "#0c0709": TEXT,
    "#251019": "#12283d",
    "#1c1016": "#0f2338",
    "#161318": "#13202f",
    "#050304": "#081422",
    # gedaempfter Text
    "#8f7079": "#5c6b75",
    "#553f48": "#3d5260",
    "#4a3640": "#33495a",
    "#b1849a": "#8fa8b3",
    "#b3a0a8": "#97a8b0",
    "#6b5560": "#5c6b75",
    "#3f2a32": "#2a3e4d",
    "#3a2a30": "#263a49",
}
SIGNATURE_RGB = {
    "255,157,192": "242,189,138",
    "255,63,134": "220,130,46",
    "255,92,152": "232,145,63",
    "214,30,102": "180,102,31",
    "210,30,102": "180,102,31",
    "255,46,154": "220,130,46",
    "255,45,150": "220,130,46",
    "120,40,60": "41,85,109",
    "12,7,9": "12,28,48",
    "20,10,14": "15,35,56",
    "9,5,7": "8,20,34",
}

SKILL = {
    # Grundflaechen -> Dunkelblau-Familie
    "#09090f": TEXT,
    "#0f0f18": "#12283d",
    "#15151f": "#17324a",
    "#1c1c28": "#1d3d58",
    "#3a3444": "#2a4356",
    # Neon-Pink -> Petrol (dieses Design leuchtet petrol)
    "#ff3d8b": PETROL_HELL,
    "#ff74ad": PETROL_LEUCHTEND,
    "#c2185b": PETROL,
    "#ff2e86": PETROL_DUNKEL,   # Verlauf-Anfang Knopf
    "#ff5fa2": PETROL,          # Verlauf-Mitte Knopf
    "#ff9ecb": "#17949f",       # Verlauf-Ende Knopf (nicht heller — sonst Kontrast weg)
    # Text
    "#f5eef2": CREME,
    "#a9a2ae": "#9aa8b3",
    "#9a939f": "#8b9aa6",
    "#6f6874": "#5c6b75",
    # Signalfarben bleiben Signalfarben, nur markennah gedreht
    "#e06a6a": "#d4614f",
    "#7ee0a8": "#7ed0b4",
}
SKILL_RGB = {
    "255,46,134": "18,130,140",
    "255,95,162": "43,167,179",
    "255,116,173": "111,208,214",
    "201,24,91": "13,98,106",
    "9,9,15": "12,28,48",
}

KI = {
    # Grundflaechen -> Dunkelblau-Familie
    "#08060f": TEXT,
    "#0d0a18": "#122a42",
    "#150f22": "#16324c",
    # Neon-Triade -> Orange leuchtet, Petrol stuetzt
    "#ff5cc8": ORANGE,
    "#ff2fb0": ORANGE,
    "#ff86e0": ORANGE_HELL,
    "#ff6a9e": "#e8913f",
    "#c04bff": "#f7c08f",       # Verlauf-Ende Ueberschrift: hell statt petrol
    "#a63bff": PETROL,
    "#c11bd0": "#1a9aa5",
    "#7a1bd8": PETROL,
    "#41e7ff": "#4fc9d1",
    # Text
    "#f3e9f4": CREME,
    "#a99cb5": "#9aa8b3",
    "#6f6478": "#5c6b75",
    "#230414": TEXT,
}
KI_RGB = {
    "255,47,176": "220,130,46",
    "255,47,120": "232,145,63",
    "255,120,220": "220,130,46",
    "166,59,255": "18,130,140",
    "120,60,255": "18,130,140",
    "65,231,255": "79,201,209",
    "8,6,15": "12,28,48",
}

# Nur in den dunklen Designs wird reines Weiss zu Creme — auf hellem Grund
# bleibt Weiss die Sektionsfarbe und darf nicht angefasst werden.
DESIGNS = {
    "minikurs-salespage": (MINIKURS, MINIKURS_RGB, False),
    "signature-kurs-salespage": (SIGNATURE, SIGNATURE_RGB, False),
    "skill-salespage": (SKILL, SKILL_RGB, True),
    "ki-salespage": (KI, KI_RGB, True),
}


def schriften_ersetzen(text: str) -> str:
    """Google-Fonts-Link und alle font-family-Angaben auf die Marke drehen."""
    text = re.sub(
        r"https://fonts\.googleapis\.com/css2\?[^\"']+",
        SCHRIFT_LINK,
        text,
    )
    for alt, neu in SCHRIFT_ERSATZ:
        text = text.replace(alt, neu)
        text = text.replace(alt.replace("'", ""), neu.replace("'", ""))
    return text


def farben_ersetzen(text: str, hexe: dict, rgbs: dict, weiss_zu_creme: bool) -> tuple:
    """Ersetzt genau die aufgelisteten Werte. Nie per Muster — sonst
    erwischt es HTML-Entities wie &#128247; oder &#215;."""
    treffer = 0
    for alt, neu in sorted(hexe.items(), key=lambda p: -len(p[0])):
        muster = re.compile(r"(?<!&)" + re.escape(alt), re.IGNORECASE)
        text, n = muster.subn(neu, text)
        treffer += n
    for alt, neu in rgbs.items():
        muster = re.compile(r"(rgba?\(\s*)" + re.escape(alt), re.IGNORECASE)
        text, n = muster.subn(lambda m: m.group(1) + neu, text)
        treffer += n
    if weiss_zu_creme:
        for muster, ersatz in (
            (r"#ffffff\b", CREME),
            (r"#fff\b", CREME),
        ):
            text, n = re.subn(muster, ersatz, text, flags=re.IGNORECASE)
            treffer += n
    return text, treffer


def entities_pruefen(text: str) -> list:
    """HTML-Entities sind rein numerisch (&#128293;). Steht dort ein
    Buchstabe, hat eine Farbersetzung hineingegriffen und das Zeichen
    zerstoert."""
    return sorted(set(re.findall(r"&#[0-9]*[a-fA-F][0-9a-fA-F]*;", text)))


def rest_pruefen(text: str, design: str) -> list:
    """Sucht Farbwerte, die nach dem Lauf noch nach Fremdfarbe aussehen —
    viel Rot bei wenig Gruen und Blau (Pink/Magenta) oder Gold-Gelb."""
    verdaechtig = []
    for wert in set(re.findall(r"#[0-9a-fA-F]{6}\b", text)):
        r = int(wert[1:3], 16)
        g = int(wert[3:5], 16)
        b = int(wert[5:7], 16)
        pink = r > 170 and b > 110 and g < r - 60 and b > g + 30
        # Gold hat Gruen dicht am Rot (#e0b73c: Abstand 41). Orange nicht
        # (#dc822e: Abstand 90) — sonst schlaegt die Pruefung bei jedem
        # Marken-Orange an.
        gold = r > 170 and g > 130 and b < 110 and abs(r - g) < 55
        if pink or gold:
            verdaechtig.append(wert)
    return sorted(verdaechtig)


def main() -> int:
    if not ORIGINAL.is_dir():
        print(f"Original-Bundle fehlt: {ORIGINAL}")
        return 1

    fehler = 0
    for design, (hexe, rgbs, weiss) in DESIGNS.items():
        quelle = ORIGINAL / design / "references" / "reference-page.html"
        ziel = ZIEL / design / "references" / "reference-page.html"
        if not quelle.is_file():
            print(f"  fehlt: {quelle}")
            fehler += 1
            continue
        ziel.parent.mkdir(parents=True, exist_ok=True)

        text = quelle.read_text(encoding="utf-8")
        text = schriften_ersetzen(text)
        nachtrag = NACHTRAG.get(design)
        if nachtrag:
            stelle = text.rfind("</style>")
            if stelle == -1:
                print(f"  {design}: kein </style> gefunden, Nachtrag faellt aus")
                fehler += 1
            else:
                text = text[:stelle] + nachtrag + text[stelle:]
        text, treffer = farben_ersetzen(text, hexe, rgbs, weiss)
        ziel.write_text(text, encoding="utf-8")

        rest = rest_pruefen(text, design)
        kaputt = entities_pruefen(text)
        if kaputt:
            print(f"{design:26s} FEHLER — zerstoerte Zeichen: {', '.join(kaputt)}")
            fehler += 1
            continue
        hinweis = f"  Rest zu pruefen: {', '.join(rest)}" if rest else "  sauber"
        print(f"{design:26s} {treffer:4d} Farbwerte ersetzt |{hinweis}")

        # Die Beispiel-Bilder der Vorlage kopieren, falls vorhanden
        bilder = ORIGINAL / design / "references" / "assets"
        if bilder.is_dir():
            for datei in bilder.iterdir():
                if datei.is_file() and datei.name != ".gitkeep":
                    shutil.copy2(datei, ziel.parent / "assets" / datei.name)

    return fehler


if __name__ == "__main__":
    sys.exit(main())
