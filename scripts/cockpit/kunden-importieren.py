"""Holt Kundinnen und Kundenstimmen **einmalig** ins Cockpit.

Patricia am 24.09.2026: *„auch das mit den kunden soll rein bitte"* und
*„auch testimonials"*.

🚨 **Personendaten.** Die Namen stehen in `kunden-roh.json` daneben, nicht in
diesem Skript — dieselbe Regel wie seit dem 13.09.: Daten anderer Menschen
gehoeren in eine ausgeschlossene Datei, die das Skript liest, nie in den Code.
Beide Ordner (`scripts/cockpit/` und `outputs/cockpit/abgleich/`) sind
gitignored; nichts davon landet im oeffentlichen Repo.

🚨 **Telefon, Adresse, Geburtstag und URL sind nicht uebernommen.** Nicht aus
Vorsicht — sie waren in Notion bei **allen 34** Eintraegen leer. Ein Feld, das
nie gefuellt wurde, ins Cockpit zu heben heisst, eine Spalte zu bauen, die
dauerhaft leer aussieht und trotzdem nach sensiblen Daten verlangt.

🚨 **Die Notion-Testimonial-Datenbank ist faktisch leer**: drei Eintraege, davon
einer „Super Kurs!", einer nur ein Vorname mit Screenshots, einer ganz ohne
Text. Die **echten** Kundenstimmen stehen in der MBA-Salespage — mit Namen und
Instagram-Handle, und die Seite ist oeffentlich, also sind sie freigegeben.
Deshalb liest dieses Skript sie **von dort**.

    python scripts/cockpit/kunden-importieren.py
    # danach: ArtifactData set -> daten/leads und daten/stimmen
"""

import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
SALESPAGES = [
    ROOT / "outputs" / "produkte" / "mba-launch" / "mba-salespage.html",
]

# Notion-Status -> die Stufen, die der Leads-Reiter schon kennt.
STATUS = {"Aktiv": "Kundin", "Potenziell": "Neu"}


def kontakte(ziel: Path) -> list:
    p = ziel / "kunden-roh.json"
    if not p.exists():
        print("  ⚠️ kunden-roh.json fehlt — keine Kontakte übernommen.")
        return []
    d = json.loads(p.read_text(encoding="utf-8"))
    raus = []
    for i, k in enumerate(d.get("kontakte") or []):
        name = (k.get("name") or "").strip()
        if not name:
            continue
        raus.append({
            "id": "kd%03d" % i,
            "name": name,
            # 🚨 „Quelle" heisst im Leads-Reiter: woher kam der Kontakt. Die
            # Notion-Kategorie (Kunde/Kooperation/Dienstleister) ist etwas
            # anderes und bekommt ein eigenes Feld.
            "quelle": "Sonstiges",
            "kategorie": k.get("kategorie") or "Kunde",
            "email": k.get("email") or "",
            "interesse": k.get("produkt") or "",
            "status": STATUS.get(k.get("status"), "Neu"),
            "schritt": "",
            "notiz": k.get("notiz") or "",
            "datum": k.get("von") or "",
        })
    return raus


def stimmen() -> list:
    """Kundenstimmen aus den Salespages. Nur, was oeffentlich steht."""
    raus = []
    for p in SALESPAGES:
        if not p.exists():
            continue
        h = p.read_text(encoding="utf-8")
        # 🚨 Auf die HTML-Struktur matchen, nicht auf Anfuehrungszeichen.
        # Der erste Versuch suchte nach „…“ und fand **null** Treffer, weil
        # oeffnendes und schliessendes Zeichen im Dokument nicht das Paar sind,
        # das man erwartet. Die Struktur dagegen ist eindeutig:
        #   <div class="testi …">TEXT<span class="who">— Name · @handle</span></div>
        for m in re.finditer(
                r'<div class="testi[^"]*">(.*?)<span class="who">\s*[—-]\s*(.*?)</span>',
                h, re.S):
            text = m.group(1)
            wer = re.sub(r"<[^>]+>", " ", m.group(2))
            teile = [t.strip() for t in wer.split("·")]
            name = teile[0] if teile else ""
            handle = next((t for t in teile[1:] if t.startswith("@")), "")
            text = re.sub(r"<[^>]+>", " ", text)
            text = text.strip().strip("„“”\"")
            text = re.sub(r"\s+", " ", text).strip()
            if not text:
                continue
            raus.append({
                "id": "st%03d" % len(raus),
                "text": text,
                "name": name,
                "handle": handle,
                "quelle": p.name,
                # Die Salespage ist oeffentlich — was dort steht, ist freigegeben.
                "freigegeben": True,
            })
    return raus


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    ks = kontakte(ziel)
    sts = stimmen()

    (ziel / "leads.json").write_text(json.dumps(
        {"items": ks, "stand": date.today().isoformat(),
         "quelle": "Notion «Kunden und Kontakte», einmalig übernommen",
         "gebaut": datetime.now().isoformat(timespec="seconds")},
        ensure_ascii=False, indent=2), encoding="utf-8")

    (ziel / "stimmen.json").write_text(json.dumps(
        {"items": sts, "stand": date.today().isoformat(),
         "quelle": "Salespages (öffentlich) + Notion-Testimonials",
         "hinweis": "Nur was öffentlich auf einer Salespage steht, gilt als "
                    "freigegeben. Alles andere gehört hier nicht hinein.",
         "gebaut": datetime.now().isoformat(timespec="seconds")},
        ensure_ascii=False, indent=2), encoding="utf-8")

    print("  %d Kontakte übernommen" % len(ks))
    nach_kat = {}
    for k in ks:
        nach_kat[k["kategorie"]] = nach_kat.get(k["kategorie"], 0) + 1
    print("     %s" % " · ".join("%s %d" % kv for kv in sorted(nach_kat.items())))
    print("     %d mit E-Mail, %d mit Produkt, %d mit Zeitraum"
          % (len([k for k in ks if k["email"]]),
             len([k for k in ks if k["interesse"]]),
             len([k for k in ks if k["datum"]])))
    print("  %d Kundenstimmen aus den Salespages" % len(sts))
    for s in sts:
        print("     %s%s: %s…" % (s["name"], " " + s["handle"] if s["handle"] else "",
                                  s["text"][:58]))
    print("\nAbgelegt in: %s, %s" % (ziel / "leads.json", ziel / "stimmen.json"))


if __name__ == "__main__":
    main()
