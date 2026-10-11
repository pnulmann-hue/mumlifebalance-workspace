"""Auf welche Gedanken, Gefühle und Einwände gehen die Nischen-Konten ein — und welche ziehen?

Patricia am 04.10.2026: *„kannst du in die analyse auch miteinbeziehen, auf was für
gedanken gefühle und einwände die quellen in ihren beiträgen eingehen? weil
kommentare gibt es vielleicht ja nicht so viele.“*

Jede Mentorin in ihrer Nische hat ihre Zielgruppe studiert. Jeder Beitrag greift
einen Gedanken auf, den die Leserin hat. Hier wird das je Beitrag herausgelesen
(Caption + Titelbild-Text), mit dem Faktor gegen den Konto-Median verbunden und
ausgezählt. Dazu die echten Kommentare, wo es welche gibt.

Ergebnis ist der Psychologie-Datensatz **aus Daten** — Ergänzung zu
`context/hook-datensaetze.md`, das aus Kursunterlagen und Interviews stammt.

    python scripts/hooks/themen-analyse.py

Voraussetzung: `bild-hooks.py` und `markt-analyse.py` sind gelaufen (Faktor, Bildtext).
Ausgabe: `outputs/marktrecherche/JJJJ-MM-TT-nische-gedanken.md` + `nische-gedanken.json`.
Die Einordnung je Beitrag wird in `nische-gedanken-cache.json` gemerkt.
"""

import datetime
import glob
import json
import os
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import List, Optional

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "outputs" / "apify-runs"
WATCH = ROOT / "context" / "competitor-watchlist.json"
DB = ROOT / "outputs" / "marktrecherche" / "hook-datenbank.json"
BILD = ROOT / "outputs" / "marktrecherche" / "bild-hooks.json"
ZIEL = ROOT / "outputs" / "marktrecherche"
CACHE = ZIEL / "nische-gedanken-cache.json"
MODELL = "claude-opus-5-5"
STAPEL = 20

ANLEITUNG = """Du liest Instagram-Beiträge von Mentorinnen, die Frauen (oft Mamas, oft Networkerinnen
oder Selbständige) beibringen, mit Social Media zu verkaufen. Für jeden Beitrag (Nummer behalten):

- gedanke: der Gedanke der LESERIN, auf den der Beitrag eingeht — als ihr eigener Satz in Ich-Form,
  so wie sie ihn denken würde (z.B. „Ich poste jeden Tag und keiner reagiert.“). Nicht die Botschaft
  der Mentorin, sondern was die Leserin vorher denkt. Max. 20 Wörter.
- gefuehl: das Gefühl der Leserin dabei, ein Wort (z.B. frust, scham, angst, ueberforderung, neid,
  hoffnung, sehnsucht, zweifel, wut, muedigkeit, neugier, stolz)
- einwand: falls der Beitrag einen Einwand oder eine Ausrede entkräftet, diesen als ihr Satz
  („Ich hab keine Zeit dafür.“) — sonst leer
- sehnsucht: was sie eigentlich will, max. 8 Wörter — sonst leer
- thema: Oberthema in 1–3 Wörtern aus dieser Liste, wenn passend: Reichweite, Kunden gewinnen,
  Verkaufen, Content-Ideen, Zeit & Familie, Selbstzweifel, Sichtbarkeit & Scham, Geld,
  Positionierung, Storys, Reels, KI, Network, Mindset, Persönliches, Angebot
- art: lehrt · erzaehlt · provoziert · verkauft · persoenlich"""


def lies(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return None


def main():
    import anthropic
    from pydantic import BaseModel

    if not os.environ.get("ANTHROPIC_API_KEY"):
        for z in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
            if z.startswith("ANTHROPIC_API_KEY="):
                os.environ["ANTHROPIC_API_KEY"] = z.split("=", 1)[1].strip().strip('"')

    class Eintrag(BaseModel):
        nr: int
        gedanke: str
        gefuehl: str
        einwand: Optional[str] = ""
        sehnsucht: Optional[str] = ""
        thema: str
        art: str

    class Antwort(BaseModel):
        beitraege: List[Eintrag]

    kern = {k["handle"] for k in (lies(WATCH) or {}).get("accounts", []) if k.get("nische") == "kern"}
    faktor = {p.get("sc"): p.get("faktor") for p in (lies(DB) or {}).get("markt", []) if p.get("sc")}
    bild = lies(BILD) or {}
    posts = {}
    for f in sorted(glob.glob(str(RUNS / "tiefe-*.json"))) + sorted(glob.glob(str(RUNS / "competitors-*.json")))[-5:]:
        d = lies(f) or {}
        quelle = d.get("posts") or [p for a in d.get("results", []) for p in (a.get("latestPosts") or [])]
        for p in quelle:
            sc, konto = p.get("shortCode"), p.get("ownerUsername")
            if konto in kern and sc and sc not in posts and not p.get("isPinned"):
                posts[sc] = {
                    "sc": sc, "konto": konto, "datum": (p.get("timestamp") or "")[:10], "link": p.get("url"),
                    "bild": (bild.get(sc) or {}).get("text", ""), "caption": (p.get("caption") or "")[:1500],
                    "kommentare": [c.get("text", "") for c in (p.get("latestComments") or []) if c.get("text")][:15],
                    "faktor": faktor.get(sc),
                }
    print(f"Nischen-Beiträge: {len(posts)} aus {len({p['konto'] for p in posts.values()})} Konten")

    cache = lies(CACHE) or {}
    offen = [p for p in posts.values() if p["sc"] not in cache and (p["bild"] or p["caption"].strip())]
    print(f"neu einzuordnen: {len(offen)}")
    client = anthropic.Anthropic()
    for i in range(0, len(offen), STAPEL):
        teil = offen[i:i + STAPEL]
        text = "\n\n".join(f"### {n}\nTitelbild: {p['bild'] or '—'}\nCaption: {p['caption']}" for n, p in enumerate(teil))
        try:
            r = client.messages.parse(model=MODELL, max_tokens=16000, output_config={"effort": "low"},
                                      system=ANLEITUNG, messages=[{"role": "user", "content": text}], output_format=Antwort)
        except (anthropic.APIStatusError, anthropic.APIConnectionError) as e:
            print(f"  Stapel {i // STAPEL + 1}: Fehler {getattr(e, 'status_code', '')} — übersprungen")
            continue
        if r.stop_reason == "refusal" or r.parsed_output is None:
            continue
        for e in r.parsed_output.beitraege:
            if 0 <= e.nr < len(teil):
                cache[teil[e.nr]["sc"]] = e.model_dump(exclude={"nr"})
        CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  Stapel {i // STAPEL + 1}/{(len(offen) - 1) // STAPEL + 1}")

    zeilen = [dict(p, **cache[p["sc"]]) for p in posts.values() if p["sc"] in cache]
    heute = datetime.date.today().isoformat()
    (ZIEL / "nische-gedanken.json").write_text(json.dumps({"stand": heute, "beitraege": zeilen}, ensure_ascii=False, indent=1), encoding="utf-8")

    # Die Gedanken selbst sind frei formuliert — zum Zusammenfassen bekommt Claude sie gebündelt je Thema
    je_thema = defaultdict(list)
    for z in zeilen:
        je_thema[z["thema"]].append(z)
    tabelle = []
    for t, zs in je_thema.items():
        f = [z["faktor"] for z in zs if z.get("faktor") is not None]
        tabelle.append((t, len(zs), round(statistics.median(f), 2) if len(f) >= 5 else None))
    tabelle.sort(key=lambda x: -x[1])

    eingabe = []
    for t, n, m in tabelle:
        zs = sorted(je_thema[t], key=lambda z: -(z.get("faktor") or 0))
        eingabe.append(f"## Thema: {t} ({n} Beiträge, Median-Faktor {m})\n" + "\n".join(
            f"- [{z.get('faktor')}] Gedanke: {z['gedanke']} | Gefühl: {z['gefuehl']} | Einwand: {z.get('einwand') or '—'} | Sehnsucht: {z.get('sehnsucht') or '—'}"
            for z in zs[:60]))
    kommentare = [c for z in zeilen for c in z["kommentare"] if len(c.split()) >= 4][:400]
    auftrag = ("Fasse zusammen, was die Zielgruppe dieser Nische denkt und fühlt. Zahlen in eckigen Klammern sind der "
               "Faktor des Beitrags gegen den Durchschnitt seines Kontos (1,0 = normal).\n\n"
               "Liefere auf Deutsch (Schweizer ss, keine ß), als Markdown:\n"
               "1. **Die 15 häufigsten Gedanken** als ihr Satz in Ich-Form, je mit: wie oft (ungefähr), typisches Gefühl, "
               "ob Beiträge dazu über oder unter dem Durchschnitt lagen.\n"
               "2. **Die 10 häufigsten Einwände/Ausreden** als ihr Satz, je mit wie oft und wie die Mentorinnen antworten (Mechanik, ein Satz).\n"
               "3. **Sehnsüchte** — die 8 häufigsten.\n"
               "4. **Was zieht, was nicht** — welche Gedanken/Gefühle stehen bei den Beiträgen mit hohem Faktor, welche bei den schwachen.\n"
               "5. **Aus den Kommentaren**: wiederkehrende Sätze, Fragen, Wörter der Leserinnen (wörtlich zitieren, nur was wirklich dasteht).\n"
               "Nichts erfinden. Wenn eine Aussage dünn belegt ist, das dazusagen.\n\n"
               + "\n\n".join(eingabe) + "\n\n## Kommentare der Leserinnen\n" + "\n".join(f"- {c[:200]}" for c in kommentare))
    # Gestreamt und mit viel Luft: mit 16'000 brach die Zusammenfassung am 04.10. mitten in Teil 3 ab
    with client.messages.stream(model=MODELL, max_tokens=64000, output_config={"effort": "medium"},
                                messages=[{"role": "user", "content": auftrag}]) as s:
        r = s.get_final_message()
    zusammenfassung = "".join(b.text for b in r.content if b.type == "text")
    if r.stop_reason == "max_tokens":
        zusammenfassung += "\n\n⚠️ Abgeschnitten (max_tokens)."

    konten = sorted({z["konto"] for z in zeilen})
    L = ["---", "tags: [research, hooks, zielgruppe]", "---", "", f"# Was die Zielgruppe denkt — aus den Beiträgen deiner Nische · {heute}", "",
         f"**Grundlage:** {len(zeilen)} Beiträge von {', '.join(konten)}. Je Beitrag hat Claude herausgelesen, auf welchen Gedanken, "
         "welches Gefühl und welchen Einwand der Leserin er eingeht, und das mit dem Faktor gegen den Konto-Durchschnitt verbunden. "
         f"Dazu {len(kommentare)} echte Kommentare.", "",
         "⚠️ Das sind die Gedanken, die **die Mentorinnen** ihrer Zielgruppe zuschreiben — gut belegt, weil sie davon leben, "
         "aber keine Umfrage. Wortlaut der Leserinnen steht nur im Kommentar-Teil.", "",
         "## Themen nach Häufigkeit", "", "| Thema | Beiträge | Median-Faktor |", "|---|---:|---:|"]
    L += [f"| {t} | {n} | {m if m is not None else '–'} |" for t, n, m in tabelle]
    L += ["", zusammenfassung, "", "---", "", "## 🔗 Verwandte Notizen", "", "- [[hook-datensaetze]]",
          "- [[2026-10-04-hook-markt-analyse]]", "- [[2026-10-04-hook-maschine]]", ""]
    pfad = ZIEL / f"{heute}-nische-gedanken.md"
    pfad.write_text("\n".join(L), encoding="utf-8")
    print(f"→ {pfad.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
