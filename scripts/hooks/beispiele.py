"""Das Beispiel-Paket für die Hook-Maschine — was Claude vor dem Schreiben sieht.

Das ist Apelis „Gehirn“, nur mit Patricias eigenen Zahlen: statt 2'000 fremder
viraler Posts die Hooks, die **bei ihr** und **in ihrer Nische** nachweislich
getragen haben, plus die Regeln, die sich daraus gerade ergeben. Die Regeln
werden bei jedem Lauf neu aus der Datenbank gerechnet, nicht abgeschrieben —
ändert sich, was trägt, ändert sich das Paket mit.

    python scripts/hooks/beispiele.py --profil mentoring
    python scripts/hooks/beispiele.py --profil mentoring --thema "Mama Zeit Haushalt" --ziel lead

Voraussetzung: `markt-analyse.py` und `verkaufsdaten.py` sind gelaufen.
Gelesen wird von `/content` Schritt 4 und vom Modus „Maschine“ im Hook-Skill.
"""

import argparse
import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "outputs" / "marktrecherche" / "hook-datenbank.json"
VK = ROOT / "outputs" / "marktrecherche" / "hook-verkaufsdaten.json"
MIN = 8
# reine Gewinnspiel-, Begrüssungs- und Firmenmeldungen sind kein Vorbild
RAUSCHEN = re.compile(r"gewinnspiel|türchen|schön,? dass du (mich )?hier|willkommen auf meinem|danke für \d|anpfiff|produkt-highlights", re.I)


def lies(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        sys.exit(f"Fehlt: {p} — zuerst scripts/hooks/markt-analyse.py und verkaufsdaten.py laufen lassen.")


def woerter(t):
    return {w for w in re.findall(r"[a-zäöüß]{4,}", t.lower())}


def passt(p, thema):
    if not thema:
        return 0
    return len(woerter(thema) & (woerter(p["hook"]) | woerter(p.get("thema", ""))))


def regeln(eigen, markt):
    """Welche Werte je Merkmal bei ihr und im Markt vorne/hinten liegen."""
    out = []
    for k, name in (("angle", "Angle"), ("stufe", "Stufe"), ("form", "Form"), ("emotion", "Gefühl"), ("frage", "Frage in Zeile 1")):
        for wer, gruppe in (("bei dir", eigen), ("im Markt", markt)):
            je = defaultdict(list)
            for p in gruppe:
                if k in p and p.get("faktor") is not None:
                    je[str(p[k])].append(p["faktor"])
            z = sorted(((w, len(f), statistics.median(f)) for w, f in je.items() if len(f) >= MIN), key=lambda t: -t[2])
            if len(z) == 2:
                out.append(f"- **{name} {wer}:** " + " · ".join(f"{w} {m:.2f}" for w, n, m in z))
            elif len(z) > 2:
                top = ", ".join(f"{w} {m:.2f}" for w, n, m in z[:2])
                flop = ", ".join(f"{w} {m:.2f}" for w, n, m in z[-2:])
                out.append(f"- **{name} {wer}:** vorne {top} · hinten {flop}")
    return out


def zeile(p, mit_konto=False):
    k = f"{p['konto']} · " if mit_konto else ""
    return f"- „{p['hook'][:180]}“ — {k}Faktor {p['faktor']} · {p.get('form', '?')} · {p.get('angle', '?')} · Stufe {p.get('stufe', '?')}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profil", default="mentoring", choices=["mentoring", "doterra"])
    ap.add_argument("--thema", default="")
    ap.add_argument("--ziel", default="beides", choices=["reichweite", "lead", "beides"])
    ap.add_argument("--anzahl", type=int, default=15)
    a = ap.parse_args()

    db = lies(DB)
    eigen = [p for p in db["eigen"] if p["profil"] == a.profil and p.get("faktor") is not None]
    markt = [p for p in db["markt"] if p["profil"] == a.profil and not RAUSCHEN.search(p["hook"])]
    sortiert = lambda ps: sorted(ps, key=lambda p: (-passt(p, a.thema), -p["faktor"]))

    print(f"# Hook-Beispiel-Paket · {a.profil} · Stand {db['stand']}")
    if a.thema:
        print(f"*Thema: {a.thema} — passende Hooks stehen vorne, danach die stärksten insgesamt.*")
    print("\nFaktor = so viel besser als sonst beim selben Konto (1,0 = normal). Hooks sind Vorbilder für die **Mechanik**, "
          "nie zum Abschreiben: Szene, Zahlen und Worte kommen aus Patricias Leben.\n")

    print("## Was gerade trägt (aus den Zahlen gerechnet)\n")
    print("\n".join(regeln(eigen, markt)) or "- zu wenig Daten")

    if not eigen:
        print("\n⚠️ Für dieses Profil gibt es keine eigenen Zahlen (Konto nicht an der Schnittstelle). Nur Markt-Vorbilder.")
    else:
        gut = [p for p in eigen if p["faktor"] >= 1.5]
        print(f"\n## Deine Gewinner ({len(gut)} Beiträge ≥ 1,5×)\n")
        print("\n".join(zeile(p) for p in sortiert(gut)[:a.anzahl]))
        schlecht = sorted(eigen, key=lambda p: p["faktor"])[:6]
        print("\n## So nicht — deine schwächsten\n")
        print("\n".join(zeile(p) for p in schlecht))

    kern = [p for p in markt if p.get("nische") == "kern" and p["faktor"] >= 1.5]
    if kern:
        print(f"\n## Deine Nische — von dir benannte Konten ({len(kern)} Beiträge ≥ 1,5×)\n")
        print("*Zählt vor dem übrigen Markt. „Bildtext“ = der Hook stand auf dem Titelbild.*\n")
        print("\n".join(zeile(p, True) + (" · Bildtext" if p.get("hook_quelle") == "bild" else "") for p in sortiert(kern)[:a.anzahl]))
    gut_m = [p for p in markt if p["faktor"] >= 2 and p.get("nische") != "kern"]
    print(f"\n## Übriger Markt — nur als Anregung ({len(gut_m)} Beiträge ≥ 2× ihres Kontos)\n")
    print("\n".join(zeile(p, True) for p in sortiert(gut_m)[:max(5, a.anzahl // 2)]))

    if a.ziel in ("lead", "beides") and a.profil == "mentoring":  # Stichwörter und Lead-Zahlen gibt es nur fürs Mentoring
        vk = lies(VK)
        leads = [p for p in vk["leads"] if p["profil"] == a.profil and p.get("kommentare")]
        print("\n## Lead-Beiträge: welche Hooks holen Kommentare\n")
        n0 = sum(1 for p in vk["leads"] if p["profil"] == a.profil and not p.get("kommentare"))
        print(f"*{n0} von {n0 + len(leads)} Lead-Beiträgen hatten null Kommentare. Ein Lead-Beitrag beginnt mit IHREM Satz, nicht mit dem Angebot.*\n")
        for p in sorted(leads, key=lambda p: -p["kommentar_rate"])[:8]:
            print(f"- „{p['hook'][:160]}“ — {p['kommentar_rate']} Kommentare je 100 · Stichwort {p['keyword']} · {p.get('angle', '?')} · Stufe {p.get('stufe', '?')}")
        kws = sorted((k for k in vk["stichwoerter"] if k.get("je_beitrag")), key=lambda k: -k["je_beitrag"])
        if kws:
            print("\n**Stichwörter nach Eintragungen je Beitrag:** " + " · ".join(f"{k['keyword']} {k['je_beitrag']}" for k in kws))


if __name__ == "__main__":
    main()
