#!/usr/bin/env python3
"""Prueft Karussell-Foliendefinitionen gegen die KI-Floskel-Blackliste.

    python scripts/karussell-render/blackliste.py <def.json> [...]

Quelle der Muster: context/ki-phrasen-blackliste.md und CLAUDE.md
(Abschnitt "Texte pruefen"). Die vier Tarnungen sind bewusst einzeln
abgedeckt — ein Muster allein findet nur einen Teil der Treffer.
"""
import json, re, sys, os

MUSTER = [
    ("Nicht X, sondern Y",        r"[Nn]icht[^.!?]{0,80}[,.]\s*[Ss]ondern"),
    ("... ueber die Satzgrenze",  r"[Nn]icht[^.!?]{0,90}[.!?]\s*[Ss]ondern"),
    ("... mit Doppelpunkt",       r"[Nn]icht[^.!?]{0,80}:\s*[A-ZÄÖÜ]"),
    ("Kontrast ohne sondern",     r"\b(nicht|kein|keine)\b[^.!?]{0,70}[.!?]\s*(Sie|Er|Es|Das|Du)\s+\w+\s+\w*(daran|deshalb|darum)"),
    ("Stell dir ... vor",         r"[Ss]tell(e)? dir\b[^.!?]{0,40}\bvor\b"),
    ("Es geht nicht um",          r"[Ee]s geht nicht um"),
    ("Das ist kein X, das ist Y", r"[Dd]as ist kein[^.!?]{0,60}[,.]\s*[Dd]as ist"),
]

def texte(pfad):
    d = json.load(open(pfad, encoding="utf-8"))
    for i, f in enumerate(d.get("folien", []), 1):
        for k in ("titel", "unter", "mitte", "fuss", "schluss"):
            if f.get(k):
                yield i, k, re.sub(r"<br>", " ", f[k]).replace("*", "")
        b = f.get("biokarte") or {}
        for k in ("name", "kategorie"):
            if b.get(k):
                yield i, "bio." + k, b[k].replace("*", "")
        for z in b.get("zeilen", []):
            yield i, "bio.zeile", z.replace("*", "")

def main(pfade):
    treffer = 0
    for p in pfade:
        for folie, feld, t in texte(p):
            for name, mus in MUSTER:
                m = re.search(mus, t)
                if m:
                    treffer += 1
                    print(f"TREFFER  {os.path.basename(p)}  Folie {folie} [{feld}]  — {name}")
                    print(f"         ...{t[max(0, m.start()-30):m.end()+30]}...")
    print(f"\n{treffer} Treffer" if treffer else "\nkeine Treffer")
    print("Nicht geprueft: der Beitrags-Check (beruehrt es / nimmt sie etwas mit /")
    print("Grund zu speichern / Grund zu kommentieren) und der Hook-Check. Das bleibt Lesearbeit.")
    return 1 if treffer else 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    sys.exit(main(sys.argv[1:]))
