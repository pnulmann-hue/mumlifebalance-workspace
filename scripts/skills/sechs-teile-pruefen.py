# -*- coding: utf-8 -*-
"""Prueft jeden eigenen Skill gegen die sechs Teile aus Lektion 5.2.

    python scripts/skills/sechs-teile-pruefen.py [--voll]

Die sechs Teile stehen in der Kursfolie `l52-teile` (scripts/ki-kurs/folien-modul-5.py)
und sind hier woertlich uebernommen — wird die Folie geaendert, gehoert diese Liste
nachgezogen. Zwei Fassungen desselben Versprechens laufen sonst auseinander.

🚨 Die sieben zugekauften Skills werden nicht geprueft und nie weitergegeben
(chatgpt-ads, facebook-ads, copywriting, die vier Salespage-Designs).

🚨 Ein Treffer heisst „der Teil ist vorhanden", nicht „er ist gut". Ob ein Beispiel
wirklich von Patricia ist und ob die Ausgabe-Menge stimmt, sieht nur ein Mensch.
Das Skript sagt das am Ende selbst.
"""

import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

WURZEL = Path(__file__).resolve().parents[2]
SKILLS = WURZEL / ".claude" / "skills"

ZUGEKAUFT = {"chatgpt-ads", "facebook-ads", "copywriting",
             "minikurs-salespage", "signature-kurs-salespage",
             "skill-salespage", "ki-salespage",
             "remotion-motion-graphics"}

# Die sechs Teile, wie die Folie sie nennt, mit dem, woran man sie im Text erkennt.
TEILE = [
    ("Kopf", "Name und ein Satz, wann er dran ist",
     lambda t: bool(re.search(r"^name:\s*\S", t, re.M))
               and bool(re.search(r"^description:", t, re.M))),
    # 🚨 Beim ersten Lauf am 04.11.2026 stand hier nur „Zweck" und „Was dieser Skill
    # macht" — Ergebnis: 27 von 29 angeblich ohne Zweck. Die Skills schreiben aber
    # „Wofür dieser Skill da ist" oder sagen es in der Titelzeile. 27 gleiche Treffer
    # sind nie ein Befund, immer ein Lesefehler.
    ("Zweck", "was am Ende dasteht",
     lambda t: bool(re.search(r"^#{1,4}.*\b(Zweck|Wof[üu]r|Worum|Was dieser Skill)\b",
                              t, re.M | re.I))
               or bool(re.search(r"^\*\*(Zweck|Wof[üu]r|Worum)\b", t, re.M | re.I))
               # Titelzeile mit Gedankenstrich sagt es auch: „# /story — Daily Story …"
               or bool(re.search(r"^#\s+\S.*[—–-]\s*\S{4,}", t, re.M))),
    ("Vorher lesen", "mindestens der Business-Brief",
     lambda t: bool(re.search(r"(liest? (zuerst|vorher)|Pflicht-Lekt|Wissensgrundlage|"
                              r"Grundlage|bevor .{0,30}schreib|context/[\w-]+\.md)",
                              t, re.I))),
    ("Regeln", "Vorgaben und Verbote",
     lambda t: bool(re.search(r"^#{1,4}.*\b(Regeln|Verbote|Harte Regeln|Pflichtregeln)\b",
                              t, re.M | re.I))
               or bool(re.search(r"^\*\*Regeln", t, re.M))),
    ("Ausgabe-Menge", "ganz genau, mit Zahl und Form",
     lambda t: bool(re.search(r"\b(\d+|f[uü]nf|drei|zehn|vier|sieben)\s+"
                              r"(Hooks?|Texte?|Vorschl|Beitr|Folien|Ideen|Varianten|"
                              r"Slides?|Reels?|Karussells?|Mails?|Zeilen|S[aä]tze)",
                              t, re.I))
               or bool(re.search(r"^#{1,4}.*\b(Output|Ausgabe|Standard-Output|"
                                 r"Was herauskommt|Ergebnis)\b", t, re.M | re.I))),
    ("Beispiel", "eines, und von dir",
     lambda t: bool(re.search(r"^#{1,4}.*\bBeispiel", t, re.M | re.I))
               or bool(re.search(r"^\*\*Beispiel", t, re.M))),
]


def main():
    voll = "--voll" in sys.argv
    zeilen = []
    for ordner in sorted(SKILLS.iterdir()):
        if not ordner.is_dir() or ordner.name.startswith("_"):
            continue
        datei = ordner / "SKILL.md"
        if not datei.exists():
            continue
        if ordner.name in ZUGEKAUFT:
            continue
        t = datei.read_text(encoding="utf-8", errors="replace")
        hat = [pruef(t) for _n, _b, pruef in TEILE]
        zeilen.append((ordner.name, hat, len(t)))

    breit = max(len(n) for n, _h, _l in zeilen)
    kopf = "  %-*s  %s" % (breit, "Skill", "  ".join(
        n[:12].ljust(12) for n, _b, _p in TEILE))
    print(kopf)
    print("  " + "-" * (len(kopf) - 2))

    luecken = {}
    for name, hat, _l in sorted(zeilen, key=lambda x: sum(x[1])):
        felder = "  ".join(("ja" if h else "FEHLT").ljust(12) for h in hat)
        print("  %-*s  %s" % (breit, name, felder))
        fehlt = [TEILE[i][0] for i, h in enumerate(hat) if not h]
        if fehlt:
            luecken[name] = fehlt

    voll_ok = [n for n, h, _l in zeilen if all(h)]
    print()
    print("  %d eigene Skills geprueft" % len(zeilen))
    print("  %d haben alle sechs Teile" % len(voll_ok))
    if luecken:
        print()
        print("  Wo etwas fehlt:")
        for name, fehlt in sorted(luecken.items(), key=lambda x: -len(x[1])):
            print("    %-22s %s" % (name, " · ".join(fehlt)))
    if voll:
        print()
        print("  Vollstaendig: %s" % ", ".join(sorted(voll_ok)))
    print()
    print("  🚨 Das Skript sieht nur, OB ein Teil da ist.")
    print("     Ob das Beispiel wirklich von dir ist und ob die Ausgabe-Menge")
    print("     stimmt, muss ein Mensch lesen.")


if __name__ == "__main__":
    main()
