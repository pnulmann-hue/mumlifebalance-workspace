# -*- coding: utf-8 -*-
"""Haengt den Launch-Storys die fehlende Folie „Wer ist schon dabei" an.

Anlass: Patricia am 08.10.2026 — *„sorg dafür, dass in den vorbereiteten storys
im launch alle käufertypen berücksichtigt sind"*.

Befund der Durchsicht aller 19 KI-Launch-Story-Tage: fuenf der sechs Kaeufertypen
kommen je Woche vor, **die Mitmacherin nicht ein einziges Mal**. Die Suche nach
„sind dabei · schon drin · die ersten · Vornamen · haben sich" findet in 139
Folien null Treffer.

🚨 Der Grund ist kein Versehen: Die Storys wurden am 25.09. und 08.10. geschrieben,
   da gab es noch keine Kaeufe. „Wer schon dabei ist" kann man nicht vorschreiben.
   Deshalb legt dieses Skript einen **Platz** an, nicht einen Inhalt — Wortlaut
   zum Anpassen, Anweisung in `notiz` (wird nie gezeichnet).

🚨 Keine erfundenen Namen und keine erfundenen Zahlen. Vornamen nur mit Okay der
   Kundin, sonst Screenshot mit abgedecktem Namen — dieselbe Regel wie in
   `context/kundinnen-geschichten.md`.

🚨 Die Folie kommt VOR die letzte Folie, nie an den Schluss: der CTA bleibt das
   Letzte, was sie sieht.

Wiederholbar: laeuft ein zweites Mal ins Leere, weil die Folie `s-dabei` heisst.

    python scripts/launch/storys-mitmacherin.py <quell-ordner> --ziel <ordner>
"""
import argparse
import json
import pathlib
import sys

# Die Verkaufsphase: ab dem Tag, an dem die Tueren offen sind (08.10. abends),
# bis Kassenschluss. Der 08.10. selbst ist draussen — an dem Tag gab es noch
# keine Kaeufe, die man zeigen koennte.
TAGE = [
    "kw41-story-m-ki-fr", "kw41-story-m-ki-sa", "kw41-story-m-ki-so",
    "kw42-story-m-ki-mo", "kw42-story-m-ki-di", "kw42-story-m-ki-mi",
    "kw42-story-m-ki-do", "kw42-story-m-ki-fr", "kw42-story-m-ki-sa",
    "kw42-story-m-ki-so",
    "kw43-story-m-ki-mo", "kw43-story-m-ki-di", "kw43-story-m-ki-mi",
    "kw43-story-m-ki-do", "kw43-story-m-ki-fr",
]

# Fuenf Wortlaute im Wechsel, damit nicht fuenfzehnmal dieselbe Folie steht.
WORTE = [
    ("Die Ersten sind dabei.",
     "Ich freu mich gerade wie ein Kind über jede einzelne."),
    ("Heute ist wieder jemand dazugekommen.",
     "Ab dem 1. November richtet sie sich ihren Arbeitsplatz ein."),
    ("Schau mal, wer sich entschieden hat.",
     "Genau diese Frauen hatte ich im Kopf, als ich den Kurs gebaut habe."),
    ("Die Gruppe füllt sich.",
     "Ihr fangt am 1. November zusammen an."),
    ("Noch eine, die im November dabei ist.",
     "Und ja, auch sie hat gesagt, dass sie keine Technikerin ist."),
]

# Aussehen im Wechsel: kein Tag sieht aus wie der davor.
# 🚨 `layout` muss zum Hintergrund passen: nur mit `hg: "foto"` ist es "bild".
#    Sonst stuft `storys-gestalten.py` die Folie als Foto-Folie ein und legt
#    eines darunter, das nie gemeint war.
LOOKS = [
    {"hg": "foto", "foto": "s09.jpg", "layout": "bild", "align": "left",
     "schrift": "philo-k", "farbe": "creme", "balken": "zeilen", "pos": 70},
    {"hg": "creme", "layout": "text", "align": "center", "schrift": "sans-b",
     "farbe": "petrol", "balken": "karte", "pos": 46},
    {"hg": "petrol", "layout": "text", "align": "center", "schrift": "philo-k",
     "farbe": "creme", "balken": "zeilen", "pos": 50},
]

NOTIZ = ("✏️ Screenshot der Bestellung oder der Nachricht einsetzen "
         "— Vornamen nur mit Okay der Kundin, sonst Namen abdecken. "
         "Gibt es heute wirklich keinen neuen Kauf, Folie weglassen "
         "statt etwas behaupten.")


def baue(i):
    look = dict(LOOKS[i % len(LOOKS)])
    text, klein = WORTE[i % len(WORTE)]
    f = {"id": "s-dabei", "eyebrow": "Wer schon dabei ist",
         "text": text, "klein": klein, "notiz": NOTIZ,
         "cta": "", "optA": "", "optB": "", "extra": []}
    f.update(look)
    return f


def main():
    p = argparse.ArgumentParser()
    p.add_argument("quelle")
    p.add_argument("--ziel", required=True)
    a = p.parse_args()
    q, z = pathlib.Path(a.quelle), pathlib.Path(a.ziel)
    z.mkdir(parents=True, exist_ok=True)

    fehlt = [t for t in TAGE if not (q / (t + ".json")).exists()]
    if fehlt:
        sys.exit("\U0001f6a8 Nicht gefunden: %s" % ", ".join(fehlt))

    n = 0
    for i, t in enumerate(TAGE):
        d = json.loads((q / (t + ".json")).read_text(encoding="utf-8"))
        fr = d.get("frames") or []
        if any(x.get("id") == "s-dabei" for x in fr):
            print("  %-22s schon drin" % t)
            continue
        if len(fr) < 2:
            sys.exit("\U0001f6a8 %s hat nur %d Folien" % (t, len(fr)))
        neu = fr[:-1] + [baue(i)] + fr[-1:]
        (z / (t + ".json")).write_text(
            json.dumps({"frames": neu,
                        "updatedAt": "2026-10-08T19:00:00.000Z"},
                       ensure_ascii=False, indent=1), encoding="utf-8")
        n += 1
        print("  %-22s %d -> %d Folien  (%s)"
              % (t, len(fr), len(neu), WORTE[i % len(WORTE)][0]))

    print("\n%d Tage vorbereitet in %s" % (n, z))
    print("Jetzt: ArtifactData batch update, Sammlung \"storys\", "
          "je Tag mit if_version.")


if __name__ == "__main__":
    main()
