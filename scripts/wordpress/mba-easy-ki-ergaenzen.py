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

# 23.10.2026: kein Datum mehr auf der Seite (Patricia) — Easy KI ist in der MBA gratis dabei
HINWEIS = "gratis dabei"
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

    # --- 3 · Wert-Tabelle: Easy KI als Geschenk, NICHT in die Summe ------------
    # 23.10.2026: Vier Kurse einzeln wären 1332 — gleich neben dem MBA-Preis 1347 sähe
    # das Jahr Begleitung plus PIA aus wie 15 Franken wert. Deshalb bleibt die Summe bei
    # den drei Kursen (999), und Easy KI steht als eigene Zeile „gratis dabei“ darunter.
    summe = '<span>Nur die 3 Kurse, ganz ohne Begleitung</span><span>CHF 999</span></div>'
    easy_vrow = ('\n      <div class="vrow"><span>Dazu Easy KI für Networkerinnen — in der MBA '
                 'gratis dabei</span><span>Wert CHF 333</span></div>')
    h = ersetze(h, summe, summe + easy_vrow, "3 Easy KI als Geschenk unter der Summe")

    # --- 4 · „drei Kurse" → „drei Kurse plus Easy KI" ----------------------------
    n = h.count("drei Kurse")
    assert n == 4, "„drei Kurse“ kommt %dx vor (erwartet 4)" % n
    h = h.replace("drei Kurse", "drei Kurse plus Easy KI")
    aenderungen.append("4 „drei Kurse“ → „drei Kurse plus Easy KI“ (4x)")

    # --- 5 · Termine raus (Programm läuft seit dem Sommer) -------------------
    h = ersetze(h, "Los mit PIA und den Kursen, in deinem Tempo, schon über den Sommer.",
                "Du startest sofort mit PIA und den Kursen, in deinem Tempo.", "5a Schritt 2 ohne Sommer")
    h = ersetze(h, "Nach den Sommerferien starten wir live — du bleibst nie allein.",
                "Die Live-Calls laufen schon, du steigst einfach beim nächsten ein und bist nie allein damit.",
                "5b Schritt 3 ohne Sommerferien")
    h = ersetze(h, "<li>Programmstart Mitte August — Zugang sofort</li>",
                "<li>Zugang sofort, die Live-Calls laufen schon</li>", "5c Preisblock ohne Programmstart")
    h = ersetze(h, "Zweimal im Monat, live (und aufgezeichnet). Wir starten nach den Sommerferien und legen die "
                   "festen Zeiten gemeinsam mit der Gruppe fest.",
                "Zweimal im Monat, live und aufgezeichnet. Die Termine findest du in der Telegram-Gruppe.",
                "5d FAQ Calls ohne Sommerferien")

    # --- Gegenproben -------------------------------------------------------
    print("Geändert:")
    for a in aenderungen:
        print("  ✓ %s" % a)

    print("\nGegenproben:")
    proben = [
        ("Easy KI kommt vor", h.count("Easy KI") == 7, "7x erwartet (Liste, Block 04, Wertzeile, 4× „plus Easy KI“)"),
        ("Summe bleibt CHF 999", "CHF 999" in h and "CHF 1332" not in h, ""),
        ("kein Sommer, kein August", not re.search(r"Sommer|August", h), ""),
        ("Hinweis „gratis dabei“", h.count(HINWEIS) >= 2, "Liste + Block 04"),
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
