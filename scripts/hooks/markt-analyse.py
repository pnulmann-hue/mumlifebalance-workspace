"""Was im Markt funktioniert — und was davon bei Patricia funktioniert.

Patricia am 04.10.2026 nach dem Apeli-Webinar: *„mir gefällt die umfassende
analyse die ihr gemacht hat, was im markt funktioniert etc. und daraus dann die
hooks baut"*. Das hier ist Baustein 3 aus dem Plan
`plans/2026-10-04-hook-maschine.md`: die Wissensdatenbank — aus echten Zahlen,
nicht aus „2'000 viralen Posts“, die niemand gezeigt hat.

**Drei Quellen:**

| Quelle | Was gemessen wird |
|---|---|
| eigene Beiträge (`gepostet-voll.json`) | Reichweite gegen den eigenen Median |
| Konkurrenz-Scrape (`apify-runs/competitors-*`) | Aufrufe (Reels) bzw. Likes+Kommentare gegen den Median **des jeweiligen Kontos** |
| Hashtag-Discovery (`apify-runs/discovery-*`) | Likes+Kommentare gegen den Median des Kontos |

🚨 **Nie absolut vergleichen.** Ein Konto mit 40'000 Followern hat immer mehr
Likes. Jeder Beitrag zählt nur gegen sein eigenes Konto (Faktor).
🚨 **Mindestbasis:** Konto ab 6 Beiträgen, Beitrag ab 15 Interaktionen bzw.
200 Aufrufen — darunter misst die Quote Zufall.
🚨 **Der Hook ist die erste Caption-Zeile.** Der Text im Video kann abweichen,
Video und Thema wirken mit. Der Bericht sagt das dazu.

Etiketten (Form, Angle, Bewusstseinsstufe, konkret ja/nein …) setzt Claude im
Stapel; sie werden in `outputs/marktrecherche/hook-etiketten-cache.json`
gemerkt, ein zweiter Lauf kostet nur die neuen Hooks.

    python scripts/hooks/markt-analyse.py            # alles
    python scripts/hooks/markt-analyse.py --ohne-ki  # nur Regel-Merkmale

Ausgabe: `outputs/marktrecherche/hook-datenbank.json` und
`outputs/marktrecherche/JJJJ-MM-TT-hook-markt-analyse.md`.
"""

import argparse
import datetime
import glob
import hashlib
import json
import os
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import List, Literal

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "outputs" / "apify-runs"
EIGEN = ROOT / "outputs" / "cockpit" / "abgleich" / "gepostet-voll.json"
WATCH = ROOT / "context" / "competitor-watchlist.json"
ZIEL = ROOT / "outputs" / "marktrecherche"
CACHE = ZIEL / "hook-etiketten-cache.json"
BILD = ZIEL / "bild-hooks.json"   # Text auf dem Titelbild, gelesen von bild-hooks.py

EIGENE = {"mumlifebalance_patricia_ulmann": "mentoring", "patricia_ulmann": "doterra"}
MIN_BEITRAEGE = 6
MIN_INTERAKTIONEN = 15
MIN_AUFRUFE = 200
MIN_GRUPPE = 8          # darunter steht eine Merkmals-Zeile nicht im Bericht
MODELL = "claude-opus-5-5"
STAPEL = 60


# ---------------------------------------------------------------- Hilfen

def lies(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return None


def hook_aus(caption):
    """Erste Zeile der Caption, ohne Rand-Emojis, höchstens 220 Zeichen."""
    if not caption:
        return ""
    zeilen = [z.strip() for z in caption.replace("\r", "").split("\n") if z.strip()]
    if not zeilen:
        return ""
    h = zeilen[0]
    # sehr kurze erste Zeile (z.B. nur ein Emoji oder „POV:“) mit der zweiten verbinden
    if len(re.sub(r"\W", "", h)) < 12 and len(zeilen) > 1:
        h = h + " " + zeilen[1]
    h = re.sub(r"\*\*", "", h)
    return h[:220].strip()


def profil_raten(handle, text=""):
    t = (handle + " " + text[:300]).lower()
    if any(w in t for w in ("doterra", "oel", "öl", "oil", "aroma", "terra")):
        return "doterra"
    return "mentoring"


def median_faktoren(posts, wert):
    """Hängt je Beitrag faktor = wert / Median seines Kontos an."""
    je = defaultdict(list)
    for p in posts:
        if wert(p) is not None:
            je[p["konto"]].append(wert(p))
    med = {k: statistics.median(v) for k, v in je.items() if len(v) >= MIN_BEITRAEGE and statistics.median(v) > 0}
    for p in posts:
        w = wert(p)
        if w is not None and p["konto"] in med:
            p["faktor"] = round(w / med[p["konto"]], 2)
            p["median_konto"] = med[p["konto"]]
    return med


# ---------------------------------------------------------------- Quellen

def eigene_beitraege():
    d = lies(EIGEN) or {}
    out = []
    for b in d.get("beitraege", []):
        if not b.get("reif") or b.get("alte_positionierung") or not b.get("reach"):
            continue
        h = hook_aus(b.get("anfang") or "")
        if len(h) < 12:
            continue
        out.append({
            "quelle": "eigen", "konto": b["handle"], "profil": EIGENE.get(b["handle"], "mentoring"),
            "hook": h, "typ": b.get("typ"), "datum": (b.get("datum") or "")[:10],
            "link": b.get("link"), "wert": b["reach"], "masz": "Reichweite",
            "faktor": b.get("faktor"), "saves": b.get("saved") or 0, "shares": b.get("shares") or 0,
        })
    return out


def markt_beitraege():
    konten = (lies(WATCH) or {}).get("accounts", [])
    watch = {a["handle"]: a.get("profile") for a in konten}
    nische = {a["handle"]: a.get("nische", "umfeld") for a in konten}
    bild = lies(BILD) or {}
    posts = {}
    # Konkurrenz-Scrape: jüngste Beobachtung je Beitrag gewinnt
    for f in sorted(glob.glob(str(RUNS / "competitors-*.json"))):
        d = lies(f)
        if not d:
            continue
        for a in d.get("results", []):
            for p in a.get("latestPosts") or []:
                konto = p.get("ownerUsername") or a.get("username")
                if not konto or konto in EIGENE or p.get("isPinned"):
                    continue
                sc = p.get("shortCode") or p.get("url")
                cap_hook = hook_aus(p.get("caption"))
                bild_hook = (bild.get(sc) or {}).get("text", "")
                posts[sc] = {
                    "quelle": "konkurrenz", "konto": konto, "sc": sc, "nische": nische.get(konto, "umfeld"),
                    "profil": watch.get(konto) or profil_raten(konto, p.get("caption") or ""),
                    # Steht der Hook auf dem Bild, ist das der Hook — die Caption ist dann nur Zeile zwei
                    "hook": bild_hook or cap_hook, "hook_quelle": "bild" if bild_hook else "caption",
                    "caption_anfang": cap_hook, "typ": p.get("type"),
                    "datum": (p.get("timestamp") or "")[:10], "link": p.get("url"),
                    "likes": p.get("likesCount") or 0, "kommentare": p.get("commentsCount") or 0,
                    "aufrufe": p.get("videoViewCount") or 0,
                }
    # Tiefen-Abrufe (apify-tiefe.yml): je Konto ~200 Beiträge, gleiche Felder wie der tägliche Scrape
    for f in sorted(glob.glob(str(RUNS / "tiefe-*.json"))):
        for p in (lies(f) or {}).get("posts", []):
            konto = p.get("ownerUsername")
            sc = p.get("shortCode")
            if not konto or not sc or konto in EIGENE or p.get("isPinned") or sc in posts:
                continue
            cap_hook = hook_aus(p.get("caption"))
            bild_hook = (bild.get(sc) or {}).get("text", "")
            posts[sc] = {
                "quelle": "konkurrenz", "konto": konto, "sc": sc, "nische": nische.get(konto, "umfeld"),
                "profil": watch.get(konto) or profil_raten(konto, p.get("caption") or ""),
                "hook": bild_hook or cap_hook, "hook_quelle": "bild" if bild_hook else "caption",
                "caption_anfang": cap_hook, "typ": p.get("type"),
                "datum": (p.get("timestamp") or "")[:10], "link": p.get("url"),
                "likes": max(p.get("likesCount") or 0, 0), "kommentare": p.get("commentsCount") or 0,
                "aufrufe": p.get("videoViewCount") or p.get("videoPlayCount") or 0,
            }
    # Hashtag-Discovery
    for f in sorted(glob.glob(str(RUNS / "discovery-*.json"))):
        d = lies(f)
        if not d:
            continue
        nische_disc = "doterra" if "doterra" in Path(f).name else "mentoring"
        for r in d.get("ranked", []):
            for p in r.get("posts") or []:
                konto = r.get("handle")
                if not konto or konto in EIGENE:
                    continue
                m = re.search(r"/(?:p|reel)/([^/?]+)", p.get("url") or "")
                sc = m.group(1) if m else p.get("url")
                if sc in posts:
                    continue
                posts[sc] = {
                    "quelle": "discovery", "konto": konto, "profil": nische_disc, "nische": "umfeld", "hook_quelle": "caption",
                    "hook": hook_aus(p.get("caption")), "typ": p.get("type"),
                    "datum": (p.get("timestamp") or "")[:10], "link": p.get("url"),
                    "likes": p.get("likes") or 0, "kommentare": p.get("comments") or 0, "aufrufe": 0,
                }
    # Median über ALLE Beiträge des Kontos — auch die ohne lesbaren Hook. Sonst fällt ein Konto,
    # das den Hook nur aufs Bild schreibt (reichweitenherz), mangels Masse ganz heraus.
    alle = list(posts.values())
    for p in alle:
        p["interaktionen"] = p["likes"] + p["kommentare"]

    # Reels mit Aufrufen gegen Reels mit Aufrufen, der Rest gegen Interaktionen
    mit_aufrufen = [p for p in alle if p["aufrufe"] >= MIN_AUFRUFE]
    ohne = [p for p in alle if p not in mit_aufrufen and p["interaktionen"] >= MIN_INTERAKTIONEN]
    median_faktoren(mit_aufrufen, lambda p: p["aufrufe"])
    median_faktoren(ohne, lambda p: p["interaktionen"])
    for p in mit_aufrufen:
        p["wert"], p["masz"] = p["aufrufe"], "Aufrufe"
    for p in ohne:
        p["wert"], p["masz"] = p["interaktionen"], "Likes+Kommentare"
    return [p for p in mit_aufrufen + ohne if p.get("faktor") is not None and len(p["hook"]) >= 12]


# ---------------------------------------------------------------- Merkmale

ZAHL = re.compile(r"\d")
LISTE = re.compile(r"^\s*(\d+|drei|vier|fünf|sieben|zehn)\s+\w+", re.I)
ICH = re.compile(r"\b(ich|mein|meine|mir|mich)\b", re.I)
DU = re.compile(r"\b(du|dein|deine|dir|dich)\b", re.I)


def regel_merkmale(h):
    w = len(h.split())
    return {
        "frage": "?" in h,
        "zahl": bool(ZAHL.search(h)),
        "liste": bool(LISTE.search(h)),
        "perspektive": "ich" if ICH.search(h) and not DU.search(h) else ("du" if DU.search(h) and not ICH.search(h) else ("beides" if ICH.search(h) else "neutral")),
        "laenge": "kurz (≤8 Wörter)" if w <= 8 else ("mittel (9–16)" if w <= 16 else "lang (17+)"),
    }


FORMEN = Literal["bekenntnis", "ereignis", "liste", "ratgeber", "frage", "meinung", "du-szene", "dialog", "beweis", "aufruf", "zitat", "sonstiges"]
ANGLES = Literal["schmerz", "ergebnis", "beweis", "kontraer", "identitaet", "neugier", "vergleich"]

ANLEITUNG = """Du ordnest Instagram-Hooks (erste Caption-Zeile) aus dem deutschsprachigen Markt ein:
Online-Business für Mamas, Network Marketing, ätherische Öle.

Für jeden Hook (Nummer behalten):
- form: bekenntnis (Ich gebe etwas Persönliches zu) · ereignis (etwas ist passiert, Mini-Geschichte) ·
  liste (Zahl + Aufzählung versprochen) · ratgeber (Tipp/Anleitung/So geht's) · frage (Hook ist eine Frage an sie) ·
  meinung (Hot Take, steile These) · du-szene (beschreibt ihre Situation in der Du-Form) · dialog (wörtliche Rede, Satz von jemandem) ·
  beweis (Zahl/Ergebnis als Beleg) · aufruf (Kommentier/Folge/Link) · zitat (Spruch, Motivation) · sonstiges
- angle: schmerz · ergebnis · beweis · kontraer · identitaet · neugier · vergleich
- stufe: Bewusstseinsstufe 1–5 (1 = weiss nicht, dass sie ein Problem hat · 3 = kennt Lösungen · 5 = kennt das Angebot)
- konkret: true, wenn ein greifbarer Gegenstand, Ort, Betrag, Zeitpunkt oder ein Ereignis drinsteht (Gesichtscreme, Auto, 500 Franken, mit 22, Dienstag 7 Uhr). Abstrakte Begriffe (Erfolg, Business, Sichtbarkeit) zählen nicht.
- thema: 2–4 Wörter auf Deutsch
- emotion: das Gefühl, das der Hook auslösen will, ein Wort (z.B. scham, neugier, wut, hoffnung, erleichterung, stolz, angst, humor, keine)"""


def ki_etiketten(posts):
    try:
        import anthropic
        from pydantic import BaseModel
    except ImportError:
        print("⚠ anthropic/pydantic fehlt — nur Regel-Merkmale.")
        return
    if not os.environ.get("ANTHROPIC_API_KEY"):
        for zeile in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
            if zeile.startswith("ANTHROPIC_API_KEY="):
                os.environ["ANTHROPIC_API_KEY"] = zeile.split("=", 1)[1].strip().strip('"')
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("⚠ Kein ANTHROPIC_API_KEY in .env — nur Regel-Merkmale.")
        return

    class Etikett(BaseModel):
        nr: int
        form: FORMEN
        angle: ANGLES
        stufe: int
        konkret: bool
        thema: str
        emotion: str

    class Antwort(BaseModel):
        hooks: List[Etikett]

    cache = lies(CACHE) or {}
    schluessel = lambda h: hashlib.sha1(h.encode("utf-8")).hexdigest()[:16]
    offen = [p for p in posts if schluessel(p["hook"]) not in cache]
    # gleiche Hooks nur einmal fragen
    eindeutig = list({schluessel(p["hook"]): p["hook"] for p in offen}.items())
    print(f"Etiketten: {len(posts) - len(offen)} aus dem Speicher, {len(eindeutig)} neu.")
    client = anthropic.Anthropic()
    for i in range(0, len(eindeutig), STAPEL):
        teil = eindeutig[i:i + STAPEL]
        liste = "\n".join(f"{n}. {h}" for n, (_, h) in enumerate(teil))
        try:
            r = client.messages.parse(
                model=MODELL, max_tokens=16000,
                output_config={"effort": "low"},
                system=ANLEITUNG,
                messages=[{"role": "user", "content": liste}],
                output_format=Antwort,
            )
        except anthropic.APIStatusError as e:
            print(f"  Stapel {i // STAPEL + 1}: Fehler {e.status_code} — übersprungen")
            continue
        except anthropic.APIConnectionError:
            print(f"  Stapel {i // STAPEL + 1}: keine Verbindung — übersprungen")
            continue
        if r.stop_reason == "refusal" or r.parsed_output is None:
            print(f"  Stapel {i // STAPEL + 1}: keine Antwort ({r.stop_reason}) — übersprungen")
            continue
        for e in r.parsed_output.hooks:
            if 0 <= e.nr < len(teil):
                cache[teil[e.nr][0]] = e.model_dump(exclude={"nr"})
        CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  Stapel {i // STAPEL + 1}/{(len(eindeutig) - 1) // STAPEL + 1} fertig")
    for p in posts:
        e = cache.get(schluessel(p["hook"]))
        if e:
            p.update(e)


# ---------------------------------------------------------------- Auswertung

MERKMALE = [("form", "Form"), ("angle", "Angle"), ("stufe", "Bewusstseinsstufe"), ("konkret", "Konkret (Gegenstand/Betrag/Ereignis)"),
            ("emotion", "Emotion"), ("frage", "Frage drin"), ("zahl", "Zahl drin"), ("perspektive", "Perspektive"), ("laenge", "Länge")]


def tabelle(gruppe):
    """Je Merkmal: Wert · Anzahl · Median-Faktor · Anteil über 2× Median."""
    zeilen = {}
    for k, _ in MERKMALE:
        je = defaultdict(list)
        for p in gruppe:
            if k in p:
                je[str(p[k])].append(p["faktor"])
        z = []
        for wert, f in je.items():
            if len(f) >= MIN_GRUPPE:
                z.append((wert, len(f), round(statistics.median(f), 2), round(100 * sum(1 for x in f if x >= 2) / len(f))))
        zeilen[k] = sorted(z, key=lambda t: -t[2])
    return zeilen


def bericht(eigen, markt, heute):
    L = ["---", "tags: [research, hooks]", "---", "",
         f"# Hook-Markt-Analyse · {heute}", "",
         "**Was im Markt funktioniert — und was davon bei dir funktioniert.** Aus echten Zahlen, "
         "jeder Beitrag gemessen gegen den Durchschnitt (Median) **seines eigenen Kontos**. "
         "Faktor 2,0 heisst: doppelt so gut wie sonst bei diesem Konto.", "",
         "⚠️ Der Hook ist hier die **erste Caption-Zeile**. Der Text im Video kann anders lauten, und Video "
         "und Thema wirken mit. Muster über viele Beiträge sind belastbar, ein einzelner Treffer nicht.", ""]

    konten = sorted({p["konto"] for p in markt})
    L += ["## Datengrundlage", "",
          "| | Beiträge | Konten |", "|---|---:|---:|",
          f"| deine (reif, jetzige Ausrichtung) | {len(eigen)} | {len({p['konto'] for p in eigen})} |",
          f"| Markt: Konkurrenz-Scrape | {sum(1 for p in markt if p['quelle'] == 'konkurrenz')} | {len({p['konto'] for p in markt if p['quelle'] == 'konkurrenz'})} |",
          f"| Markt: Hashtag-Suche | {sum(1 for p in markt if p['quelle'] == 'discovery')} | {len({p['konto'] for p in markt if p['quelle'] == 'discovery'})} |", ""]

    kern = [p for p in markt if p.get("nische") == "kern"]
    if kern:
        L += ["## Deine Nische (von dir benannt: " + ", ".join(sorted({p["konto"] for p in kern})) + ")", "",
              f"*{len(kern)} Beiträge. Steht der Hook auf dem Titelbild, zählt der Bildtext ({sum(p.get('hook_quelle') == 'bild' for p in kern)} Beiträge), sonst die erste Caption-Zeile.*", ""]
        tk, te = tabelle(kern), tabelle([p for p in eigen if p["profil"] == "mentoring"])
        for k, name in MERKMALE[:5]:
            if not tk.get(k):
                continue
            eig = {w: (n, f) for w, n, f, a in te.get(k, [])}
            L += [f"### {name}", "", "| | Nische n | Nische Faktor | ≥2× | deine n | deine Faktor |", "|---|---:|---:|---:|---:|---:|"]
            for w, n, f, a in tk[k]:
                en, ef = eig.get(w, ("–", "–"))
                L.append(f"| {w} | {n} | **{f}** | {a} % | {en} | {ef} |")
            L.append("")
        L += ["### Die stärksten Hooks deiner Nische", "", "| Faktor | Konto | Hook | Quelle | Form · Angle |", "|---:|---|---|---|---|"]
        for p in sorted(kern, key=lambda p: -p["faktor"])[:25]:
            L.append(f"| {p['faktor']} | {p['konto']} | {p['hook'][:150].replace('|', '/')} | {p.get('hook_quelle', '')} | {p.get('form', '')} · {p.get('angle', '')} |")
        L.append("")

    for profil, titel in (("mentoring", "Mentoring (alle Konten, inkl. Umfeld)"), ("doterra", "doTERRA")):
        m = [p for p in markt if p["profil"] == profil]
        e = [p for p in eigen if p["profil"] == profil]
        if len(m) < 30 and len(e) < 30:
            continue
        L += [f"## {titel}", ""]
        tm, te = tabelle(m), tabelle(e)
        L += [f"*Markt: {len(m)} Beiträge · deine: {len(e)} Beiträge*", ""]
        for k, name in MERKMALE:
            if not tm.get(k) and not te.get(k):
                continue
            eig = {w: (n, f, a) for w, n, f, a in te.get(k, [])}
            L += [f"### {name}", "", "| | Markt n | Markt Faktor | Markt ≥2× | deine n | deine Faktor |", "|---|---:|---:|---:|---:|---:|"]
            gesehen = set()
            for w, n, f, a in tm.get(k, []):
                en, ef, _ = eig.get(w, ("–", "–", None))
                L.append(f"| {w} | {n} | **{f}** | {a} % | {en} | {ef} |")
                gesehen.add(w)
            for w, (n, f, _) in eig.items():
                if w not in gesehen:
                    L.append(f"| {w} | – | – | – | {n} | {f} |")
            L.append("")

        L += ["### Die stärksten Hooks im Markt", "", "| Faktor | Konto | Hook | Form · Angle |", "|---:|---|---|---|"]
        for p in sorted(m, key=lambda p: -p["faktor"])[:25]:
            L.append(f"| {p['faktor']} | {p['konto']} | {p['hook'][:150].replace('|', '/')} | {p.get('form', '')} · {p.get('angle', '')} |")
        L += ["", "### Deine stärksten Hooks", "", "| Faktor | Reichweite | Hook | Form · Angle |", "|---:|---:|---|---|"]
        for p in sorted(e, key=lambda p: -(p["faktor"] or 0))[:15]:
            L.append(f"| {p['faktor']} | {p['wert']} | {p['hook'][:150].replace('|', '/')} | {p.get('form', '')} · {p.get('angle', '')} |")
        L += ["", "### Deine schwächsten Hooks", "", "| Faktor | Reichweite | Hook | Form · Angle |", "|---:|---:|---|---|"]
        for p in sorted(e, key=lambda p: (p["faktor"] or 0))[:10]:
            L.append(f"| {p['faktor']} | {p['wert']} | {p['hook'][:150].replace('|', '/')} | {p.get('form', '')} · {p.get('angle', '')} |")
        L.append("")

    L += ["---", "", "## 🔗 Verwandte Notizen", "", "- [[2026-10-04-hook-maschine]]", "- [[hook-formel-testlog]]", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ohne-ki", action="store_true")
    a = ap.parse_args()

    eigen, markt = eigene_beitraege(), markt_beitraege()
    print(f"eigene Beiträge: {len(eigen)} · Markt-Beiträge mit Faktor: {len(markt)}")
    for p in eigen + markt:
        p.update(regel_merkmale(p["hook"]))
    if not a.ohne_ki:
        ki_etiketten(eigen + markt)

    heute = datetime.date.today().isoformat()
    ZIEL.mkdir(parents=True, exist_ok=True)
    (ZIEL / "hook-datenbank.json").write_text(json.dumps(
        {"stand": heute, "eigen": eigen, "markt": markt}, ensure_ascii=False, indent=1), encoding="utf-8")
    pfad = ZIEL / f"{heute}-hook-markt-analyse.md"
    pfad.write_text(bericht(eigen, markt, heute), encoding="utf-8")
    print(f"→ {pfad.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
