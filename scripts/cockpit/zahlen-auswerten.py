#!/usr/bin/env python3
"""„Was die Zahlen sagen“ — die Auswertung oben im Cockpit-Reiter „Gepostet & Analyse“.

Patricia, 13.10.2026 (Kurs „Content Shortcut“ schlug ein eigenes Dashboard vor):
*„genau logisch kein neues dashboard. sondern in meinem bestehenden schlau integrieren“*.

Liest den jüngsten Abzug aus `outputs/instagram-insights/` (holen.py) und
`outputs/cockpit/abgleich/umsatz-stichwort.json` (umsatz-je-stichwort.py) und schreibt
`outputs/cockpit/abgleich/auswertung.json` → Cockpit `daten/auswertung`.

Was drinsteht:
- die wichtigste Erkenntnis als ein Satz mit Zahlen (Umsatz zuerst, sonst Reichweite)
- Wochentage (ab 3 Beiträgen) · Formate Reel/Karussell/Bild
- Patricias fünf Säulen (eingeordnet von Claude, zwischengespeichert)
- Stichwörter: Beiträge, Kommentare, Eintragungen, Käuferinnen, Umsatz
- Diagnose je Beitrag: Reichweite ohne Reaktion · läuft · leise
- drei Empfehlungen, jede mit ihrer Zahl

🚨 Gezählt werden nur **ausgereifte** Beiträge (ab 7 Tagen), sonst zieht ein Reel von
gestern jeden Schnitt nach unten. 🚨 Median neben dem Schnitt, weil ein Ausreisser den
Schnitt verzerrt. 🚨 Quoten erst ab einer Mindestbasis (Reichweite über dem eigenen
Median), sonst misst die Quote den Zufall (CLAUDE.md, „Jede Quote braucht eine Mindestbasis“).

    python scripts/cockpit/zahlen-auswerten.py
"""
import hashlib
import json
import os
import re
import statistics as st
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
EIN = ROOT / "outputs" / "instagram-insights"
AB = ROOT / "outputs" / "cockpit" / "abgleich"
ZIEL = AB / "auswertung.json"
CACHE = AB / "saeulen-cache.json"
ZH = ZoneInfo("Europe/Zurich")
TAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
SAEULEN = {
    1: "Personal Brand statt Copy-Paste",
    2: "Plan B und eigenes Geld",
    3: "Business im Mama-Alltag",
    4: "Eigenverantwortung statt Hobbymodus",
    5: "Beweis und Angebot",
}
MODELL = "claude-haiku-5-5"
HOOKTYPEN = ["Frage", "Polarisierung", "Story-Einstieg", "Pain-Punkt", "Listicle", "Behauptung", "Zitat"]
HOOK_CACHE = AB / "hooktyp-cache.json"
STICHWORT = re.compile(r"[Kk]ommentier\w*\s+[„\"«*]*([A-ZÄÖÜ0-9]{3,})")


def neuester_abzug():
    dateien = sorted(EIN.glob("20??-??-??.json"))
    if not dateien:
        sys.exit("Kein Abzug in outputs/instagram-insights — erst holen.py laufen lassen.")
    return dateien[-1]


def format_von(b):
    mt = (b.get("medientyp") or "").upper()
    if (b.get("typ") or "").upper() == "REELS" or mt == "VIDEO":
        return "Reel"
    if mt == "CAROUSEL_ALBUM":
        return "Karussell"
    if mt == "IMAGE":
        return "Bild"
    return "Karussell/Bild"     # alter Abzug ohne medientyp


def lokaler_tag(b):
    z = b.get("zeitpunkt")
    if z:
        try:
            return datetime.fromisoformat(z.replace("+0000", "+00:00")).astimezone(ZH).date()
        except ValueError:
            pass
    return date.fromisoformat(b["datum"])


def interaktionen(b):
    t = b.get("total_interactions")
    if isinstance(t, (int, float)):
        return t
    return sum(b.get(k) or 0 for k in ("likes", "kommentare", "saved", "shares"))


def saeulen_einordnen(beitraege):
    """Claude ordnet jede Caption einer der fünf Säulen zu. Zwischengespeichert,
    damit derselbe Beitrag nie zweimal gefragt wird."""
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    schl = lambda b: hashlib.sha1((b.get("caption") or b.get("anfang") or b["id"])
                                  .encode("utf-8")).hexdigest()[:16]
    offen = [b for b in beitraege if schl(b) not in cache]
    if offen:
        try:
            import anthropic
        except ImportError:
            print("⚠ anthropic fehlt — Säulen bleiben leer.")
            offen = []
        if offen and not os.environ.get("ANTHROPIC_API_KEY"):
            for z in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
                if z.startswith("ANTHROPIC_API_KEY="):
                    os.environ["ANTHROPIC_API_KEY"] = z.split("=", 1)[1].strip().strip('"')
        if offen:
            client = anthropic.Anthropic()
            saeulen = "\n".join("%d = %s" % kv for kv in SAEULEN.items())
            for i in range(0, len(offen), 25):
                teil = offen[i:i + 25]
                liste = "\n".join("%d. %s" % (n, (b.get("caption") or b.get("anfang") or "")[:600]
                                               .replace("\n", " ")) for n, b in enumerate(teil))
                r = client.messages.create(
                    model=MODELL, max_tokens=2000,
                    system=("Du ordnest Instagram-Beiträge einer Mentorin für Network-Mamas "
                            "genau einer von fünf Content-Säulen zu:\n" + saeulen +
                            "\nAntworte nur mit JSON: {\"nr\": säule, ...} für jede Nummer."),
                    messages=[{"role": "user", "content": liste}])
                text = "".join(x.text for x in r.content if getattr(x, "type", "") == "text")
                m = re.search(r"\{.*\}", text, re.S)
                antwort = json.loads(m.group(0)) if m else {}
                for n, b in enumerate(teil):
                    s = antwort.get(str(n))
                    if isinstance(s, int) and s in SAEULEN:
                        cache[schl(b)] = s
                CACHE.write_text(json.dumps(cache, indent=1), encoding="utf-8")
            print("Säulen: %d neu eingeordnet" % len(offen))
    for b in beitraege:
        b["saeule"] = cache.get(schl(b))


def hooktyp_einordnen(beitraege):
    """Claude ordnet die erste Zeile jedes Beitrags einem Hook-Typ zu (Bestperformer-
    Analyse aus dem Kurs „Content Shortcut“, 13.10.2026). Eigener Zwischenspeicher."""
    cache = json.loads(HOOK_CACHE.read_text(encoding="utf-8")) if HOOK_CACHE.exists() else {}
    schl = lambda b: hashlib.sha1((b.get("caption") or b.get("anfang") or b["id"])
                                  .encode("utf-8")).hexdigest()[:16]
    offen = [b for b in beitraege if schl(b) not in cache]
    if offen:
        import anthropic
        if not os.environ.get("ANTHROPIC_API_KEY"):
            for z in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
                if z.startswith("ANTHROPIC_API_KEY="):
                    os.environ["ANTHROPIC_API_KEY"] = z.split("=", 1)[1].strip().strip('"')
        client = anthropic.Anthropic()
        for i in range(0, len(offen), 25):
            teil = offen[i:i + 25]
            liste = "\n".join("%d. %s" % (n, (b.get("caption") or b.get("anfang") or "")[:220]
                                           .replace("\n", " ")) for n, b in enumerate(teil))
            r = client.messages.create(
                model=MODELL, max_tokens=6000, thinking={"type": "disabled"},
                system=("Bestimme für jeden Instagram-Beitrag den Hook-Typ seiner ersten Zeile. "
                        "Genau einer von: " + ", ".join(HOOKTYPEN) + ". Antworte nur mit JSON: "
                        "{\"nr\": \"Typ\", ...} für jede Nummer."),
                messages=[{"role": "user", "content": liste}])
            text = "".join(x.text for x in r.content if getattr(x, "type", "") == "text")
            m = re.search(r"\{.*\}", text, re.S)
            antwort = json.loads(m.group(0)) if m else {}
            for n, b in enumerate(teil):
                h = antwort.get(str(n))
                if h in HOOKTYPEN:
                    cache[schl(b)] = h
            HOOK_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
        print("Hook-Typen: %d neu eingeordnet" % len(offen))
    for b in beitraege:
        b["hooktyp"] = cache.get(schl(b))


def laenge(b):
    w = len((b.get("caption") or b.get("anfang") or "").split())
    return "kurz" if w < 60 else ("mittel" if w < 160 else "lang")


def cta_art(b):
    c = (b.get("caption") or "")
    if STICHWORT.search(c):
        return "Stichwort"
    if re.search(r"[Ss]chick|[Tt]eil (das|es|den)|weiterleiten", c):
        return "Teilen"
    if re.search(r"[Ss]peicher", c):
        return "Speichern"
    if re.search(r"[Ff]olg(e)? mir|[Ff]olgen", c):
        return "Folgen"
    if re.search(r"\?\s*(⬇️|👇)?\s*$", c.strip()[-160:]) or re.search(r"[Ss]chreib (mir|es) (in die|unten)", c):
        return "Frage"
    return "keiner"


def bestperformer(reif, med_reich):
    """Top 10 nach Rate — aber nur mit Mindestbasis (Reichweite über dem eigenen Median,
    mind. 3 Interaktionen), sonst gewinnt ein Beitrag mit 40 Erreichten und 2 Likes."""
    basis = [b for b in reif if b["reach"] > med_reich and interaktionen(b) >= 3]
    top = sorted(basis, key=lambda b: b["rate"], reverse=True)[:10]
    def haeufig(feld, bs):
        c = defaultdict(int)
        for b in bs:
            if b.get(feld):
                c[b[feld]] += 1
        return sorted(c.items(), key=lambda kv: -kv[1])
    def anteil(feld, wert):
        alle = [b for b in reif if b.get(feld)]
        return round(100 * sum(1 for b in alle if b[feld] == wert) / max(1, len(alle)))
    zeilen = [{"datum": b["tag"].isoformat(), "anfang": " ".join((b.get("anfang") or "").split()[:8]),
               "link": b.get("link"), "format": b["format"], "thema": SAEULEN.get(b.get("saeule"), "–"),
               "hooktyp": b.get("hooktyp") or "–", "laenge": laenge(b), "cta": cta_art(b),
               "reichweite": b["reach"], "rate": b["rate"]} for b in top]
    for z, b in zip(zeilen, top):
        b["laenge"], b["cta"], b["thema"] = z["laenge"], z["cta"], z["thema"]
    muster = {}
    for feld in ("format", "hooktyp", "thema", "laenge", "cta"):
        h = haeufig(feld, top)
        if h:
            wert, n = h[0]
            muster[feld] = {"wert": wert, "in_top": n, "von": len(top),
                            "anteil_gesamt": anteil(feld, wert) if feld != "thema" else None,
                            "verteilung": h}
    for b in reif:
        b.setdefault("laenge", laenge(b))
        b.setdefault("cta", cta_art(b))
    for b in reif:
        b["thema"] = SAEULEN.get(b.get("saeule"), "–")
    for feld in ("laenge", "cta", "format", "hooktyp", "thema"):
        if feld in muster:
            muster[feld]["anteil_gesamt"] = anteil(feld, muster[feld]["wert"])
    def w(f): return muster.get(f, {}).get("wert", "–")
    formel = ("Nimm %s + %s-Hook + Thema „%s“ + %s Caption + Aufruf: %s."
              % (w("format"), w("hooktyp"), w("thema"), {"kurz": "kurze", "mittel": "mittellange", "lang": "lange"}.get(w("laenge"), w("laenge")), w("cta")))
    return {"top": zeilen, "muster": muster, "formel": formel,
            "basis": "Top 10 nach Rate, nur Beiträge mit Reichweite über dem Median (%d) und mind. 3 Interaktionen"
                     % round(med_reich)}


def nachfrage_je_saeule(reif):
    """Für die Produktideen: Saves, Shares und Kommentare je Säule, auf 1'000 Erreichte.
    Reichweite allein ist keine Nachfrage — wer speichert, will es später benutzen."""
    g = defaultdict(list)
    for b in reif:
        if b.get("saeule"):
            g[SAEULEN[b["saeule"]]].append(b)
    out = []
    for name, bs in g.items():
        r = sum(b["reach"] for b in bs) or 1
        s = sum(b.get("saved") or 0 for b in bs)
        sh = sum(b.get("shares") or 0 for b in bs)
        k = sum(b.get("kommentare") or 0 for b in bs)
        out.append({"name": name, "beitraege": len(bs), "reichweite": r,
                    "saves": s, "shares": sh, "kommentare": k,
                    "saves_je_1000": round(1000 * s / r, 1), "shares_je_1000": round(1000 * sh / r, 1),
                    "kommentare_je_1000": round(1000 * k / r, 1),
                    "top": [{"anfang": " ".join((b.get("anfang") or "").split()[:10]), "link": b.get("link"),
                             "saves": b.get("saved") or 0, "shares": b.get("shares") or 0,
                             "kommentare": b.get("kommentare") or 0, "reichweite": b["reach"]}
                            for b in sorted(bs, key=lambda b: -((b.get("saved") or 0) + (b.get("shares") or 0)
                                                                 + (b.get("kommentare") or 0)))[:3]]})
    return sorted(out, key=lambda x: -(x["saves_je_1000"] + x["shares_je_1000"] + x["kommentare_je_1000"]))


def gruppe(beitraege, schluessel):
    g = defaultdict(list)
    for b in beitraege:
        k = schluessel(b)
        if k is not None:
            g[k].append(b)
    raus = []
    for k, bs in g.items():
        reich = [b["reach"] for b in bs]
        raus.append({
            "name": k, "beitraege": len(bs),
            "reichweite_median": round(st.median(reich)),
            "reichweite_schnitt": round(st.mean(reich)),
            "rate": round(100 * sum(interaktionen(b) for b in bs) / max(1, sum(reich)), 2),
            "gespeichert": sum(b.get("saved") or 0 for b in bs),
            "geteilt": sum(b.get("shares") or 0 for b in bs),
            "kommentare": sum(b.get("kommentare") or 0 for b in bs),
        })
    return raus


def zahl(x):
    return "{:,}".format(round(x)).replace(",", "'")


def main():
    quelle = neuester_abzug()
    konto = json.loads(quelle.read_text(encoding="utf-8"))["konten"][0]
    heute = date.today()
    alle = [b for b in konto["beitraege"] if isinstance(b.get("reach"), (int, float))]
    for b in alle:
        b["format"] = format_von(b)
        b["tag"] = lokaler_tag(b)
        b["alter"] = (heute - b["tag"]).days
        b["rate"] = round(100 * interaktionen(b) / b["reach"], 2) if b["reach"] else 0
        m = STICHWORT.search(b.get("caption") or "")
        b["stichwort"] = m.group(1) if m else None
    reif = [b for b in alle if b["alter"] >= 7]
    if len(reif) < 10:
        sys.exit("Zu wenige ausgereifte Beiträge (%d) für eine Auswertung." % len(reif))
    saeulen_einordnen(reif)
    hooktyp_einordnen(reif)

    med_reich = st.median(b["reach"] for b in reif)
    schnitt_rate = 100 * sum(interaktionen(b) for b in reif) / sum(b["reach"] for b in reif)
    med_kommentar_rate = st.mean((b.get("kommentare") or 0) / b["reach"] for b in reif if b["reach"])

    # --- Wochentage (ab 3 Beiträgen) ---
    tage = [t for t in gruppe(reif, lambda b: TAGE[b["tag"].weekday()]) if t["beitraege"] >= 3]
    tage.sort(key=lambda t: TAGE.index(t["name"]))
    stark = max(tage, key=lambda t: t["reichweite_median"]) if tage else None
    schwach = min(tage, key=lambda t: t["reichweite_median"]) if tage else None

    # --- Formate ---
    formate = sorted(gruppe(reif, lambda b: b["format"]), key=lambda f: -f["beitraege"])

    # --- Säulen ---
    saeulen = sorted(gruppe(reif, lambda b: SAEULEN.get(b.get("saeule"))),
                     key=lambda s: -s["reichweite_median"])

    # --- Stichwörter mit Umsatz ---
    umsatz = {}
    u_datei = AB / "umsatz-stichwort.json"
    u = json.loads(u_datei.read_text(encoding="utf-8")) if u_datei.exists() else {}
    for z in u.get("stichwoerter", []):
        umsatz[z["stichwort"]] = z
    kw = []
    gespielt = defaultdict(list)
    for b in alle:
        if b["stichwort"]:
            gespielt[b["stichwort"]].append(b)
    for name in sorted(set(gespielt) | set(umsatz)):
        bs = gespielt.get(name, [])
        reich = sum(b["reach"] for b in bs)
        z = umsatz.get(name, {})
        kw.append({
            "stichwort": name, "beitraege": len(bs), "reichweite": reich,
            "kommentare": sum(b.get("kommentare") or 0 for b in bs),
            "eintragungen": z.get("eintragungen"), "kaeuferinnen": z.get("kaeuferinnen"),
            "umsatz": z.get("umsatz"),
            "umsatz_je_1000": round(1000 * z["umsatz"] / reich, 2) if z.get("umsatz") and reich else None,
            "nie_benutzt": not bs,
            "geteilt_mit": z.get("geteilt_mit") or [],
            "produkte": z.get("produkte") or [],
        })
    kw.sort(key=lambda k: -(k["umsatz"] or 0))

    # --- Diagnose je Beitrag ---
    diag = []
    for b in sorted(reif, key=lambda b: b["tag"], reverse=True)[:40]:
        kom_rate = (b.get("kommentare") or 0) / b["reach"] if b["reach"] else 0
        if b["reach"] > med_reich and b["rate"] < schnitt_rate:
            d = "Reichweite ohne Reaktion"
        elif b["reach"] > med_reich and b["rate"] >= schnitt_rate:
            d = "läuft"
        elif b["rate"] >= schnitt_rate:
            d = "Reaktion ohne Reichweite"
        else:
            d = "leise"
        diag.append({"datum": b["tag"].isoformat(), "format": b["format"], "link": b.get("link"),
                     "anfang": b.get("anfang"), "reichweite": b["reach"], "rate": b["rate"],
                     "kommentare": b.get("kommentare") or 0, "stichwort": b["stichwort"],
                     "diagnose": d})

    def top(bs, n, key):
        return [{"datum": b["tag"].isoformat(), "format": b["format"], "link": b.get("link"),
                 "anfang": b.get("anfang"), "reichweite": b["reach"], "rate": b["rate"],
                 "gespeichert": b.get("saved") or 0, "geteilt": b.get("shares") or 0}
                for b in sorted(bs, key=key, reverse=True)[:n]]

    # Mindestbasis: nur über dem eigenen Median zählt eine hohe Rate
    basis = [b for b in reif if b["reach"] > med_reich and interaktionen(b) >= 3]

    # --- Erkenntnis und Empfehlungen ---
    erkenntnis, empfehlungen = [], []
    bester_kw = next((k for k in kw if k["umsatz"]), None)
    if bester_kw:
        erkenntnis.append(
            "Das Stichwort %s hat seit %s CHF %s gebracht (%d Käuferin%s aus %d Eintragungen) — "
            "auf %s Reichweite sind das CHF %s je 1'000 erreichte Personen."
            % (bester_kw["stichwort"], u.get("ab", ""), zahl(bester_kw["umsatz"]),
               bester_kw["kaeuferinnen"], "" if bester_kw["kaeuferinnen"] == 1 else "nen",
               bester_kw["eintragungen"] or 0, zahl(bester_kw["reichweite"]),
               zahl(bester_kw["umsatz_je_1000"] or 0)))
        if bester_kw["geteilt_mit"]:
            erkenntnis[-1] += (" Vorsicht bei der Deutung: Dieselbe Käuferin trägt auch %s — "
                               "ihr Kauf steht bei jedem dieser Stichwörter, es ist ein Kauf, nicht drei."
                               % " und ".join(bester_kw["geteilt_mit"]))
    if stark and schwach and stark["name"] != schwach["name"]:
        erkenntnis.append(
            "Am %s erreichst du im Median %s Personen, am %s nur %s."
            % (stark["name"], zahl(stark["reichweite_median"]),
               schwach["name"], zahl(schwach["reichweite_median"])))
        empfehlungen.append({
            "was": "Den stärksten Beitrag der Woche auf %s legen, nicht auf %s."
                   % (stark["name"], schwach["name"]),
            "zahl": "%s gegen %s Median-Reichweite (je mind. 3 Beiträge)"
                    % (zahl(stark["reichweite_median"]), zahl(schwach["reichweite_median"]))})
    if bester_kw:
        leer = [k["stichwort"] for k in kw if k["beitraege"] >= 2 and not k["umsatz"]]
        empfehlungen.append({
            "was": "Bei den Lead-Posts zuerst %s spielen%s."
                   % (bester_kw["stichwort"],
                      (", " + " und ".join(leer[:2]) + " brachten bisher keinen Kauf") if leer else ""),
            "zahl": "%s: CHF %s Umsatz aus %d Beiträgen"
                    % (bester_kw["stichwort"], zahl(bester_kw["umsatz"]), bester_kw["beitraege"])})
    roh = [d for d in diag if d["diagnose"] == "Reichweite ohne Reaktion"]
    if roh:
        empfehlungen.append({
            "was": "Bei %d Beiträgen kam Reichweite, aber keine Reaktion — dort fehlt der Grund "
                   "zum Antworten: ein Stichwort in Zeile 1 oder eine Frage mit Zahlenwahl."
                   % len(roh),
            "zahl": "Reichweite über dem Median (%s), Rate unter dem Schnitt (%.1f %%)"
                    % (zahl(med_reich), schnitt_rate)})
    if u.get("gesamt", {}).get("anteil_ohne_stichwort") is not None:
        g = u["gesamt"]
        erkenntnis.append("%s %% des Umsatzes seit %s lässt sich keinem Stichwort zuordnen "
                          "(Story-Link, Bio, Mail oder ohne Eintragung)."
                          % (zahl(g["anteil_ohne_stichwort"]), u.get("ab", "")))

    daten = {
        "stand": heute.isoformat(),
        "zahlen_vom": quelle.stem,
        "basis": {"beitraege": len(reif), "ab": min(b["tag"] for b in reif).isoformat(),
                  "reichweite_median": round(med_reich), "rate_schnitt": round(schnitt_rate, 2),
                  "hinweis": "nur Beiträge ab 7 Tagen · Rate = Interaktionen je erreichte Person"},
        "umsatz": u.get("gesamt"),
        "umsatz_ab": u.get("ab"),
        "umsatz_misst": u.get("misst"),
        "erkenntnis": erkenntnis,
        "empfehlungen": empfehlungen[:3],
        "wochentage": tage,
        "formate": formate,
        "saeulen": saeulen,
        "stichwoerter": kw,
        "diagnose": diag,
        "bestperformer": bestperformer(reif, med_reich),
        "nachfrage": nachfrage_je_saeule(reif),
        "top_rate": top(basis, 5, lambda b: b["rate"]),
        "top_reels": top([b for b in reif if b["format"] == "Reel"], 3, lambda b: b["reach"]),
        "top_karussells": top([b for b in reif if b["format"] != "Reel"], 3, lambda b: b["reach"]),
    }
    ZIEL.write_text(json.dumps(daten, ensure_ascii=False, indent=1), encoding="utf-8")
    for e in erkenntnis:
        print("•", e)
    for e in empfehlungen[:3]:
        print("→", e["was"], "|", e["zahl"])
    print("->", ZIEL)


if __name__ == "__main__":
    main()
