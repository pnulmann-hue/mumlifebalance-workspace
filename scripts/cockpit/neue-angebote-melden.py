"""Neue Angebote in ThriveCart erkennen und als Checklisten-Aufgabe vorbereiten.

Patricia, 31.10.2026: „dass bei den neu angelegten produkten und auch bumps etc.
immer alles nach der checkliste abgearbeitet wird“.

Was direkt in ThriveCart entsteht (ein geklontes Produkt, ein neuer Bump, ein
Upsell), läuft an /angebot vorbei und damit an der Funnel-Checkliste. Dieses
Skript vergleicht den heutigen Abzug (thrivecart.json) mit dem, was schon
gesehen wurde, und schreibt für jedes neue Stück eine Aufgabe in
neue-angebote.json. Der Task cockpit-daten-abgleich hängt sie an
daten/aufgaben an und meldet sie per Telegram.

    python scripts/cockpit/neue-angebote-melden.py outputs/cockpit/abgleich

🚨 Beim allerersten Lauf gibt es keinen Vergleich. Dann wird nur der Stand
   gemerkt und nichts gemeldet — sonst stünden 60 alte Angebote als „neu“ da.
🚨 Erst nach dem Melden gilt etwas als gesehen. Bricht der Task dazwischen ab,
   kommt es am nächsten Tag nochmal, statt still verloren zu gehen.
   Deshalb merkt sich das Skript den Stand nur mit --merken.
"""
import datetime
import json
import pathlib
import sys

ARTEN = {"products": "Produkt", "bumps": "Bump", "upsells": "Upsell",
         "downsells": "Downsell"}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ordner = pathlib.Path(args[0] if args else "outputs/cockpit/abgleich")
    tc = json.loads((ordner / "thrivecart.json").read_text(encoding="utf-8"))
    gesehen_pfad = ordner / "thrivecart-gesehen.json"
    jetzt = {art: sorted(str(x["id"]) for x in tc.get(art) or []) for art in ARTEN}

    if not gesehen_pfad.exists():
        gesehen_pfad.write_text(json.dumps(jetzt, indent=1), encoding="utf-8")
        (ordner / "neue-angebote.json").write_text("[]", encoding="utf-8")
        print("Erster Lauf: Stand gemerkt (%s), nichts gemeldet."
              % ", ".join("%d %s" % (len(v), k) for k, v in jetzt.items()))
        return

    if "--merken" in sys.argv:
        gesehen_pfad.write_text(json.dumps(jetzt, indent=1), encoding="utf-8")
        print("Stand gemerkt.")
        return

    alt = json.loads(gesehen_pfad.read_text(encoding="utf-8"))
    heute = datetime.date.today()
    morgen = (heute + datetime.timedelta(days=1)).isoformat()
    aufgaben = []
    for art, wort in ARTEN.items():
        bekannt = set(alt.get(art) or [])
        for x in tc.get(art) or []:
            kennung = str(x["id"])
            if kennung in bekannt:
                continue
            name = (x.get("name") or "").strip() or "ohne Namen"
            preis = ", ".join("%s %s" % (p.get("betrag"), p.get("waehrung") or "")
                              for p in x.get("preise") or [] if p.get("betrag") is not None)
            wo = x.get("url") or ""
            aufgaben.append({
                "id": "fc-%s-%s" % (art, kennung),
                "aufgabe": "Funnel-Checkliste · neues %s: %s" % (wort, name),
                "datum": morgen,
                "prio": "Mittel",
                "status": "Geplant",
                "notiz": ("Neu in ThriveCart seit %s (%s %s%s%s). Claude prüft es gegen die "
                          "Funnel-Checkliste, sobald du „prüf %s gegen die Checkliste“ sagst — "
                          "oder du gehst die Liste selbst durch."
                          % (heute.strftime("%d.%m."), wort, kennung,
                             " · " + preis.strip() if preis.strip() else "",
                             " · " + wo if wo else "", name)),
                "erledigt": False,
                "bereich": "Business",
                "quelle": "ThriveCart-Abgleich",
                "fuerClaude": True,
            })
    (ordner / "neue-angebote.json").write_text(
        json.dumps(aufgaben, ensure_ascii=False, indent=1), encoding="utf-8")
    print("%d neue Angebote in ThriveCart" % len(aufgaben))
    for a in aufgaben:
        print("  " + a["aufgabe"])


if __name__ == "__main__":
    main()
