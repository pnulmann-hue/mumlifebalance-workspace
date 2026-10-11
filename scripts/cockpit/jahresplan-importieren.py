"""Holt die Notion-Jahresplanung **einmalig** ins Cockpit.

Patricia am 24.09.2026: *„launches siehst du eigentlich in jahresplanung. da
müssen wir unter umständen dann noch etwas tiefer eintauchen"*.

🚨 **Das ist ein Umzug, kein Abgleich.** Danach wird die Jahresplanung im
Cockpit gepflegt und in Notion nicht mehr — sonst haette sie genau die
Doppelpflege, die sie loswerden will. Deshalb landet das Ergebnis in
`daten/jahresplan`, und dieses Dokument **gehoert ihr**: der taegliche Abgleich
darf es nie ueberschreiben, wie `daten/ketten` und `daten/produkt-details`.

Die Zeilen stehen hier als Liste im Code, weil ein Python-Skript nicht an
Notion kommt (kein Token ausserhalb der MCP-Verbindung, und Zugangsdaten
gehoeren ohnehin nicht in den Code). Claude hat sie am 24.09.2026 aus
`collection://2ae7078e-8b7e-81f9-adb5-000bb877b193` gelesen — 57 Zeilen, davon
3 leer.

    python scripts/cockpit/jahresplan-importieren.py
    # danach: ArtifactData set -> Sammlung "daten", Dokument "jahresplan"

🚨 **Drei Dinge, die im Cockpit-Launches-Reiter bisher fehlten:**
- **Ferien** sind Kapazitaetsplanung, kein Launch. Fuenf Bloecke im Jahr, in
  denen nichts Grosses starten darf — das sieht man nur, wenn sie mit auf der
  Achse stehen.
- **Preisformat** (0€ / Mini / Mittel / Hochpreisig) ist die Produkttreppe. Ohne
  das steht auf der Achse nicht, ob ein Monat vom Freebie oder vom 777er lebt.
- **Bereich** trennt Mentoring von doTERRA. In Notion heisst das Feld „Status",
  meint aber keine Phase — das Cockpit hat unter „Phase" etwas anderes
  (Vorbereitung/Warm-up/Verkauf). Die beiden nie vermischen.
"""

import json
import sys
from datetime import date, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]

# (start, ende, bereich, stufe, aktivitaet)
# bereich: "mentoring" | "doterra" | "ferien" | ""   stufe: "0€"|"Mini"|"Mittel"|"Hoch"|""
ZEILEN = [
    ("2025-11-25", "2025-12-14", "", "", "Launch Rauhnächte Familienreise"),
    ("2025-12-24", "2026-01-06", "", "", "Rauhnächte Familienreise"),
    ("2025-12-29", "2026-02-28", "doterra", "", "doTERRA: Telegramgruppe Winter"),
    ("2026-01-01", "2026-02-28", "mentoring", "Mittel", "Instagram-Kundenmaschine"),
    ("2026-01-19", "2026-01-23", "doterra", "", "doTERRA: sanfter Start ins Jahr — zurück zu deinem Körper"),
    ("2026-01-19", "", "mentoring", "", "Mum Life Balance: mein Businessaufbau"),
    ("2026-01-20", "2026-01-31", "mentoring", "", "Launch Magnet-Ich"),
    ("2026-01-26", "2026-02-01", "ferien", "", "Sportferien Kids"),
    ("2026-01-29", "2026-01-31", "doterra", "", "doTERRA Businessevent"),
    ("2026-02-14", "2026-02-20", "mentoring", "0€", "Instagram-Story-Challenge"),
    ("2026-02-16", "2026-03-07", "mentoring", "Mini", "Finde dein Thema im Network in 60 Minuten"),
    ("2026-03-01", "2026-03-31", "doterra", "Mittel", "doTERRA: Launch Wellness made simple"),
    ("2026-03-01", "2026-03-31", "mentoring", "Mittel", "Vom Networkwissen zur digitalen Produktwelt"),
    ("2026-03-01", "2026-03-31", "mentoring", "Mini", "Minikurs: Vom Network-Wissen zum eigenen Produkt"),
    ("2026-03-01", "2026-03-31", "doterra", "Mittel", "Mittleres Produkt: Onlineprodukt erstellen"),
    ("2026-03-14", "2026-03-20", "mentoring", "0€", "3-Tage-Challenge: Finde deine erste digitale Produktidee"),
    ("2026-04-01", "2026-04-05", "mentoring", "Hoch", "1:1 Beta-Mentoring «Aus Nebenbei wird Business» (777) — Warm Outreach"),
    ("2026-04-03", "2026-04-17", "ferien", "", "Frühlingsferien"),
    ("2026-04-06", "2026-04-13", "mentoring", "Mini", "Minikurs «Finde dein Thema» reaktivieren"),
    ("2026-04-14", "2026-04-20", "mentoring", "0€", "Masterclass «So schaffst du dir als Mama Zeit fürs Business»"),
    ("2026-04-21", "2026-04-30", "mentoring", "Mini", "Pre-Sale «Dein Business-Rhythmus» — Lieferung Mai"),
    ("2026-04-30", "2026-04-30", "mentoring", "0€", "Erster Test-Call «Die Umsetzerinnen» — Testimonials sammeln"),
    ("2026-05-01", "2026-05-31", "mentoring", "Mittel", "Säule 3: Dein Business-Rhythmus — Signature (333)"),
    ("2026-05-01", "2026-07-31", "doterra", "", "doTERRA Phase 1 — Eimer dichten (Reaktivierung)"),
    ("2026-05-27", "2026-05-31", "ferien", "", "Convention doTERRA"),
    ("2026-06-01", "2026-06-30", "mentoring", "Mittel", "Instagram-Kundenmaschine"),
    ("2026-06-01", "2026-06-30", "mentoring", "Mini", "Reels für Networkerinnen: Sichtbar ohne Tanz-Videos"),
    ("2026-06-01", "2026-06-30", "mentoring", "Mini", "«Die Umsetzerinnen» Membership — Launch (29/Monat)"),
    ("2026-06-13", "2026-06-19", "mentoring", "0€", "Content-Ideen-Challenge: 7 Tage, 7 Posts, 0 Stress"),
    ("2026-07-01", "2026-07-31", "mentoring", "Hoch", "VIP-Paket / Backstage Pass — Jahres-Mitgliedschaft"),
    ("2026-07-01", "2026-07-31", "mentoring", "Mittel", "Vom Networkwissen zur digitalen Produktwelt"),
    ("2026-07-01", "2026-07-31", "mentoring", "Mini", "Dein Workbook in einem Tag"),
    ("2026-07-06", "2026-08-09", "ferien", "", "Sommerferien"),
    ("2026-08-01", "2026-08-30", "mentoring", "Mittel", "Dein Business-Rhythmus — Signature (333)"),
    ("2026-08-01", "2026-08-31", "mentoring", "Mini", "Mama-Zeit: Deine Energie-Basis"),
    ("2026-08-01", "2026-08-31", "doterra", "", "doTERRA: Schlaf-Bundle 151 PV"),
    ("2026-08-01", "2026-08-31", "doterra", "0€", "doTERRA Freebie: 3-Abende-Ritual (Keyword SCHLAF)"),
    ("2026-08-01", "2026-10-31", "doterra", "", "doTERRA Phase 2 — Wachstum drauf (Acquisition + Onboarding)"),
    ("2026-08-08", "2026-08-14", "mentoring", "0€", "Selbstführungs-Check: Wo verlierst du täglich deine Energie?"),
    ("2026-09-01", "2026-09-30", "mentoring", "Mini", "Minikurs «Expertin statt Verkäuferin» — Reaktivierung"),
    ("2026-09-01", "2026-09-30", "mentoring", "0€", "Leadmagnet: «Die 5-Block-Methode» Workbook"),
    ("2026-09-01", "2026-09-30", "mentoring", "Hoch", "1:1 Mentoring «Aus Nebenbei wird Business» (777) — 2. Runde"),
    ("2026-09-28", "2026-10-16", "ferien", "", "Herbstferien"),
    ("2026-10-01", "2026-10-31", "mentoring", "Hoch", "VIP-Paket / Backstage Pass — 2. Launch-Zyklus"),
    ("2026-10-01", "2026-10-31", "mentoring", "0€", "Leadmagnet: Mini-Masterclass als Warm-up VIP-Launch"),
    ("2026-10-01", "2026-10-31", "mentoring", "Mini", "«Fokuszeit für Mamas — in 90 Minuten mehr schaffen»"),
    ("2026-11-01", "2026-11-30", "mentoring", "Mittel", "Instagram-Kundenmaschine — 2. Zyklus"),
    ("2026-11-01", "2026-11-30", "mentoring", "0€", "Leadmagnet: «Dein Instagram-Profil-Check» Workbook"),
    ("2026-11-01", "2026-11-30", "mentoring", "Mini", "Minikurs «Finde dein Thema» — Einstieg IKM"),
    ("2026-11-01", "2026-12-31", "doterra", "", "doTERRA Phase 3 — Push zu Gold + End-of-Year"),
    ("2026-12-01", "2026-12-31", "mentoring", "Mittel", "Säule 2: Digitale Produktwelt — 2. Zyklus (333)"),
    ("2026-12-01", "2026-12-31", "mentoring", "Mini", "Minikurs «Vom Network-Wissen zum eigenen Produkt»"),
    ("2026-12-01", "2026-12-31", "mentoring", "0€", "Jahresplanungsworkshop 2027 — live via Zoom"),
    ("2026-12-21", "2027-01-01", "ferien", "", "Weihnachtsferien"),
]

BEREICH_NAME = {"mentoring": "Mentoring", "doterra": "doTERRA",
                "ferien": "Ferien & Termine", "": "ohne Zuordnung"}


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    heute = date.today().isoformat()
    eintraege = []
    for i, (start, ende, bereich, stufe, name) in enumerate(ZEILEN):
        if not name.strip():
            continue           # die drei leeren Notion-Zeilen fallen raus
        eintraege.append({
            "id": "jp%03d" % i,
            "name": name,
            "start": start,
            "ende": ende or start,
            "bereich": bereich,
            "stufe": stufe,
            "laeuft": bool(start and (ende or start) >= heute >= start),
            "vorbei": bool((ende or start) < heute),
        })

    eintraege.sort(key=lambda x: x["start"])

    # Ein paar Zahlen, die auf der Achse sonst niemand sieht.
    jahr = heute[:4]
    imjahr = [e for e in eintraege if e["start"][:4] == jahr]
    nach_stufe = {}
    for e in imjahr:
        if e["bereich"] == "ferien":
            continue
        nach_stufe[e["stufe"] or "ohne"] = nach_stufe.get(e["stufe"] or "ohne", 0) + 1

    daten = {
        "stand": heute,
        "eintraege": eintraege,
        "bereiche": BEREICH_NAME,
        "zahlen": {
            "gesamt": len(eintraege),
            "im_jahr": len(imjahr),
            "nach_stufe": nach_stufe,
            "ferienbloecke": len([e for e in imjahr if e["bereich"] == "ferien"]),
        },
        "quelle": "Notion-Jahresplanung, einmalig übernommen am 2026-09-24",
        "hinweis": "Gehört Patricia. Der tägliche Abgleich darf das nie überschreiben.",
        "gebaut": datetime.now().isoformat(timespec="seconds"),
    }

    (ziel / "jahresplan.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    print("  %d Einträge übernommen (%d leere Notion-Zeilen weggelassen)"
          % (len(eintraege), len(ZEILEN) - len(eintraege)))
    print("  %d davon in %s" % (len(imjahr), jahr))
    print("  Produkttreppe im Jahr: %s"
          % ", ".join("%s %d" % (k, v) for k, v in sorted(nach_stufe.items())))
    print("  %d Ferien-/Termin-Blöcke" % daten["zahlen"]["ferienbloecke"])
    laeuft = [e for e in eintraege if e["laeuft"]]
    if laeuft:
        print("\n  Läuft gerade:")
        for e in laeuft:
            print("     [%-9s] %s" % (e["bereich"] or "—", e["name"][:64]))
    print("\nAbgelegt in: %s" % (ziel / "jahresplan.json"))


if __name__ == "__main__":
    main()
