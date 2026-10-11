"""Holt Instagram-Zahlen ueber die Meta Graph API — Beitraege und Storys.

Warum es das gibt: Reichweite, Speicherungen und Geteilt-Zahlen stehen sonst
nur in der Instagram-App und muessen von Hand in die Notion-Content-DB
abgetippt werden. Das passiert erfahrungsgemaess nicht, und dann fehlt beim
Monatsrueckblick die Grundlage.

    python scripts/instagram-insights/holen.py            # letzte 25 Beitraege
    python scripts/instagram-insights/holen.py --anzahl 50
    python scripts/instagram-insights/holen.py --storys   # nur die aktiven Storys

Zugang kommt aus scripts/meta-ads/.env (META_ACCESS_TOKEN, gitignored).
Kein Schluessel steht in dieser Datei.

🚨 STORYS LAUFEN AB. Instagram gibt Story-Zahlen nur heraus, solange die Story
   aktiv ist — also hoechstens 24 Stunden. Wer einmal am Tag laeuft, erwischt
   sie; wer zwei Tage spaeter schaut, bekommt sie nie mehr. Beitraege dagegen
   kann man auch Wochen spaeter noch abfragen.
"""

import argparse
import datetime
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

WURZEL = pathlib.Path(__file__).resolve().parents[2]
ENV = WURZEL / "scripts" / "meta-ads" / ".env"
ZIEL = WURZEL / "outputs" / "instagram-insights"
API = "https://graph.facebook.com/v21.0"

# Zahlen je Beitrag. total_interactions = Likes + Kommentare + Speicherungen + Geteilt.
BEITRAG_METRIKEN = "reach,saved,shares,total_interactions"
# Storys: navigation buendelt Weitertippen, Zurueck und Verlassen.
STORY_METRIKEN = "reach,replies,navigation"


def zugang():
    """Liest den Token aus der .env. Bricht ab, statt mit einem Platzhalter weiterzulaufen."""
    if not ENV.exists():
        sys.exit("Keine .env unter %s — dort muss META_ACCESS_TOKEN stehen." % ENV)
    werte = {}
    for zeile in ENV.read_text(encoding="utf-8").splitlines():
        zeile = zeile.strip()
        if zeile and not zeile.startswith("#") and "=" in zeile:
            k, v = zeile.split("=", 1)
            werte[k.strip()] = v.strip()
    tok = werte.get("META_ACCESS_TOKEN")
    if not tok:
        sys.exit("META_ACCESS_TOKEN fehlt in der .env.")
    return tok


def hole(pfad, token, **felder):
    felder["access_token"] = token
    url = API + "/" + pfad + "?" + urllib.parse.urlencode(felder)
    try:
        with urllib.request.urlopen(url) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        leib = e.read().decode("utf-8", "replace")
        try:
            return {"error": json.loads(leib).get("error", {})}
        except ValueError:
            return {"error": {"message": leib[:200]}}


def konten(token):
    """Alle Instagram-Konten, die an einer freigegebenen Facebook-Seite haengen.

    Wichtig: instagram_business_account kommt nur mit dem SEITEN-Token zurueck,
    nicht mit dem Nutzer-Token. Das hat uns beim Einrichten eine Stunde gekostet.
    """
    r = hole("me/accounts", token, fields="id,name,access_token")
    if "error" in r:
        sys.exit("Seiten nicht abrufbar: %s" % r["error"].get("message"))
    raus = []
    for seite in r.get("data", []):
        st = seite.get("access_token")
        if not st:
            continue
        d = hole(seite["id"], st, fields="instagram_business_account{id,username,followers_count,media_count}")
        ig = d.get("instagram_business_account")
        if ig:
            raus.append({
                "seite": seite.get("name"),
                "ig_id": ig["id"],
                "handle": ig.get("username"),
                "follower": ig.get("followers_count"),
                "beitraege_gesamt": ig.get("media_count"),
                "token": st,
            })
    return raus


def sauber(text, laenge=90):
    """Emoji raus, eine Zeile — sonst zerreisst es die Konsole und die Tabelle."""
    t = re.sub(r"[^\x20-\x7EÀ-ſ]", "", (text or "").replace("\n", " "))
    t = re.sub(r"\s+", " ", t).strip()
    return t[:laenge]


def messwerte(obj_id, token, metriken):
    r = hole("%s/insights" % obj_id, token, metric=metriken)
    if "error" in r:
        return {"_fehler": r["error"].get("message", "")[:120]}
    raus = {}
    for m in r.get("data", []):
        wert = m["values"][0]["value"]
        if isinstance(wert, dict):          # navigation kommt als Aufschluesselung
            raus.update({m["name"] + "_" + k: v for k, v in wert.items()})
        else:
            raus[m["name"]] = wert
    return raus


def seiten(pfad, token, hoechstens, **felder):
    """Blaettert durch die Antwort, bis `hoechstens` Eintraege da sind.

    🚨 Die API gibt hoechstens 100 Eintraege pro Seite, aber **nicht** nur 100
    insgesamt. Bis zum 24.09.2026 holte dieses Skript stur die letzten 25 — das
    war eine Vorgabe hier im Code, keine Grenze von Instagram. Auf dem
    Mentoring-Konto lagen zu dem Zeitpunkt 321 Beitraege, von denen 296 nie
    jemand gesehen hat.
    """
    felder["limit"] = min(hoechstens, 100)
    r = hole(pfad, token, **felder)
    if "error" in r:
        return r
    raus = list(r.get("data", []))
    weiter = (r.get("paging") or {}).get("next")
    while weiter and len(raus) < hoechstens:
        try:
            with urllib.request.urlopen(weiter) as antwort:
                r = json.loads(antwort.read().decode("utf-8"))
        except Exception as e:
            print("   Abbruch beim Blaettern nach %d Eintraegen (%s)" % (len(raus), e))
            break
        raus.extend(r.get("data", []))
        weiter = (r.get("paging") or {}).get("next")
    return {"data": raus[:hoechstens]}


def beitraege(konto, anzahl):
    r = seiten("%s/media" % konto["ig_id"], konto["token"], anzahl,
               fields="id,media_type,media_product_type,timestamp,permalink,like_count,comments_count,caption")
    if "error" in r:
        print("   Beitraege nicht abrufbar: %s" % r["error"].get("message"))
        return []
    raus = []
    gesamt = len(r.get("data", []))
    if gesamt > 60:
        print("   %d Beitraege — je einer braucht einen eigenen Abruf fuer die "
              "Insights, das dauert ein paar Minuten." % gesamt)
    for x in r.get("data", [])[:anzahl]:
        eintrag = {
            "id": x["id"],
            "datum": x["timestamp"][:10],
            "typ": x.get("media_product_type") or x.get("media_type"),
            "link": x.get("permalink"),
            "likes": x.get("like_count"),
            "kommentare": x.get("comments_count"),
            "anfang": sauber(x.get("caption")),
            # 🚨 Die VOLLE Caption gehoert mit. `anfang` ist auf 90 Zeichen
            # gekuerzt, und der Keyword-CTA steht immer am Ende — wer nur den
            # Anfang durchsucht, findet kein einziges Stichwort und haelt einen
            # laufenden Funnel fuer tot.
            "caption": (x.get("caption") or "").strip(),
        }
        eintrag.update(messwerte(x["id"], konto["token"], BEITRAG_METRIKEN))
        raus.append(eintrag)
    return raus


def storys(konto):
    r = hole("%s/stories" % konto["ig_id"], konto["token"], fields="id,media_type,timestamp,permalink")
    if "error" in r:
        print("   Storys nicht abrufbar: %s" % r["error"].get("message"))
        return []
    raus = []
    for x in r.get("data", []):
        eintrag = {
            "id": x["id"],
            "zeit": x["timestamp"][:16].replace("T", " "),
            "typ": x.get("media_type"),
            "link": x.get("permalink"),
        }
        eintrag.update(messwerte(x["id"], konto["token"], STORY_METRIKEN))
        raus.append(eintrag)
    return raus


def bericht(daten):
    """Markdown mit Obsidian-Frontmatter, damit es sauber im Vault landet."""
    z = ["---", "tags: [content, insights]", "---", "",
         "# Instagram-Zahlen · %s" % daten["stand"], "",
         "Geholt ueber die Meta Graph API. Reichweite heisst: so viele verschiedene",
         "Konten haben den Beitrag gesehen. Speicherungen und Geteilt sind die zwei",
         "Zahlen, die weitere Reichweite bringen.", ""]

    for k in daten["konten"]:
        z += ["## @%s" % k["handle"], "",
              "%s Follower · %s Beitraege gesamt · Seite *%s*" %
              (k["follower"], k["beitraege_gesamt"], k["seite"]), ""]

        if k["beitraege"]:
            z += ["| Datum | Format | Reichweite | Likes | Komm. | Gespeichert | Geteilt | Caption-Anfang |",
                  "|---|---|---|---|---|---|---|---|"]
            for b in k["beitraege"]:
                z.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
                    b["datum"], b["typ"], b.get("reach", "—"), b["likes"], b["kommentare"],
                    b.get("saved", "—"), b.get("shares", "—"), b["anfang"][:46]))
            gesehen = [b.get("reach") for b in k["beitraege"] if isinstance(b.get("reach"), int)]
            if gesehen and k["follower"]:
                schnitt = sum(gesehen) / len(gesehen)
                z += ["", "Durchschnittliche Reichweite: **%d** — das sind %.1f %% deiner Follower." %
                      (schnitt, schnitt / k["follower"] * 100)]
            gesamt_sp = sum(b.get("saved", 0) or 0 for b in k["beitraege"])
            gesamt_ge = sum(b.get("shares", 0) or 0 for b in k["beitraege"])
            z += ["Ueber alle %d Beitraege: **%d Speicherungen**, **%d mal geteilt**." %
                  (len(k["beitraege"]), gesamt_sp, gesamt_ge), ""]
        else:
            z += ["Keine Beitraege abrufbar.", ""]

        if k["storys"]:
            z += ["### Storys, die gerade laufen", "",
                  "| Zeit | Typ | Reichweite | Antworten |", "|---|---|---|---|"]
            for s in k["storys"]:
                z.append("| %s | %s | %s | %s |" % (
                    s["zeit"], s["typ"], s.get("reach", "—"), s.get("replies", "—")))
            z.append("")
        else:
            z += ["*Gerade keine aktive Story. Story-Zahlen gibt Instagram nur innerhalb",
                  "von 24 Stunden heraus — was heute nicht geholt wird, ist morgen weg.*", ""]

    return "\n".join(z)


def main():
    p = argparse.ArgumentParser(description="Instagram-Zahlen holen")
    p.add_argument("--anzahl", type=int, default=25,
                   help="wie viele Beitraege (Standard 25, --alle holt die ganze Historie)")
    p.add_argument("--alle", action="store_true",
                   help="die ganze Historie statt nur der letzten --anzahl")
    p.add_argument("--storys", action="store_true", help="nur die aktiven Storys")
    args = p.parse_args()
    if args.alle:
        args.anzahl = 5000   # weit ueber allem, was realistisch dasteht


    token = zugang()
    liste = konten(token)
    if not liste:
        sys.exit("Kein Instagram-Konto an einer freigegebenen Seite gefunden.\n"
                 "Pruefen: haengt das Konto als Professional-Account an der Seite, und\n"
                 "war die Seite im Freigabe-Dialog beim Token-Erzeugen angehakt?")

    daten = {"stand": datetime.date.today().isoformat(), "konten": []}
    for k in liste:
        print("@%s — %s Follower" % (k["handle"], k["follower"]))
        eintrag = {kk: k[kk] for kk in ("seite", "handle", "follower", "beitraege_gesamt")}
        eintrag["beitraege"] = [] if args.storys else beitraege(k, args.anzahl)
        eintrag["storys"] = storys(k)
        print("   %d Beitraege · %d aktive Storys" % (len(eintrag["beitraege"]), len(eintrag["storys"])))
        daten["konten"].append(eintrag)

    ZIEL.mkdir(parents=True, exist_ok=True)
    roh = ZIEL / ("%s.json" % daten["stand"])
    md = ZIEL / ("%s.md" % daten["stand"])
    roh.write_text(json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")
    md.write_text(bericht(daten), encoding="utf-8")
    print()
    print("Geschrieben:")
    print("  %s" % md)
    print("  %s" % roh)


if __name__ == "__main__":
    main()
