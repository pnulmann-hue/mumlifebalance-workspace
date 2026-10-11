# -*- coding: utf-8 -*-
"""Ergänzt Easy KI auf der MBA-Seite (WP 3857) — Vorbereitung des HTML.

    python scripts/wordpress/mba-easy-ki-ergaenzen.py            # trocken
    python scripts/wordpress/mba-easy-ki-ergaenzen.py --schreiben  # Datei bauen

Die Seite liegt als EIN text-editor-Widget in `_elementor_data` (Pfad 0/0).
Dieses Skript ändert nur den HTML-String; hochgeladen wird er danach mit
`mba-hochladen.mjs`.

🚨 Die Seite ist über die REST-Schnittstelle nur mit `context=edit` vollständig
   lesbar. Ohne das kommt `content.raw` leer zurück und die Meta-Felder fehlen —
   daran bin ich am 07.10.2026 zuerst gescheitert und hielt die Seite für nicht
   änderbar. Sie ist es.

🚨 Jede Ersetzung prüft vorher mit assert, dass der Suchtext genau einmal
   vorkommt. Ein `str.replace`, das ins Leere läuft, meldet sonst Erfolg und
   ändert nichts.

Fünf Stellen:
  1 Liste „Das ist die MBA"      → Easy KI nach Digitale Produktwelt
  2 „Was in den Kursen steckt"   → Block 04, aus Block 03 als Vorlage gebaut
  3 Einzelpreis-Tabelle          → Zeile Easy KI
  4 Summe 3 Kurse / CHF 999      → 4 Kurse / CHF 1332
  5 vier Stellen „drei Kurse"    → „vier Kurse"
"""
import argparse
import glob
import io
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SICHERUNG = os.path.join(ROOT, "outputs/produkte/mba-launch/_sicherung")
ZIEL = os.path.join(SICHERUNG, "mba-widget-neu.html")

HINWEIS = "Neu ab 1.11.26"
KASSE = "https://mumlifebalance.ch/ki-kurs/"

aenderungen = []


def ersetze(t, alt, neu, was):
    """Ersetzt genau einmal — oder bricht ab."""
    n = t.count(alt)
    assert n == 1, "%s: Suchtext kommt %dx vor (erwartet 1)\n  %r" % (was, n, alt[:110])
    aenderungen.append(was)
    return t.replace(alt, neu)


def lies_widget():
    dateien = sorted(glob.glob(os.path.join(SICHERUNG, "mba-3857-*.json")))
    assert dateien, "Keine Sicherung gefunden — erst mba-holen.mjs laufen lassen."
    d = json.load(io.open(dateien[-1], encoding="utf-8"))
    el = json.loads(d["meta"]["_elementor_data"])
    return dateien[-1], el, el[0]["elements"][0]["settings"]["editor"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schreiben", action="store_true")
    args = ap.parse_args()

    quelle, el, h = lies_widget()
    print("Quelle: %s" % os.path.basename(quelle))
    print("Widget: %d Zeichen\n" % len(h))

    assert "Easy KI" not in h, "Easy KI steht schon drin — Seite schon ergaenzt?"

    # --- 1 · Liste „Das ist die MBA" ---------------------------------------
    dpw_feat = ('<div class="feat reveal"><div class="ico">🚀</div><div>'
                '<h3>Digitale Produktwelt</h3><p>Dein eigenes digitales Angebot, '
                'das auch verkauft, wenn du am Spielplatz sitzt.</p></div></div>')
    easy_feat = ('\n      <div class="feat reveal"><div class="ico">🧠</div><div>'
                 '<h3>Easy KI <em>— %s</em></h3><p>Damit deine KI weiss, wer du bist, '
                 'und in deiner Sprache schreibt — statt dass du jeden Text wieder '
                 'umbaust.</p></div></div>' % HINWEIS)
    h = ersetze(h, dpw_feat, dpw_feat + easy_feat, "1 Liste „Das ist die MBA“")

    # --- 2 · Kursblock 04, aus 03 als Vorlage ------------------------------
    i = h.find(">03</div><div><h3>Digitale Produktwelt</h3>")
    assert i > 0, "Kursblock 03 nicht gefunden"
    start = h.rfind("<div class=", 0, i)
    ende = h.find("</div></div>", i) + len("</div></div>")
    block03 = h[start:ende]

    block04 = (block03
               .replace(">03</div>", ">04</div>")
               .replace("<h3>Digitale Produktwelt</h3>",
                        "<h3>Easy KI <em>— %s</em></h3>" % HINWEIS)
               .replace("Dein erstes digitales Produkt (mit KI), deine Produkttreppe "
                        "und dein Funnel — verkaufen, ohne dich zu verbiegen.",
                        "Dein eigener Arbeitsplatz, feste Auftraege fuer Beitraege und "
                        "Mails, und Werkzeuge, die du deiner Kundschaft weitergeben "
                        "kannst — mit deinem Wissen dahinter.")
               .replace("→ Danach hast du Einkommen, das dir gehört.",
                        "→ Danach schreibt deine KI in deiner Sprache, statt dass du "
                        "Texte umbaust.")
               .replace("https://mumlifebalance.thrivecart.com/digitale-produktwelt/", KASSE))

    # Umschrift wieder einsetzen — im Quelltext stehen echte Umlaute
    for falsch, richtig in [("Auftraege", "Aufträge"), ("Beitraege", "Beiträge"),
                            ("fuer", "für")]:
        block04 = block04.replace(falsch, richtig)

    assert "Easy KI" in block04 and "04</div>" in block04, "Block 04 nicht sauber gebaut"
    h = ersetze(h, block03, block03 + "\n      " + block04, "2 Kursblock 04")

    # --- 3 · Einzelpreis-Zeile --------------------------------------------
    dpw_vrow = ('<div class="vrow"><span>Digitale Produktwelt — einzeln, ohne '
                'Begleitung</span><span>CHF 333</span></div>')
    easy_vrow = ('\n      <div class="vrow"><span>Easy KI — einzeln, ohne Begleitung'
                 '</span><span>CHF 333</span></div>')
    h = ersetze(h, dpw_vrow, dpw_vrow + easy_vrow, "3 Einzelpreis-Zeile")

    # --- 4 · Summe ---------------------------------------------------------
    h = ersetze(h,
                '<span>Nur die 3 Kurse, ganz ohne Begleitung</span><span>CHF 999</span>',
                '<span>Nur die 4 Kurse, ganz ohne Begleitung</span><span>CHF 1332</span>',
                "4 Summe 999 → 1332")

    # --- 5 · „drei Kurse" → „vier Kurse" -----------------------------------
    n = h.count("drei Kurse")
    assert n == 4, "„drei Kurse“ kommt %dx vor (erwartet 4)" % n
    h = h.replace("drei Kurse", "vier Kurse")
    aenderungen.append("5 „drei Kurse“ → „vier Kurse“ (4x)")

    # --- Gegenproben -------------------------------------------------------
    print("Geändert:")
    for a in aenderungen:
        print("  ✓ %s" % a)

    print("\nGegenproben:")
    proben = [
        ("Easy KI kommt vor", h.count("Easy KI") == 3, "3x erwartet (Liste, Block 04, Preiszeile)"),
        ("kein „drei Kurse“ mehr", "drei Kurse" not in h, ""),
        ("kein „3 Kurse“ mehr", "3 Kurse" not in h, ""),
        ("CHF 999 ist weg", "CHF 999" not in h, ""),
        ("CHF 1332 steht da", "CHF 1332" in h, ""),
        ("Hinweis 3x", h.count(HINWEIS) == 2, "Liste + Block 04"),
        ("keine Umschrift", not re.search(r"\b(Auftraege|Beitraege|fuer)\b", h), ""),
        ("Kurslink gesetzt", KASSE in h, ""),
    ]
    schlecht = 0
    for name, ok, zusatz in proben:
        print("  %s %s%s" % ("✓" if ok else "✗", name, (" — " + zusatz) if zusatz and not ok else ""))
        schlecht += 0 if ok else 1

    if schlecht:
        print("\n🚨 %d Gegenprobe(n) fehlgeschlagen — nichts geschrieben." % schlecht)
        sys.exit(1)

    if args.schreiben:
        io.open(ZIEL, "w", encoding="utf-8", newline="\n").write(h)
        print("\nGeschrieben: %s (%d Zeichen)" % (os.path.relpath(ZIEL, ROOT), len(h)))
        print("Hochladen:   node --env-file=.env mba-hochladen.mjs")
    else:
        print("\nTrockenlauf — mit --schreiben die Datei bauen.")


if __name__ == "__main__":
    main()
