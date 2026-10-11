"""Schreibt den offenen Cockpit-Stand dorthin, wo der Telegram-Bot ihn lesen kann.

🚨 **Der Cockpit-Bot kommt nicht an die Artifact-Datenbank.** Er laeuft als
Worker auf Railway; die Beitraege liegen im Artifact und sind nur ueber
`ArtifactData` erreichbar, also nur aus Claude Code heraus. Es gibt keinen
Schluessel, der das aendert — es gibt schlicht keine Schnittstelle dorthin.

Deshalb diese Bruecke: Claude holt die Beitraege (`ArtifactData list` nach
`outputs/cockpit/inhalte-roh/`), dieses Skript macht daraus einen kleinen
Auszug, und der liegt **im Repo neben dem Bot** — Railway deployt ihn mit.

    python scripts/cockpit/stand-fuer-bot.py

-> `scripts/cockpit-bot/cockpit-stand.json`

**Die Aufteilung ist dieselbe wie in der Wochen-Vorschau** (`wasFehlt()` im
Cockpit) und darf nicht auseinanderlaufen:

| Wer | Wann |
|---|---|
| **Patricia** | Sprechreel ohne Video · fehlende Caption · fehlender Hook |
| **Claude** | B-Roll ohne Video (wird aus vorhandenem Material gebaut) |

Ohne diese Trennung wartet jede auf die andere — genau das war seit KW38 der
Fall.

🚨 **Der Auszug traegt ein Datum, und der Bot zeigt es an, sobald er zwei Tage
alt ist.** Ein alter Stand sieht aus wie ein aktueller und ist deshalb
gefaehrlicher als gar keiner.

🚨 **Nur Feed-Beitraege.** Storys gehen nie ueber Blotato, Patricia postet sie
selbst — sie in dieselbe Zahl zu werfen macht die Zahl groesser als die Arbeit
dahinter (am 18.09. standen so 27 statt 17 da).
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
ROH = ROOT / "outputs" / "cockpit" / "inhalte-roh"
ZIEL = ROOT / "scripts" / "cockpit-bot" / "cockpit-stand.json"

# Nur Feed. Storys bleiben draussen (siehe oben).
ARTEN = [("reels", "Reel"), ("karussells", "Karussell")]


def laden(ordner: str) -> list:
    p = ROH / ordner
    if not p.is_dir():
        return []
    raus = []
    for datei in sorted(p.glob("*.json")):
        try:
            d = json.loads(datei.read_text(encoding="utf-8"))
        except Exception:
            continue
        d.setdefault("id", datei.stem)
        raus.append(d)
    return raus


def leer(wert) -> bool:
    return not (wert or "").strip() if isinstance(wert, str) else not wert


def ist_entwurf(b: dict) -> bool:
    """Ein leerer Platzhalter ist keine Aufgabe. Beim ersten Lauf am 18.09.
    standen drei Phantom-Aufgaben ganz oben in der Liste."""
    return (leer(b.get("hook")) and leer(b.get("caption"))
            and not (b.get("folien") or b.get("slides")))


def was_fehlt(b: dict, art: str) -> tuple[str, str]:
    """Gibt (wer, satz). wer ist 'du', 'claude' oder '' (nichts offen)."""
    if art == "Reel":
        if leer(b.get("videourl")) and leer(b.get("video")):
            # B-Roll baut Claude aus vorhandenem Material, ein Sprechreel
            # muss Patricia drehen.
            if (b.get("videoart") or "").lower() == "broll":
                return "claude", "B-Roll bauen"
            return "du", "Sprechreel drehen — Sprechtext steht auf der Karte"
    if leer(b.get("caption")):
        return "du", "Caption fehlt"
    if art == "Reel" and leer(b.get("hook")):
        return "du", "Hook fehlt"
    if art == "Karussell":
        folien = b.get("folien") or b.get("slides") or []
        if not folien:
            return "du", "Folien fehlen"
    return "", ""


def kurz(b: dict, art: str, satz: str = "") -> dict:
    return {
        "id": b.get("id", ""),
        "name": (b.get("name") or "")[:70],
        "art": art,
        "tag": (b.get("datum") or b.get("tag") or "")[:10],
        "profil": b.get("profil") or "",
        "was": satz,
    }


def main():
    offen_du, offen_claude, fertig, durch, vorrat = [], [], [], [], []
    gesamt = 0
    heute = date.today().isoformat()

    for ordner, art in ARTEN:
        for b in laden(ordner):
            if ist_entwurf(b):
                continue
            gesamt += 1
            e = kurz(b, art)

            # 🚨 **Ohne Datum ist nichts eine Aufgabe** — weder offen noch
            # fertig. Das sind die `vorrat-`-Eintraege UND die A/B/C-Varianten
            # aus der Freitagsproduktion, die auf keinem Platz liegen. Beim
            # ersten Test standen so fuenf „Sprechreel drehen" ganz oben, die
            # in Wahrheit nur nicht ausgewaehlte Varianten waren. Eine Aufgabe,
            # die keine ist, kostet Vertrauen in die ganze Liste.
            if not e["tag"]:
                vorrat.append(e)
                continue

            wer, satz = was_fehlt(b, art)
            if wer == "du":
                e["was"] = satz
                offen_du.append(e)
            elif wer == "claude":
                e["was"] = satz
                offen_claude.append(e)
            elif not b.get("textfrei"):
                # 🚨 Fertig heisst nicht, dass es noch rausgehen kann. Blotato
                # nimmt keinen Zeitpunkt in der Vergangenheit an, und die
                # Freigabe meldet trotzdem „abgelegt". Wer beides in eine Zahl
                # wirft, zaehlt Beitraege mit, die nie rausgehen — am 18.09.
                # waren das 9 von 26.
                if e["tag"] and e["tag"] < heute:
                    e["was"] = "Datum ist durch — neu einplanen"
                    durch.append(e)
                else:
                    fertig.append(e)

    def nach_tag(x):
        return x["tag"] or "9999"

    daten = {
        "stand": datetime.now().isoformat(timespec="seconds"),
        "gesamt": gesamt,
        "offen_du": sorted(offen_du, key=nach_tag),
        "offen_claude": sorted(offen_claude, key=nach_tag),
        "fertig": sorted(fertig, key=nach_tag),
        "datum_durch": sorted(durch, key=nach_tag),
        "vorrat": len(vorrat),
        "quelle": "outputs/cockpit/inhalte-roh (ArtifactData list)",
    }

    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    ZIEL.write_text(json.dumps(daten, ensure_ascii=False, indent=2),
                    encoding="utf-8")

    print("  %d Beiträge gelesen" % gesamt)
    print("    bei dir         %2d" % len(daten["offen_du"]))
    print("    bei Claude      %2d" % len(daten["offen_claude"]))
    print("    kann raus       %2d" % len(daten["fertig"]))
    print("    Datum ist durch %2d" % len(daten["datum_durch"]))
    print("    Vorrat (ohne Datum) %2d" % daten["vorrat"])
    if not gesamt:
        print("\n  ⚠️ Nichts gefunden. Liegt der Abzug in %s?" % ROH)
    print("\nGeschrieben: %s" % ZIEL)


if __name__ == "__main__":
    main()
