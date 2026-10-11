#!/usr/bin/env python3
"""Prueft Captions gegen die vier Kommentar-Regeln (seit 2026-09-19).

Patricia am 19.09.2026: *„mein problem ist, dass gar nicht erst jemand
kommentiert."* Die vier Gruende dafuer stehen in
`.claude/skills/caption/SKILL.md` — hier stehen sie als Code, damit nicht nur
das geprueft wird, woran ich gerade denke.

Geprueft wird:

1. **Aufruf in Zeile 1** — wer zuerst fordert, hat noch nichts gegeben.
2. **Mehr als ein Aufruf** — zwei Aufforderungen teilen die Aufmerksamkeit.
3. **Oeffentliches Eingestaendnis** — ein Kommentar ist oeffentlich. Wer zugeben
   muesste, dass sie feststeckt, tippt nichts.
4. **Aufruf ohne Ergebnis** — „dann schick ich dir das Werkzeug" ist kein Grund.
5. **Textbausteine** — derselbe Satz wortgleich in mehreren Beitraegen.

🚨 Jede Regel ist gegen einen bekannt fehlerhaften Beitrag UND gegen eine
Gegenprobe getestet, die nicht anschlagen darf (`--selbsttest`). Ein Muster, das
alles findet, ist so wertlos wie eins, das nichts findet.

Aufruf:
    python scripts/cockpit/caption-check.py <ordner-mit-json>
    python scripts/cockpit/caption-check.py <ordner> --nur kw39
    python scripts/cockpit/caption-check.py --selbsttest
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

# --------------------------------------------------------------------------
# Die Aufruf-Formen. Jede ist EINE Aufforderung.
# --------------------------------------------------------------------------
AUFRUFE = [
    ("Stichwort", re.compile(r"\bkommentier(e)?\b", re.I)),
    ("Schreib mir", re.compile(r"\bschreib(e)?\s+mir\b", re.I)),
    # 🚨 „Schreib die Nummer in einen zweiten Kommentar" ist ein zweiter Aufruf
    # und enthielt kein „mir" — rutschte deshalb bis 20.09.2026 durch.
    ("In die Kommentare", re.compile(r"in\s+(einen|die)\s+(zweiten\s+)?[Kk]ommentar", re.I)),
    ("Weiterschicken", re.compile(r"\bschick(\s|'s|s\s|e\s)?(das|es|ihn|sie|ihr)?\b", re.I)),
    ("Speichern", re.compile(r"\bspeicher(e|\s+dir)?\b", re.I)),
    ("Folgen", re.compile(r"\bfolg(e|ст)?\s+mir\b", re.I)),
    # 🚨 Braucht ein Personen-Objekt. Ohne das meldete „Markier, was mehr als
    # einmal vorkommt" (Schritt 4 einer Anleitung) einen zweiten Aufruf.
    ("Markieren", re.compile(r"\bmarkier(e)?\s+(eine|einen|jemand|wen|deine|dein|die)\b", re.I)),
    ("Teilen", re.compile(r"\bteil(e)?\s+(das|es)\b", re.I)),
]

# 🚨 „schick ich dir" ist KEIN Aufruf an sie, sondern mein Versprechen.
# Ohne diese Ausnahme meldet jeder Keyword-CTA faelschlich zwei Aufrufe.
KEIN_AUFRUF = re.compile(r"\bschick(e)?\s+ich\s+dir\b", re.I)

# --------------------------------------------------------------------------
# Fragen, die ein oeffentliches Eingestaendnis verlangen
# --------------------------------------------------------------------------
GESTAENDNIS = [
    (re.compile(r"\bbei\s+(welchem|welcher|welchen)\b[^?]{0,60}\?", re.I),
     "fragt, woran sie scheitert"),
    (re.compile(r"\bwo\s+stehst\s+du\b", re.I), "fragt nach ihrem Stand"),
    (re.compile(r"\bwie\s+lange\b[^?]{0,50}\bschon\b[^?]{0,40}\?", re.I),
     "fragt, wie lange sie schon feststeckt"),
    (re.compile(r"\bhängst\s+du\b", re.I), "fragt, wo sie hängt"),
    (re.compile(r"\bwer\s+kennt\s+(das|es)\b", re.I), "verlangt ein Handheben"),
    (re.compile(r"\bkennst\s+du\s+(das|den\s+gedanken)\b", re.I),
     "verlangt ein Handheben"),
    (re.compile(r"\bwas\s+ist\s+dein\s+(grösst|größt|schwierigst)", re.I),
     "fragt nach ihrer Schwäche"),
]

# --------------------------------------------------------------------------
# Belege dafuer, dass der Aufruf ein Ergebnis nennt
# --------------------------------------------------------------------------
# 🚨 „und du hast ein Thema" war beim ersten Lauf ein Fehlalarm — das Muster
# kannte nur „dann hast du". Erweitert und gegen das schlechte Beispiel
# gegengeprueft: dort steht weiterhin kein Ergebnis, die Regel schlaegt an.
ERGEBNIS = re.compile(
    r"\b(hast\s+du|du\s+hast|damit\s+du|dasteht|wird\s+(daraus|aus)\b|erfährst|"
    r"minuten|stunde|sekunden|tage|in\s+\d|"
    r"posten\s+kannst|rauskommt|fertig\s+bist|weisst\s+du)\b", re.I)


def zeilen(text: str) -> list[str]:
    return [z.strip() for z in str(text or "").split("\n") if z.strip()]


def ohne_hashtags(text: str) -> str:
    return "\n".join(z for z in zeilen(text) if not z.startswith("#"))


# 🚨 Der Standard-Schluss ist Absicht, kein Textbaustein. Teil 1 (Folgen-CTA mit
# der 100-Personen-Liste) und Teil 2 (Vorstellungsblock) gehoeren so in jede
# Caption — siehe Memory `feedback_caption-standard-schluss`. Ohne diese Ausnahme
# meldet der Pruefer sie als „6x wortgleich" und niemand liest die echten Funde.
STANDARD = [
    re.compile(r"cooler\s+Ansatz", re.I),
    re.compile(r"100[-\s]Personen[-\s]Liste", re.I),
    re.compile(r"Hi,\s+ich\s+bin\s+Patricia", re.I),
    re.compile(r"Mama\s+von\s+vier\s+Kindern", re.I),
    re.compile(r"Hybridmodell\s+aufgebaut", re.I),
    # 🚨 Der dritte Satz des Vorstellungsblocks. Fehlte beim ersten Anlauf, und
    # dadurch meldeten ALLE sechs Karussells einen Textbaustein, den sie
    # absichtlich tragen — genau die Sorte Fehlalarm, nach der niemand mehr hinschaut.
    re.compile(r"Bei\s+mir\s+lernst\s+du", re.I),
    re.compile(r"Klartext\s+zum\s+Businessaufbau", re.I),
]


def saetze(text: str) -> list[str]:
    roh = re.split(r"(?<=[.!?])\s+|\n+", ohne_hashtags(text))
    return [s.strip() for s in roh
            if len(s.strip()) > 45
            and not any(m.search(s) for m in STANDARD)]


def aufrufe_in(text: str) -> list[str]:
    """Welche Aufruf-Formen kommen vor. Jede zaehlt nur einmal."""
    rein = KEIN_AUFRUF.sub(" ", text)
    return [name for name, muster in AUFRUFE if muster.search(rein)]


def cta_satz(text: str) -> str:
    """Der Satz, in dem der erste Aufruf steht."""
    for s in re.split(r"(?<=[.!?])\s+|\n+", ohne_hashtags(text)):
        if aufrufe_in(s):
            return s.strip()
    return ""


def pruefe(caption: str) -> list[str]:
    raus = []
    z = zeilen(ohne_hashtags(caption))
    if not z:
        return ["keine Caption"]

    # 1 · Aufruf in Zeile 1
    if aufrufe_in(z[0]):
        raus.append("Zeile 1 ist der Aufruf")

    # 2 · mehr als ein Aufruf
    formen = aufrufe_in(ohne_hashtags(caption))
    if len(formen) > 1:
        raus.append("zwei Aufrufe: " + " + ".join(formen))

    # 3 · oeffentliches Eingestaendnis
    for muster, was in GESTAENDNIS:
        if muster.search(ohne_hashtags(caption)):
            raus.append("oeffentliches Eingestaendnis — " + was)
            break

    # 4 · Aufruf ohne Ergebnis.
    # 🚨 Nur bei Lead-Aufrufen. Ein Share-CTA („schick das der Freundin") hat
    # kein Ergebnis und braucht auch keins — der Selbsttest hat genau das als
    # Fehlalarm gemeldet, bevor das Skript zum ersten Mal gelaufen ist.
    LEAD = {"Stichwort", "Schreib mir"}
    cs = cta_satz(caption)
    if cs and LEAD & set(aufrufe_in(cs)) and not ERGEBNIS.search(cs):
        raus.append("Aufruf nennt kein Ergebnis/Aufwand")

    return raus


# --------------------------------------------------------------------------
# Selbsttest: jede Regel an einem bekannt fehlerhaften Satz UND an einer
# Gegenprobe, die NICHT anschlagen darf.
# --------------------------------------------------------------------------
SCHLECHT = """Kommentier **STANDBEIN**, dann schick ich dir das Werkzeug.

Die meisten suchen monatelang nach einem Thema.

Bei welcher der drei Fragen hängst du? Schreib mir die Nummer in einen zweiten Kommentar.

#mamabusiness"""

GUT = """„Ich weiss ja gar nicht, worüber ich schreiben soll."

Dabei beantwortest du wahrscheinlich jede Woche dieselbe Frage im Teamchat.

Im Karussell stehen die drei Fragen. Papier, zwanzig Minuten, keine neue Idee.

Kommentier **STANDBEIN**, dann schick ich dir die Fragen als Werkzeug, das so lange nachfragt, bis ein Satz dasteht, den du posten kannst.

#mamabusiness"""

SHARE = """Wie viele Montage wären es bei dir noch bis zum letzten Arbeitstag?

Ich hab das gemacht, kurz bevor es bei mir so weit war.

Schick das der Freundin, die auch gerade Montage zählt.

#mamabusiness"""


def selbsttest() -> int:
    fehler = 0
    s = pruefe(SCHLECHT)
    for erwartet in ("Zeile 1 ist der Aufruf", "zwei Aufrufe",
                     "oeffentliches Eingestaendnis", "kein Ergebnis"):
        if not any(erwartet in x for x in s):
            print(f"  FEHLT am schlechten Beispiel: {erwartet}")
            fehler += 1
    g = pruefe(GUT)
    if g:
        print("  FEHLALARM am guten Beispiel:", g)
        fehler += len(g)
    sh = pruefe(SHARE)
    if sh:
        print("  FEHLALARM am Share-Beispiel:", sh)
        fehler += len(sh)
    print("Selbsttest:", "in Ordnung" if not fehler else f"{fehler} Probleme")
    return fehler


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("ordner", nargs="?", type=pathlib.Path)
    p.add_argument("--nur", default="")
    p.add_argument("--selbsttest", action="store_true")
    a = p.parse_args()

    if a.selbsttest or not a.ordner:
        return 1 if selbsttest() else 0

    dateien = sorted(a.ordner.rglob("*.json"))
    posten, alle_saetze = [], collections.Counter()
    for d in dateien:
        try:
            doc = json.loads(d.read_text(encoding="utf-8"))
        except Exception:
            continue
        cap = doc.get("caption") or ""
        if not cap.strip():
            continue
        name = doc.get("name") or d.stem
        if a.nur and a.nur.lower() not in d.stem.lower():
            continue
        posten.append((d.stem, name, cap, doc.get("hook") or ""))
        for s in saetze(cap):
            alle_saetze[s] += 1

    print(f"{len(posten)} Beiträge mit Caption\n")
    betroffen = 0
    for schluessel, name, cap, hook in posten:
        funde = pruefe(cap)
        doppelt = [s for s in saetze(cap) if alle_saetze[s] > 1]
        if doppelt:
            funde.append(f"Textbaustein ({len(doppelt)}x wortgleich anderswo)")
        if not funde:
            continue
        betroffen += 1
        print(f"■ {schluessel}  —  {name[:52]}")
        for f in funde:
            print(f"    · {f}")
        print(f"    Zeile 1: {zeilen(ohne_hashtags(cap))[0][:88]}")
        print()

    print(f"{betroffen} von {len(posten)} Beiträgen haben mindestens einen Fund.")
    print()
    print("Was das Skript NICHT prüfen kann: ob der Hook wirklich einen Schmerz")
    print("trifft, ob sie etwas Konkretes mitnimmt und ob es nach dir klingt.")
    print("Das bleibt Lesearbeit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
