"""Sammelt die Kosten — mit dem Beleg daneben, und sagt, wo keiner liegt.

Der Monatsbogen verlangt Umsatz, Kosten und Gewinn. Der Umsatz kommt seit dem
24.09.2026 aus ThriveCart. Bei den Kosten gibt es **drei** Quellen, und sie
sind unterschiedlich viel wert:

| Quelle | Umfang | Beleg dabei? |
|---|---|---|
| `belege/_ausgepackt.json` | Juni–September 2026 | **ja, Originaldatei** |
| `belege-index-2026.md` | Februar–Mai 2026 | nein, nur Tabellenzeile |
| Notion «Kostenpositionen» | Dezember 2025, Januar 2026 | nein |

🚨 **Eine Tabellenzeile ist kein Beleg.** Patricia am 24.09.2026: *„belege
müssen aber mitabgelegt werden oder verknüpft werden. muss das ja alles
belegen"*. Sie hat recht — bei einer Nachfrage vom Steueramt zaehlt das
Dokument, nicht die Liste. Deshalb traegt jeder Posten das Feld `belege` mit
den Dateinamen, und `ohne_beleg` zaehlt, wie viele keines haben.

🚨 **Deshalb wird KEIN Gewinn gerechnet, wo Kosten fehlen.** Umsatz minus
unvollstaendige Kosten ergibt eine Zahl, die aussieht wie ein Gewinn und in
Wahrheit zu hoch ist — und zwar umso mehr, je schlechter erfasst wurde. Eine
fehlende Zahl merkt man; eine falsche nicht.

🚨 **USD-Betraege werden nicht in Franken umgerechnet.** Der echte
Frankenbetrag steht auf der Kreditkartenabrechnung und weicht vom Tageskurs ab.
Sie werden getrennt ausgewiesen, nie zusammengezaehlt.

🚨 **Rechnung und Quittung sind zwei Dateien, aber EIN Posten.** Stripe haengt
beide an. Nur die Quittung nennt den bezahlten Betrag; die Rechnung nennt die
Leistung. Wer beide als Posten zaehlt, verdoppelt die Kosten. Gruppiert wird
deshalb nach Datum und Anbieter.

    python scripts/cockpit/kosten-bauen.py
"""

import json
import re
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
BELEGE = ROOT / "context" / "finanzen" / "2026" / "belege"
INDEX = ROOT / "context" / "finanzen" / "2026" / "belege-index-2026.md"

MONATE = {"Jan": "01", "Feb": "02", "Mär": "03", "Mar": "03", "Apr": "04",
          "Mai": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09",
          "Okt": "10", "Nov": "11", "Dez": "12"}

# Anbieterkuerzel aus dem Dateinamen -> Klartext fuer die Buchung.
KLARTEXT = {
    "anthropic": "Anthropic (Claude)",
    "railway": "Railway (Bot-Hosting)",
    "supabase": "Supabase (Datenbank)",
    "manychat": "ManyChat",
    "openai": "OpenAI",
    "openai-ads": "OpenAI (ChatGPT-Werbung)",
    "canva": "Canva",
    "vercel": "Vercel",
    "apify": "Apify",
    "meta": "Meta (Werbung)",
}
# 🚨 ChatGPT-Werbung bucht die Karte als „OPENAI · Computersoftware" — wie die
# API. Getrennt halten, sonst landet Werbung unter Tools. Beleg ist die
# Kreditkartenabrechnung, OpenAI schickt keine Quittung per Mail (28.10.2026).
ART = {"meta": "Werbung", "openai-ads": "Werbung"}   # alles andere sind Tools

# Aus Notion «Kostenpositionen» uebernommen (9 Zeilen, Stand 24.09.2026).
# Monate dort als Spalten — hier als Zeilen aufgeloest.
NOTION_KOSTEN = [
    ("2025-12", "Hostar Domain", "Tools", 14.95, "CHF"),
    ("2025-12", "Hostar Webhosting", "Tools", 166.80, "CHF"),
    ("2026-01", "Basic Quarterly (ImagineArt)", "Tools", 36.00, "CHF"),
    ("2026-01", "Microsoft 365", "Tools", 9.95, "CHF"),
    ("2026-01", "Meta Verified Instagram", "Tools", 13.95, "CHF"),
    ("2026-01", "Meta Ads", "Werbung", 93.43, "CHF"),
    ("2026-01", "Canva", "Tools", 99.77, "CHF"),
    ("2026-01", "Flug Convention Katovice", "Fortbildung", 531.70, "CHF"),
]

# Laufende Abos, die ueber **Google Play** abgerechnet werden und deshalb nie
# als Anbieter-Rechnung im Postfach auftauchen. Gefunden am 24.09.2026, nachdem
# Patricia gesagt hat: „ne microsoft 365 und meta verified habe ich immer noch".
#
# 🚨 Eine Suche nach dem Anbieternamen findet sie NICHT. Absender ist
# `googleplay-noreply@google.com`, und bezahlt wird per PayPal ueber
# **pnulmann@gmx.ch** — eine zweite Adresse. Wer nur nach „from:microsoft"
# sucht, haelt ein laufendes Abo fuer gekuendigt.
#
# 🚨 Der Preis ist belegt, der einzelne Monat nicht. Beide Belege sagen
# ausdruecklich „Monthly" und „Abo mit automatischer Verlaengerung", und es gibt
# Belege am Anfang und am Ende des Zeitraums — die Monate dazwischen sind damit
# sicher, aber sie tragen `abgeleitet` und haben KEINE Datei. Ein abgeleiteter
# Posten darf nie als nachgewiesen zaehlen.
ABOS = [
    # Name, Art, Betrag, Waehrung, ab Monat, Tag, Herkunft, Erkennungswort
    #
    # 🚨 Das Erkennungswort steht ausdruecklich dabei und ist NICHT das
    # erste Wort des Namens. Mit „meta" wurde Meta Verified in jedem Monat
    # unterdrueckt, in dem eine Zeile „Meta Ads" stand — also in genau den
    # Monaten mit Werbung. Fuenf von zehn Zeilen fehlten, und die Ausgabe sah
    # trotzdem plausibel aus. Ein Muster muss so eng sein, dass es nur das
    # trifft, was es treffen soll.
    ("Microsoft 365 Personal", "Tools", 9.95, "CHF", "2026-02", 16,
     "belegt 16.05. und 16.08.2026 ueber Google Play", "microsoft"),
    ("Meta Verified (Instagram)", "Tools", 13.95, "CHF", "2026-02", 11,
     "belegt 11.05. und 11.09.2026 ueber Google Play", "verified"),
]

# ⚠ Noch nicht gebucht, weil unklar ist, ob geschaeftlich — Patricia fragen:
#   CapCut Jahresabo (Schnitt-App, laeuft bis 24.10.2026, dann gekuendigt)
#   Telegram Premium Jahresabo (04.05., steht im Index als „Business?")
#
# 🚨 „SKYWORK AI PTE. LTD." ist NICHT gemeint — das ist die Firma hinter
# der App **DramaWave (Dramas & Reels)**, also Unterhaltung und privat. Im
# Beleg steht die Firma gross und die App klein, und ein KI-klingender
# Firmenname macht aus einer Serien-App kein Werkzeug. Einmal CHF 11.00 am
# 19.08.2026, in der Gratiswoche gekuendigt, beendet am 26.08. — die CHF 16.00
# pro Woche danach sind nie geflossen. **Vor jeder Warnung den Artikelnamen
# lesen, nicht den Firmennamen.**
UNGEKLAERT = ["CapCut Jahresabo", "Telegram Premium"]


def aus_abos(vorhanden):
    """Monatszeilen fuer laufende Abos — nur wo noch keine Zeile steht."""
    from datetime import date as _d
    heute = _d.today()
    raus = []
    for name, art, betrag, whr, ab, tag, woher, kurz in ABOS:
        j, m = int(ab[:4]), int(ab[5:7])
        while (j, m) <= (heute.year, heute.month):
            monat = "%04d-%02d" % (j, m)
            # Schon im Index oder in Notion? Dann nicht doppelt buchen.
            doppelt = any(monat == v[0] and kurz in v[1].lower() for v in vorhanden)
            if not doppelt and not (j == heute.year and m == heute.month
                                    and heute.day < tag):
                raus.append({
                    "monat": monat,
                    "datum": "%s-%02d" % (monat, tag),
                    "was": name,
                    "art": art,
                    "betrag": betrag,
                    "waehrung": whr,
                    "quelle": "Google Play (Abo)",
                    "belege": [],
                    "abgeleitet": True,
                    "beleg_holen": "Beleg je Monat aus dem Postfach holen — %s" % woher,
                })
            m += 1
            if m > 12:
                m, j = 1, j + 1
    return raus


# 🚨 Der ManyChat-Betrag steht nicht im PDF, weil ManyChat keines anhaengt —
# die Rechnung steht im Mailtext, und der liegt als .eml im Belegordner.
# Ausgelesen am 24.09.2026, alle drei Monate 15.00 USD.
AUS_MAIL = {("2026-07-08", "manychat"): 15.00,
            ("2026-08-08", "manychat"): 15.00,
            ("2026-09-08", "manychat"): 15.00}


# Gefunden am 24.09.2026 beim **systematischen** Durchgang durchs Postfach.
#
# 🚨 Der Anlass war Patricias Einwand „nein der groesste teil ist in
# gmail. hast du das mal so erfasst?" — und sie hatte recht. Bis dahin wurde
# **anbieterweise** gesucht, mit einer Liste, die schon bekannt war. Wer nicht
# daraufstand, wurde nie gefunden: Google Play, Google Cloud, Groimpact und
# drei zugekaufte Kurse lagen die ganze Zeit in Gmail.
#
# **Die Lehre: nach Belegen suchen, nicht nach Anbietern.** Die Suche laeuft
# ueber Betreff-Woerter (Rechnung, Beleg, Quittung, Invoice, Receipt,
# Bestellung, Zahlung, Abo) und schliesst die bekannten privaten Absender aus
# — nicht umgekehrt.
NEUE_FUNDE = [
    # Monat, Datum, Was, Art, Betrag, Waehrung, Quelle
    ("2026-09", "2026-09-15", "Google Cloud Platform & APIs", "Tools",
     25.00, "CHF", "Google-Zahlungsbestaetigung"),
    ("2026-09", "2026-09-04", "CapCut Masterclass (Kurs)", "Fortbildung",
     29.00, "EUR", "ablefy-Bestellbestaetigung"),
]

# ⚠ Gefunden, aber OHNE Betrag in der Mail — nicht gebucht, siehe unten.
# Ein Posten ohne Betrag ist keine Buchung, und ein geschaetzter waere schlimmer
# als gar keiner.
OHNE_BETRAG = [
    ("2026-09-06", "Groimpact (Instagram-Wachstum)", "Betrag steht nicht in der Mail"),
    ("2026-08-25", "Karla Brenscheidt — Hook-Prompt fuer Claude", "Betrag steht nicht in der Mail"),
    ("2026-09-18", "Karla Brenscheidt — Test-Reel in 5 Schritten", "Betrag steht nicht in der Mail"),
    ("2026-09-10", "MediaMarkt Bestellung 327653104", "Inhalt unklar — Technik fuers Business?"),
]

# ⚠ Geprueft und als PRIVAT eingestuft (Patricias Entscheid bzw. eindeutig):
#   mybodyadvice by Lisa (Ernaehrungscoaching) — Patricia, 24.09.2026
#   DramaWave/SKYWORK · Temu · Jumbo · Decathlon · Galaxus · Apfelkiste
#   VEVOR (Rankhilfe, Garten) · ahead-nutrition · Europa-Park · Interrail
#   Uber Eats · Too Good To Go · YouTube-Film · Ricardo-Verkauf
PRIVAT_GEPRUEFT = ["mybodyadvice by Lisa", "DramaWave", "Temu", "Jumbo",
                   "Decathlon", "Galaxus", "Apfelkiste", "VEVOR",
                   "ahead-nutrition", "Europa-Park", "Interrail", "Uber Eats",
                   "Too Good To Go", "YouTube", "Ricardo"]


def aus_belegordner():
    """Die Posten, hinter denen eine echte Datei liegt."""
    p = BELEGE / "_ausgepackt.json"
    if not p.exists():
        return []
    try:
        roh = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []

    # Rechnung + Quittung gehoeren zusammen — siehe Kopf.
    gruppen = defaultdict(list)
    for e in roh:
        gruppen[(e["datum"], e["anbieter"])].append(e)

    raus = []
    for (tag, anbieter), teile in sorted(gruppen.items()):
        mit_betrag = [t for t in teile if t.get("betrag")]
        betrag = mit_betrag[0]["betrag"] if mit_betrag else \
            AUS_MAIL.get((tag, anbieter))
        whr = mit_betrag[0]["waehrung"] if mit_betrag else "USD"
        if betrag is None:
            print("  ⚠️ %s %s — Beleg da, Betrag unklar. Nicht gebucht."
                  % (tag, anbieter))
            continue
        raus.append({
            "monat": tag[:7],
            "datum": tag,
            "was": KLARTEXT.get(anbieter, anbieter.title()),
            "art": ART.get(anbieter, "Tools"),
            "betrag": betrag,
            "waehrung": whr,
            "quelle": "Belegordner",
            "belege": sorted(t["datei"] for t in teile),
        })
    return raus


def aus_werbekonto():
    """Werbeausgaben aus dem Meta-Werbekonto.

    🚨 Diese Kosten kommen NIE per Mail, weil Meta ueber das Werbekonto
    abrechnet. Wer die Buchhaltung aus dem Postfach rekonstruiert, uebersieht
    sie vollstaendig. Befund vom 24.09.2026: CHF 834 in 2026, davon standen
    CHF 0 in den Buechern.

    🚨 Die Zahl ist belegt, das Dokument nicht. `belege` bleibt leer und
    `beleg_holen` sagt, wo die Rechnung liegt — sonst zaehlt der Posten als
    nachgewiesen, obwohl kein Papier dahinter ist.
    """
    p = Path(__file__).resolve().parents[2] / "outputs" / "cockpit" /         "abgleich" / "meta-werbekosten.json"
    if not p.exists():
        return []
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []
    raus = []
    for m in d.get("monate") or []:
        if not m.get("betrag"):
            continue
        raus.append({
            "monat": m["monat"],
            "datum": m["monat"] + "-01",
            "was": "Meta Ads (Instagram/Facebook)",
            "art": "Werbung",
            "betrag": m["betrag"],
            "waehrung": m.get("waehrung") or "CHF",
            "quelle": "Meta-Werbekonto",
            "belege": [],
            "beleg_holen": d.get("beleg_hinweis", ""),
        })
    return raus


def aus_index(jahr="2026"):
    """Die aelteren Posten aus der Tabelle — ohne Datei dahinter."""
    if not INDEX.exists():
        return [], "Belege-Index nicht gefunden"
    raus = []
    for z in INDEX.read_text(encoding="utf-8").splitlines():
        if not z.strip().startswith("|"):
            continue
        sp = [x.strip() for x in z.strip().strip("|").split("|")]
        if len(sp) < 6:
            continue
        mon = MONATE.get(sp[0])
        if not mon:
            continue          # Kopf-, Trenn- und Summenzeilen
        try:
            betrag = float(sp[3].replace("'", "").replace(",", "."))
        except ValueError:
            continue
        tag = ""
        m = re.match(r"(\d{2})\.(\d{2})\.", sp[1])
        if m:
            tag = "%s-%s-%s" % (jahr, m.group(2), m.group(1))
        raus.append({
            "monat": "%s-%s" % (jahr, mon),
            "datum": tag,
            "was": re.sub(r"\*\*", "", sp[2])[:70],
            # Sternchen aus dem Markdown ("Telegram*") sonst eigene Art.
            "art": (sp[5] or "Sonstiges").strip("*"),
            "betrag": betrag,
            "waehrung": sp[4] or "CHF",
            "quelle": "Belege-Index",
            "belege": [],
        })
    return raus, ""


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    posten = aus_belegordner()
    belegt_monate = {p["monat"] for p in posten}

    # Werbung laeuft parallel zu den Tools, nie statt ihnen — deshalb kommt
    # sie dazu und wird nicht gegen den Belegordner abgewogen.
    werbung = aus_werbekonto()
    schon = {(p["monat"], p["art"]) for p in posten}
    posten += [w for w in werbung if (w["monat"], w["art"]) not in schon]

    alt, fehler = aus_index()
    # Der Belegordner gewinnt: wo eine Datei liegt, zaehlt die, nicht die Zeile.
    posten += [a for a in alt if a["monat"] not in belegt_monate]

    # 🚨 Die Notion-Zeile "Meta Ads 93.43" steht auf Januar 2026, das
    # Werbekonto weist fuer Januar aber nichts aus. Entweder ist es
    # Dezember-Ausgabe, die im Januar abgerechnet wurde, oder ein anderes
    # Konto. Sie bleibt drin und traegt einen Vermerk — geraten wird nicht.
    # Abos NACH Index und Notion, damit die dortigen Zeilen gewinnen.
    for m, was, art, betrag, whr in NOTION_KOSTEN:
        eintrag = {"monat": m, "datum": "", "was": was, "art": art,
                   "betrag": betrag, "waehrung": whr, "quelle": "Notion",
                   "belege": []}
        if art == "Werbung":
            eintrag["pruefen"] = ("Das Meta-Werbekonto weist fuer diesen Monat "
                                  "nichts aus — Zeitraum oder Konto pruefen.")
        posten.append(eintrag)

    for m, tag, was, art, betrag, whr, quelle in NEUE_FUNDE:
        posten.append({"monat": m, "datum": tag, "was": was, "art": art,
                       "betrag": betrag, "waehrung": whr, "quelle": quelle,
                       "belege": []})

    posten += aus_abos([(p["monat"], p["was"]) for p in posten])

    monate = defaultdict(lambda: defaultdict(float))
    arten = defaultdict(float)
    for p in posten:
        monate[p["monat"]][p["waehrung"]] += p["betrag"]
        if p["waehrung"] == "CHF":
            arten[p["art"]] += p["betrag"]

    # Welche Monate haben Umsatz, aber keine Kosten? Genau die sind die Luecke.
    u = ziel / "umsatz.json"
    mit_umsatz = set()
    if u.exists():
        try:
            for m in json.loads(u.read_text(encoding="utf-8")).get("monate") or []:
                if (m.get("umsatz") or 0) > 0:
                    mit_umsatz.add(m["monat"])
        except Exception:
            pass
    luecken = sorted(m for m in mit_umsatz if m not in monate)

    liste = []
    for m in sorted(monate.keys(), reverse=True):
        drin = [p for p in posten if p["monat"] == m]
        liste.append({
            "monat": m,
            "chf": round(monate[m].get("CHF", 0), 2),
            "usd": round(monate[m].get("USD", 0), 2),
            "posten": len(drin),
            "mit_beleg": len([p for p in drin if p["belege"]]),
        })

    ohne_beleg = [p for p in posten if not p["belege"]]

    daten = {
        "monate": liste,
        "posten": sorted(posten, key=lambda p: (p["monat"], p["datum"]),
                         reverse=True),
        "nach_art": {k: round(v, 2) for k, v in sorted(arten.items())},
        "luecken": luecken,
        "ohne_beleg": len(ohne_beleg),
        "mit_beleg": len(posten) - len(ohne_beleg),
        "belegordner": str(BELEGE.relative_to(ROOT)).replace("\\", "/"),
        "stand": date.today().isoformat(),
        "quellen": ["context/finanzen/2026/belege/ (Juni–September, mit Datei)",
                    "context/finanzen/2026/belege-index-2026.md (Feb–Mai)",
                    "Notion «Kostenpositionen» (Dez 2025, Jan 2026)"],
        "hinweis": ("Kein Gewinn wird gerechnet, wo Kosten fehlen. USD-Beträge "
                    "stehen getrennt — der echte Frankenbetrag steht auf der "
                    "Kreditkartenabrechnung. «Ohne Beleg» heisst: der Posten "
                    "ist erfasst, aber es liegt keine Datei dazu."),
        "gebaut": datetime.now().isoformat(timespec="seconds"),
    }

    (ziel / "kosten.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    print("  %d Kostenposten in %d Monaten · %d mit Beleg, %d ohne"
          % (len(posten), len(liste), daten["mit_beleg"], daten["ohne_beleg"]))
    if fehler:
        print("  ⚠️ %s" % fehler)
    print()
    print("  %-9s %10s %10s %7s %9s" % ("Monat", "CHF", "USD", "Posten", "m. Beleg"))
    for e in liste:
        print("  %-9s %10.2f %10.2f %7d %9s"
              % (e["monat"], e["chf"], e["usd"], e["posten"],
                 "%d/%d" % (e["mit_beleg"], e["posten"])))
    print()
    print("  Nach Art (nur CHF): %s"
          % " · ".join("%s %.0f" % kv for kv in daten["nach_art"].items()))
    if luecken:
        print()
        print("  🚨 Monate MIT Umsatz, aber OHNE erfasste Kosten:")
        print("     %s" % ", ".join(luecken))
    abgeleitet = [p for p in posten if p.get("abgeleitet")]
    if abgeleitet:
        print()
        print("  %d Monatszeilen aus laufenden Abos abgeleitet (Preis belegt, "
              "Monatsbeleg fehlt)." % len(abgeleitet))
    print()
    print("  ⚠ Noch nicht gebucht, Zuordnung unklar: %s"
          % " · ".join(UNGEKLAERT))
    print()
    print("  ⚠ Gefunden, aber ohne Betrag — nicht gebucht:")
    for tag, was, warum in OHNE_BETRAG:
        print("     %s  %-42s %s" % (tag, was, warum))
    print()
    print("  Als privat geprueft und draussen gelassen: %d Absender"
          % len(PRIVAT_GEPRUEFT))
    if ohne_beleg:
        print()
        print("  🚨 %d Posten ohne Belegdatei — bei einer Nachfrage nicht "
              "nachweisbar." % len(ohne_beleg))
        print("     Aelteste: %s" % ", ".join(
            sorted({p["monat"] for p in ohne_beleg})[:6]))
    print("\nAbgelegt in: %s" % (ziel / "kosten.json"))


if __name__ == "__main__":
    main()
