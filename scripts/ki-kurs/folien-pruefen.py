#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueft einen fertigen Foliensatz, bevor er veroeffentlicht wird.

    python scripts/ki-kurs/folien-pruefen.py <zielordner>

Geprueft wird nur der SICHTBARE Folientext — Sprechnotizen bleiben aussen vor,
die duerfen klingen wie Patricia spricht.

Nicht geprueft und trotzdem Pflicht: ob die Lektion inhaltlich etwas taugt.
Das bleibt Lesearbeit.
"""
import io, glob, os, re, sys

ZIEL = sys.argv[1] if len(sys.argv) > 1 else "."
ORDNER = os.path.join(ZIEL, "project", "slides")

# Folien, auf denen ein Muster der Unterrichtsgegenstand IST
# „raetsel" zeigt absichtlich einen schlechten KI-Hook als Gegenbeispiel —
# dort sind Blacklisten-Muster der Unterrichtsgegenstand.
ERLAUBT = {"l22-muster", "l22-korrektur", "raetsel", "paar-drei", "was-sie-raet"}

MUSTER = [
 ("Nicht/Sondern",       r"[Nn]icht[^.!?]{0,80}[,.]\s*[Ss]ondern"),
 ("Es geht nicht um",    r"[Ee]s geht nicht um"),
 ("Weniger X mehr Y",    r"\b[Ww]eniger\s+\w+,?\s+mehr\s+\w+"),
 ("Stell dir vor",       r"[Ss]tell dir\b.{0,30}\bvor"),
 ("Huelse",              r"\b(klarer Nutzen|echte Ergebnisse|konkreter Plan|individuelle Lösung|massgeschneidert|praxisnah|auf Augenhöhe|wertvolle Impulse)\b"),
 ("Buzzword",            r"\b(Game-?Changer|Level-?Up|Deep Dive|Mindset-Shift|Leichtigkeit|manifestier)\w*"),
 ("Anleitungs-Floskel",  r"\bSo (machst|geht's|schaffst|kannst) du\b"),
 ("Frage-Floskel",       r"\b(Bist du bereit|Willst du endlich|Möchtest du auch|Kennst du das)\b"),
 ("Superlativ",          r"\b(die beste|die perfekte|die ultimative|nie wieder|100% garantiert)\b"),
 ("Zeit-Floskel",        r"\b(in nur \d+|schnell und einfach|ohne Aufwand|über Nacht|in Rekordzeit)\b"),
]

def sichtbar(h):
    return re.sub(r"<[^>]+>", " ", re.sub(r"<aside>.*?</aside>", "", h, flags=re.S))

def notiz(h):
    m = re.search(r"<aside>(.*?)</aside>", h, flags=re.S)
    return re.sub(r"<[^>]+>", " ", m.group(1)) if m else ""

dateien = sorted(glob.glob(os.path.join(ORDNER, "*.html")))
if not dateien:
    print("Keine Folien in %s" % ORDNER); sys.exit(1)

funde = 0
kurz = []
lektionen = {}

for d in dateien:
    sid = os.path.basename(d)[:-5]
    h = io.open(d, encoding="utf-8").read()
    s = sichtbar(h)
    lektionen[sid.split("-")[0]] = lektionen.get(sid.split("-")[0], 0) + 1

    if sid not in ERLAUBT:
        for name, pat in MUSTER:
            for m in re.finditer(pat, s):
                funde += 1
                print("  [%-18s] %-20s %s" % (sid, name, m.group(0)[:50].strip()))

    # Dreier-Stakkato
    saetze = [x.strip() for x in re.split(r"[.!?]\s+", s) if 3 < len(x.strip()) < 60]
    for i in range(len(saetze) - 2):
        w = [x.split()[0].lower() for x in saetze[i:i+3] if x.split()]
        if len(w) == 3 and w[0] == w[1] == w[2]:
            funde += 1
            print("  [%-18s] Dreier-Stakkato: %s" % (sid, " / ".join(saetze[i:i+3])[:55]))

    # Schriftgroesse
    for m in re.finditer(r"font-size:(\d+)px", h):
        if int(m.group(1)) < 24:
            funde += 1
            print("  [%-18s] Schrift %spx unter 24" % (sid, m.group(1)))

    # Anfuehrungszeichen
    if h.count("„") != h.count("“"):
        funde += 1
        print("  [%-18s] Anfuehrungszeichen unbalanciert" % sid)

    if len(notiz(h).split()) < 12:
        kurz.append(sid)


# ── Umlaut-Waechter ──────────────────────────────────────────────────
# 🚨 Am 05.10.2026 standen „So laeuft es ab" und „Das Herzstueck" auf fertigen
# Folien — hineingerutscht beim Patchen, weil ich Umlaute umschrieben habe, um
# Encoding-Aerger zu vermeiden. Die Blacklisten-Pruefung sieht das nicht.
# Geprueft wird nur der SICHTBARE Text; Sprechnotizen duerfen alles.
AUSNAHMEN_UML = ("bauen","dauert","gedauert","dauern","dauernd","Frauen","heute","zuerst","Abenteuer","neues","neue",
                 "auch","auf","aus","laut","Haus","raus","draussen","brauchst","Frau",
                 "schauen","genau","genauso","blau","grau","Pause","Pausen","baue",
                 "baut","gebaut","glaube","glaubt","kaufe","kauft","gekauft","laufen",
                 "Verlauf","zuhause","Hause","teuer","neuer","neuen","aktuell","Statue")
uml = re.compile(r"\b\w*(ae|oe|ue)\w*\b")
for d in dateien:
    sid = os.path.basename(d)[:-5]
    txt = sichtbar(io.open(d, encoding="utf-8").read())
    for m in uml.finditer(txt):
        w = m.group(0)
        if any(w.lower().startswith(a.lower()) for a in AUSNAHMEN_UML):
            continue
        funde += 1
        print("  [%-18s] Umschriebener Umlaut: %s" % (sid, w))


print("")
print("  %d Folien, %d Lektionen" % (len(dateien), len(lektionen) - 1))
print("  Blackliste und Format: %s" % ("SAUBER" if funde == 0 else "%d Funde" % funde))
if kurz:
    print("  Duenne Sprechnotizen: %s" % ", ".join(kurz))
print("")
print("  Nicht maschinell geprueft: ob die Lektion etwas taugt. Einmal lesen.")
sys.exit(1 if funde else 0)
