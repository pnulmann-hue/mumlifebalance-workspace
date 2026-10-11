"""Packt alles fuer die Steuererklaerung in einen Ordner — auf einen Befehl.

Patricia am 24.09.2026: *„wäre da richtig geil, wenn wir ende jahr eine option
hätten, dass ich per knopfdruck die daten rauslassen kann für meine
steuererklärung"*.

    python scripts/finanzen/steuer-export.py            # laufendes Jahr
    python scripts/finanzen/steuer-export.py 2026 --zip

Heraus kommt `outputs/finanzen/steuer-JJJJ/`:

| Datei | Inhalt |
|---|---|
| `00-uebersicht.md` | Einnahmen, Ausgaben, was fehlt — zum Lesen |
| `01-einnahmen.csv` | jeder Umsatztag einzeln |
| `02-ausgaben.csv` | jeder Kostenposten mit Belegdatei daneben |
| `03-was-fehlt.md` | die Luecken, schwarz auf weiss |
| `belege/` | Kopien der Originalbelege |

🚨 **Das ist keine Steuererklaerung, sondern die Unterlage dafuer.** Was
abzugsfaehig ist und wie der private Anteil eines Abos behandelt wird,
entscheidet die Treuhaenderin oder das Steueramt — nicht dieses Skript.

🚨 **Keine Zahl ohne Herkunft.** Jede Zeile traegt in der Spalte `quelle`, wo
sie herkommt: ThriveCart, Belegordner, Meta-Werbekonto, Belege-Index oder
Notion. Eine Zahl, deren Herkunft niemand mehr kennt, ist bei einer Nachfrage
wertlos.

🚨 **USD wird NICHT umgerechnet.** Der Frankenbetrag steht auf der
Kreditkartenabrechnung und weicht vom Tageskurs ab. Beide Waehrungen werden
getrennt summiert, und die Uebersicht sagt es ausdruecklich. Ein selbst
umgerechneter Betrag sieht aus wie ein belegter.

🚨 **Kein Gewinn, wo Kosten fehlen.** Dieselbe Regel wie im Monatsbogen: eine
fehlende Zahl merkt man, eine zu hohe nicht.

🚨 **Keine Kundendaten.** Die Einnahmen werden nach Tag zusammengefasst. Namen,
Mailadressen und Rechnungsadressen der Kundinnen liegen in ThriveCart und
bleiben dort — dieser Export wird weitergegeben.
"""

import csv
import json
import shutil
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
ABGLEICH = ROOT / "outputs" / "cockpit" / "abgleich"
BELEGE = ROOT / "context" / "finanzen" / "2026" / "belege"


def lade(name):
    p = ABGLEICH / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def fr(x):
    """Schweizer Zahlenschreibweise: 1'234.50"""
    return format(x, ",.2f").replace(",", "'")


def schreibe_csv(pfad, kopf, zeilen):
    # Semikolon und BOM, weil Excel auf Deutsch sonst alles in eine Spalte legt.
    with open(pfad, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(kopf)
        w.writerows(zeilen)


def main():
    jahr = str(date.today().year)
    for a in sys.argv[1:]:
        if a.isdigit() and len(a) == 4:
            jahr = a
    zippen = "--zip" in sys.argv

    umsatz = lade("umsatz.json")
    kosten = lade("kosten.json")
    if not umsatz or not kosten:
        sys.exit("umsatz.json oder kosten.json fehlt — erst die Bauskripte "
                 "laufen lassen:\n"
                 "  python scripts/cockpit/umsatz-bauen.py\n"
                 "  python scripts/finanzen/meta-werbekosten.py\n"
                 "  python scripts/cockpit/kosten-bauen.py")

    ziel = ROOT / "outputs" / "finanzen" / ("steuer-%s" % jahr)
    if ziel.exists():
        shutil.rmtree(ziel)
    (ziel / "belege").mkdir(parents=True)

    # ---------- Einnahmen ----------
    tage = [t for t in (umsatz.get("tage") or [])
            if (t.get("datum") or "").startswith(jahr)]
    tage.sort(key=lambda t: t["datum"])
    einnahmen = sum(t["umsatz"] for t in tage)
    kaeufe = sum(t.get("kaeufe") or 0 for t in tage)
    whr_u = umsatz.get("waehrung") or "CHF"

    schreibe_csv(ziel / "01-einnahmen.csv",
                 ["Datum", "Betrag", "Waehrung", "Kaeufe", "Quelle"],
                 [[t["datum"], "%.2f" % t["umsatz"], whr_u,
                   t.get("kaeufe") or 0, "ThriveCart"] for t in tage])

    produkte = [p for p in (umsatz.get("produkte") or []) if p.get("umsatz")]
    produkte.sort(key=lambda p: -p["umsatz"])

    # ---------- Ausgaben ----------
    posten = [p for p in (kosten.get("posten") or [])
              if (p.get("monat") or "").startswith(jahr)]
    posten.sort(key=lambda p: (p.get("datum") or p["monat"], p["was"]))

    zeilen, kopiert, fehlend = [], set(), []
    for p in posten:
        dateien = p.get("belege") or []
        for d in dateien:
            q = BELEGE / d
            if q.exists():
                shutil.copy2(q, ziel / "belege" / d)
                kopiert.add(d)
        if not dateien:
            fehlend.append(p)
        zeilen.append([
            p.get("datum") or (p["monat"] + "-01"),
            p["was"],
            p["art"],
            "%.2f" % p["betrag"],
            p["waehrung"],
            " | ".join(dateien) if dateien else "FEHLT",
            p.get("quelle") or "",
        ])
    schreibe_csv(ziel / "02-ausgaben.csv",
                 ["Datum", "Was", "Kategorie", "Betrag", "Waehrung",
                  "Beleg", "Quelle"], zeilen)

    chf = sum(p["betrag"] for p in posten if p["waehrung"] == "CHF")
    usd = sum(p["betrag"] for p in posten if p["waehrung"] == "USD")
    andere = defaultdict(float)
    for p in posten:
        if p["waehrung"] not in ("CHF", "USD"):
            andere[p["waehrung"]] += p["betrag"]

    nach_art = defaultdict(lambda: defaultdict(float))
    for p in posten:
        nach_art[p["art"]][p["waehrung"]] += p["betrag"]

    # ---------- Uebersicht ----------
    z = []
    z.append("---\ntags: [finanzen, steuern, intern]\n---\n")
    z.append("# Steuer-Unterlage %s — Mum Life Balance\n" % jahr)
    z.append("**Erstellt:** %s · **Stand der Zahlen:** Umsatz %s · Kosten %s\n"
             % (date.today().isoformat(), umsatz.get("stand", "?"),
                kosten.get("stand", "?")))
    z.append("> 🚨 Das ist die **Unterlage** für die Steuererklärung, nicht die "
             "Steuererklärung. Was abzugsfähig ist und wie ein privat "
             "mitbenutztes Abo behandelt wird, entscheidet die Treuhänderin.\n")
    z.append("---\n")
    z.append("## Einnahmen\n")
    z.append("| | |\n|---|---:|")
    z.append("| Umsatz %s | **%s %s** |" % (jahr, whr_u, fr(einnahmen)))
    z.append("| Anzahl Käufe | %d |" % kaeufe)
    z.append("| Verkaufstage | %d |" % len(tage))
    z.append("\n**Quelle:** ThriveCart, alle Transaktionen des Jahres. "
             "Zusammengefasst nach Tag — Kundennamen und -adressen bleiben in "
             "ThriveCart und sind hier bewusst nicht drin.\n")
    if produkte:
        z.append("### Nach Produkt\n")
        z.append("| Produkt | Umsatz | Käufe |\n|---|---:|---:|")
        for p in produkte[:20]:
            z.append("| %s | %s | %d |" % (p["name"], fr(p["umsatz"]),
                                           p.get("kaeufe") or 0))
        z.append("")
    z.append("---\n")
    z.append("## Ausgaben\n")
    z.append("| Kategorie | CHF | USD |\n|---|---:|---:|")
    for art in sorted(nach_art):
        z.append("| %s | %s | %s |"
                 % (art,
                    fr(nach_art[art].get("CHF", 0)) if nach_art[art].get("CHF") else "—",
                    fr(nach_art[art].get("USD", 0)) if nach_art[art].get("USD") else "—"))
    z.append("| **Total** | **%s** | **%s** |" % (fr(chf), fr(usd)))
    for w, b in sorted(andere.items()):
        z.append("| Total %s | | %s |" % (w, fr(b)))
    z.append("")
    z.append("🚨 **Die USD-Beträge sind nicht umgerechnet.** Der echte "
             "Frankenbetrag steht auf der Kreditkartenabrechnung und weicht "
             "vom Tageskurs ab. Wer hier selbst umrechnet, schreibt eine Zahl "
             "hin, die aussieht wie belegt und keine ist.\n")
    z.append("---\n")
    z.append("## Ergebnis\n")
    if fehlend:
        z.append("**Kein Gewinn ausgewiesen.** %d von %d Kostenposten haben "
                 "keinen Beleg, und für einige Monate fehlen Kosten ganz. "
                 "Einnahmen minus unvollständige Kosten ergäbe einen Gewinn, "
                 "der zu hoch ist — siehe `03-was-fehlt.md`.\n"
                 % (len(fehlend), len(posten)))
        z.append("| | |\n|---|---:|")
        z.append("| Einnahmen | %s %s |" % (whr_u, fr(einnahmen)))
        z.append("| Ausgaben CHF (unvollständig) | %s |" % fr(chf))
        z.append("| Ausgaben USD (unvollständig) | %s |" % fr(usd))
        z.append("| Gewinn | **wird erst gerechnet, wenn die Kosten stehen** |")
    else:
        z.append("| | |\n|---|---:|")
        z.append("| Einnahmen | %s %s |" % (whr_u, fr(einnahmen)))
        z.append("| Ausgaben CHF | %s |" % fr(chf))
        z.append("| Ausgaben USD | %s (nicht umgerechnet) |" % fr(usd))
    z.append("\n---\n")
    z.append("## Was in diesem Ordner liegt\n")
    z.append("| Datei | Inhalt |\n|---|---|")
    z.append("| `01-einnahmen.csv` | jeder Umsatztag einzeln |")
    z.append("| `02-ausgaben.csv` | jeder Kostenposten, Spalte «Beleg» nennt die Datei |")
    z.append("| `03-was-fehlt.md` | die Lücken |")
    z.append("| `belege/` | %d Originalbelege |" % len(kopiert))
    (ziel / "00-uebersicht.md").write_text("\n".join(z), encoding="utf-8")

    # ---------- Was fehlt ----------
    f = []
    f.append("---\ntags: [finanzen, steuern, intern]\n---\n")
    f.append("# Was für %s noch fehlt\n" % jahr)
    f.append("Diese Liste steht bewusst im Export. Eine Unterlage, die ihre "
             "eigenen Lücken verschweigt, ist gefährlicher als eine, die keine "
             "hat.\n")
    f.append("## 1 · Posten ohne Belegdatei — %d von %d\n"
             % (len(fehlend), len(posten)))
    if fehlend:
        f.append("Die Zahl ist erfasst, das Dokument nicht. Bei einer "
                 "Nachfrage vom Steueramt zählt das Dokument.\n")
        f.append("| Monat | Was | Betrag | Woher die Zahl kommt |\n|---|---|---:|---|")
        for p in fehlend:
            f.append("| %s | %s | %s %s | %s |"
                     % (p["monat"], p["was"], p["waehrung"],
                        fr(p["betrag"]), p.get("quelle") or "?"))
        f.append("")
        werbung = [p for p in fehlend if p["art"] == "Werbung"]
        if werbung:
            f.append("🚨 **Die Werbekosten holst du im Business Manager** unter "
                     "Abrechnung: https://business.facebook.com/billing_hub/accounts "
                     "— die Schnittstelle gibt die Rechnungen nicht heraus, nur "
                     "die Beträge.\n")
    else:
        f.append("Keiner. Jeder Posten hat eine Datei.\n")

    luecken = [m for m in (kosten.get("luecken") or []) if m.startswith(jahr)]
    f.append("## 2 · Monate mit Umsatz, aber ohne erfasste Kosten\n")
    if luecken:
        f.append("In diesen Monaten lief Umsatz, aber es ist keine einzige "
                 "Ausgabe verbucht. Das ist unwahrscheinlich — Abos laufen "
                 "weiter, auch wenn niemand hinschaut.\n")
        f.append("· " + " · ".join(luecken) + "\n")
    else:
        f.append("Keine.\n")

    f.append("## 3 · Was dieses System nicht sieht\n")
    f.append("| | |\n|---|---|")
    f.append("| **Bank und Kreditkarte** | Schweizer Banken haben keine offene "
             "Schnittstelle. Der Auszug ist die einzige Stelle, an der die "
             "echten Frankenbeträge der USD-Abos stehen. |")
    f.append("| **Barauslagen** | Porto, Material, Fahrten — davon weiss keine "
             "Schnittstelle etwas. |")
    f.append("| **Privatanteile** | Handy, Internet, Arbeitszimmer. Gehört der "
             "Treuhänderin vorgelegt, nicht hier entschieden. |")
    f.append("| **Rechnungen ohne Mail** | Alles, was nur im Kundenportal des "
             "Anbieters liegt. |")
    (ziel / "03-was-fehlt.md").write_text("\n".join(f), encoding="utf-8")

    # ---------- optional packen ----------
    archiv = ""
    if zippen:
        archiv = shutil.make_archive(str(ziel), "zip", str(ziel))

    print("  Steuer-Unterlage %s" % jahr)
    print("  ─────────────────────────────────────────────")
    print("  Einnahmen         %s %12s   (%d Käufe an %d Tagen)"
          % (whr_u, fr(einnahmen), kaeufe, len(tage)))
    print("  Ausgaben CHF          %12s" % fr(chf))
    print("  Ausgaben USD          %12s   nicht umgerechnet" % fr(usd))
    print("  Belege kopiert        %12d" % len(kopiert))
    print("  Posten ohne Beleg     %12d von %d" % (len(fehlend), len(posten)))
    print()
    print("  %s" % ziel)
    if archiv:
        print("  %s" % archiv)


if __name__ == "__main__":
    main()
