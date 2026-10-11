"""Verkaufsdaten für die Hook-Maschine — welche Hooks bringen Leute in die Liste?

Der vierte Datensatz aus `plans/2026-10-04-hook-maschine.md`. Reichweite allein
reicht nicht: zwei grosse Markt-Konten sind Inspirations-Konten, keine
Verkäuferinnen.

🚨 **Fremde Verkaufsdaten gibt es nicht.** Was Konkurrentinnen verkaufen, steht
nirgends. Gemessen wird deshalb zweierlei, und der Bericht sagt beides dazu:

| Ebene | Was gemessen wird |
|---|---|
| **deine** | Lead-Beiträge (mit Stichwort, Zuordnung aus `funnel.json`): Kommentare je 100 erreichte Personen — wer das Stichwort kommentiert, kommentiert. Dazu Eintragungen je Beitrag je Stichwort (ActiveCampaign, Untergrenze). |
| **Markt** | Verkaufssignale in der Caption (Stichwort-CTA, Link/Bio, Preis, Launch-Sprache) — und ob solche Beiträge beim jeweiligen Konto besser oder schlechter laufen als dessen übrige. Plus Kommentare je Like als Mass für Antworten. |

🚨 **Eintragungen gibt es nur je Stichwort, nicht je Beitrag.** ManyChat gibt
keine Zahlen heraus. Je Beitrag ist die Kommentar-Rate das Beste, was messbar ist.

Setzt voraus, dass `markt-analyse.py` gelaufen ist (Etiketten im Cache).

    python scripts/hooks/verkaufsdaten.py
"""

import datetime
import glob
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
FUNNEL = ROOT / "outputs" / "cockpit" / "abgleich" / "funnel.json"
EIGEN = ROOT / "outputs" / "cockpit" / "abgleich" / "gepostet-voll.json"
RUNS = ROOT / "outputs" / "apify-runs"
ZIEL = ROOT / "outputs" / "marktrecherche"
MIN_GRUPPE = 6

SIGNALE = {
    "stichwort": re.compile(r"\b(kommentier\w*|schreib\w*)\b[^.\n]{0,40}\b[A-ZÄÖÜ]{3,}\b"),
    "link": re.compile(r"link in (der )?bio|link im profil|👉\s*link|klick\w* auf den link", re.I),
    "preis": re.compile(r"\d+\s?(€|eur|chf|franken)\b|€\s?\d+|rabatt|gratis|kostenlos", re.I),
    "launch": re.compile(r"warteliste|türen|anmeld\w*|nur noch \d|letzte chance|startet am|plätze", re.I),
}


def lies(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return None


def med(xs):
    return round(statistics.median(xs), 2) if xs else None


def eigene_leads():
    db = lies(DB) or {}
    nach_link = {p.get("link"): p for p in db.get("eigen", [])}
    kom = {b.get("link"): b for b in (lies(EIGEN) or {}).get("beitraege", [])}
    fu = lies(FUNNEL) or {}
    zeilen, je_kw = [], []
    gesehen = set()
    for it in fu.get("items", []):
        kw = it.get("keyword")
        je_kw.append({"keyword": kw, "beitraege": len(it.get("posts_gepostet") or []),
                      "eintragungen": it.get("tag_kontakte"), "je_beitrag": it.get("kontakte_je_beitrag"),
                      "reichweite_median": it.get("reichweite_median")})
        for p in it.get("posts_gepostet") or []:
            link = p.get("link")
            if link in gesehen:
                continue
            gesehen.add(link)
            h = nach_link.get(link)
            b = kom.get(link) or {}
            if not h or not b.get("reach"):
                continue
            zeilen.append(dict(h, keyword=kw, kommentare=b.get("kommentare") or 0,
                               kommentar_rate=round(100 * (b.get("kommentare") or 0) / b["reach"], 2)))
    return zeilen, je_kw


def markt_signale():
    db = lies(DB) or {}
    nach_link = {p.get("link"): p for p in db.get("markt", [])}
    captions = {}
    for f in sorted(glob.glob(str(RUNS / "competitors-*.json"))):
        d = lies(f) or {}
        for a in d.get("results", []):
            for p in a.get("latestPosts") or []:
                captions[p.get("url")] = (p.get("caption") or "", p.get("likesCount") or 0, p.get("commentsCount") or 0)
    out = []
    for link, (cap, likes, kom) in captions.items():
        h = nach_link.get(link)
        if not h:
            continue
        sig = [k for k, rx in SIGNALE.items() if rx.search(cap)]
        out.append(dict(h, signale=sig, verkauf=bool(sig), kom_je_like=round(kom / likes, 3) if likes else None))
    return out


def gruppen(zeilen, schluessel, wert):
    je = defaultdict(list)
    for z in zeilen:
        if schluessel in z and z.get(wert) is not None:
            je[str(z[schluessel])].append(z[wert])
    return sorted(((k, len(v), med(v)) for k, v in je.items() if len(v) >= MIN_GRUPPE), key=lambda t: -t[2])


def bericht(leads, je_kw, markt, heute):
    L = ["---", "tags: [research, hooks]", "---", "", f"# Hook-Verkaufsdaten · {heute}", "",
         "**Welche Hooks bringen Leute in die Liste, nicht nur Reichweite?** Ergänzung zu [[2026-10-04-hook-markt-analyse]].", "",
         "⚠️ Eintragungen gibt es nur **je Stichwort** (ActiveCampaign, Untergrenze). Je Beitrag ist die **Kommentar-Rate** "
         "(Kommentare je 100 erreichte Personen) das Beste, was messbar ist. Fremde Umsätze sind nirgends öffentlich.", "",
         "## Deine Stichwörter", "", "| Stichwort | Beiträge | in der Liste | je Beitrag | Median-Reichweite |", "|---|---:|---:|---:|---:|"]
    for k in sorted(je_kw, key=lambda k: -(k["je_beitrag"] or 0)):
        if k["beitraege"]:
            L.append(f"| {k['keyword']} | {k['beitraege']} | {k['eintragungen'] if k['eintragungen'] is not None else '–'} | "
                     f"{k['je_beitrag'] if k['je_beitrag'] is not None else '–'} | {k['reichweite_median'] or '–'} |")
    L += ["", f"## Deine Lead-Beiträge: welche Hooks holen Kommentare? ({len(leads)} Beiträge)", "",
          f"Median-Kommentar-Rate aller Lead-Beiträge: **{med([z['kommentar_rate'] for z in leads])}** je 100 erreichte Personen.", ""]
    for k, name in (("form", "Form"), ("angle", "Angle"), ("stufe", "Bewusstseinsstufe"), ("emotion", "Emotion"), ("frage", "Frage drin")):
        g = gruppen(leads, k, "kommentar_rate")
        if g:
            L += [f"### {name}", "", "| | n | Kommentare je 100 | Reichweite (Faktor) |", "|---|---:|---:|---:|"]
            for w, n, r in g:
                f = med([z["faktor"] for z in leads if str(z.get(k)) == w and z.get("faktor") is not None])
                L.append(f"| {w} | {n} | **{r}** | {f} |")
            L.append("")
    L += ["### Die Lead-Beiträge mit den meisten Kommentaren je Reichweite", "", "| Kom./100 | Reichweite | Stichwort | Hook |", "|---:|---:|---|---|"]
    for z in sorted(leads, key=lambda z: -z["kommentar_rate"])[:12]:
        L.append(f"| {z['kommentar_rate']} | {z['wert']} | {z['keyword']} | {z['hook'][:130].replace('|', '/')} |")

    L += ["", "## Markt: laufen Verkaufsbeiträge schlechter?", "",
          "Jeder Beitrag gegen den Median seines Kontos. „Verkaufssignal“ = Stichwort-Aufruf, Link/Bio, Preis oder Launch-Sprache in der Caption.", "",
          "| Konto | Verkaufsbeiträge | Faktor | übrige | Faktor | Kommentare je Like (Verkauf / übrige) |", "|---|---:|---:|---:|---:|---|"]
    je = defaultdict(list)
    for m in markt:
        je[m["konto"]].append(m)
    for konto, ps in sorted(je.items(), key=lambda kv: -len(kv[1])):
        v = [p for p in ps if p["verkauf"]]
        u = [p for p in ps if not p["verkauf"]]
        if len(v) >= 3 and len(u) >= 3:
            kv = med([p["kom_je_like"] for p in v if p["kom_je_like"] is not None])
            ku = med([p["kom_je_like"] for p in u if p["kom_je_like"] is not None])
            L.append(f"| {konto} | {len(v)} | {med([p['faktor'] for p in v])} | {len(u)} | {med([p['faktor'] for p in u])} | {kv} / {ku} |")
    sv = [p for p in markt if "stichwort" in p["signale"]]
    L += ["", f"### Stichwort-Beiträge im Markt ({len(sv)}): die stärksten", "", "| Faktor | Konto | Hook | Form · Angle |", "|---:|---|---|---|"]
    for p in sorted(sv, key=lambda p: -p["faktor"])[:12]:
        L.append(f"| {p['faktor']} | {p['konto']} | {p['hook'][:130].replace('|', '/')} | {p.get('form', '')} · {p.get('angle', '')} |")
    L += ["", "---", "", "## 🔗 Verwandte Notizen", "", "- [[2026-10-04-hook-markt-analyse]]", "- [[2026-10-04-hook-maschine]]", ""]
    return "\n".join(L)


def main():
    leads, je_kw = eigene_leads()
    markt = markt_signale()
    print(f"Lead-Beiträge mit Etikett: {len(leads)} · Markt-Beiträge mit Caption: {len(markt)} · davon mit Verkaufssignal: {sum(p['verkauf'] for p in markt)}")
    heute = datetime.date.today().isoformat()
    (ZIEL / "hook-verkaufsdaten.json").write_text(json.dumps({"stand": heute, "leads": leads, "stichwoerter": je_kw},
                                                             ensure_ascii=False, indent=1), encoding="utf-8")
    p = ZIEL / f"{heute}-hook-verkaufsdaten.md"
    p.write_text(bericht(leads, je_kw, markt, heute), encoding="utf-8")
    print(f"→ {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
