# -*- coding: utf-8 -*-
"""Repariert den Aufzeichnungs-Link und setzt den MBA-Block in die
Stimm-Check-Strecke (Automation 83, „1 Mail Stimcheck nach Masterclass").

    python scripts/ki-kurs/stimmcheck-mba-block.py          # trocken
    python scripts/ki-kurs/stimmcheck-mba-block.py --los    # schreibt

Zwei Funde in derselben Mail (08.10.2026):

  1 Der Knopf „Zur Aufzeichnung" zeigt auf `#aufzeichnung-folgt` — ein
    Platzhalter-Anker. Wer darauf klickt, bleibt stehen. Das ist der einzige
    Link in der ganzen Mail, die Mail ist damit funktionslos.

  2 Die Academy kommt in KEINER der sieben Stimm-Check-Mails vor, obwohl sie
    am Schluss der Masterclass gepitcht wird. Patricia am 08.10.: „ich pitche
    ja auch die mba. da steht jetzt aber nichts mehr drin."

🚨 WER DIESE MAIL BEKOMMT, WAR NICHT LIVE DABEI.
   Die Automation teilt sich in zwei Zweige: wer sich VOR der Masterclass
   eintraegt, bekommt die Einladung; wer sich DANACH eintraegt, bekommt diese
   Mail mit der Aufzeichnung. Deshalb steht hier NICHT „weil du dabei warst" —
   das waere schlicht falsch und faellt sofort auf.

🚨 DIE FRIST IST EINE ENTSCHEIDUNG, KEINE ABLEITUNG.
   Die Webinar-Teilnehmerinnen haben bis Freitag 21 Uhr. Diese Leute kommen
   spaeter herein, fuer sie kann dieselbe Frist nicht gelten. Gesetzt ist der
   Launch-Schluss (Do 23.10.), weil dann ohnehin der ganze Verkauf endet.
   🔁 NACH DEM 23.10. GEHOERT DER BLOCK RAUS — die Automation laeuft evergreen
   weiter, und ein abgelaufenes Datum in einer Dauermail ist schlimmer als
   gar kein Angebot. Dafuer dieses Skript mit --entfernen laufen lassen.
"""
import argparse
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
KAMPAGNE = 792            # „1 Mail  Stimcheck nach Masterclass"

AUFZEICHNUNG = "https://vimeo.com/1233995735/e14aa6e93c?share=copy&amp;fl=sv&amp;fe=ci"
TOT = "#aufzeichnung-folgt"
KASSE = "https://mumlifebalance.thrivecart.com/mba-webinar/"
KURSSEITE = "https://mumlifebalance.ch/ki-kurs/"

# 🔁 Launch-Phase. Ab 16.10. gilt 333 — dann hier und auf der Seite aendern.
KURS_FRIST = "Der Fr&uuml;hbucherpreis von 277 gilt bis Donnerstag, 15. Oktober."

# 🚨 RELATIV, nicht als Datum (Patricias Entscheid 08.10.2026: „und zwar genau
#    24h"). Die Mail laeuft in einer Automation und geht bei jeder neuen
#    Eintragung raus — ein festes Datum steht in drei Wochen abgelaufen da und
#    macht jede weitere Frist unglaubwuerdig. Eine relative Frist stimmt immer.
FRIST = "24 Stunden ab dieser Mail"

CREME, TINTE, GRAU, ORANGE = "#f1ecdd", "#0c1c30", "#5f5748", "#dc822e"

# Direkt nach dem Aufzeichnungs-Knopf, vor dem Gruss.
ANKER = ">Zur Aufzeichnung</a></td></tr></table>"

# ---------------------------------------------------------------------------
# Block 1 · der KI-Kurs
#
# 🚨 Der Kurs steht VOR der Academy, nicht danach. Julia dazu woertlich:
#    „kein Sprung von 0 auf einen Preis im Tausenderbereich". Diese Leute
#    haben gerade ein 0€-Tool geholt — wer ihnen als Erstes 997 hinstellt,
#    verliert die, fuer die 277 der richtige naechste Schritt waere.
#    Dieselbe Reihenfolge wie in „Versand Aufzeichnung" (Mail 801).
#
# 🚨 Der Bonus-Call (Frist Sa 10.10.) steht hier bewusst NICHT drin. Er gilt
#    den Live-Teilnehmerinnen, und diese Mail laeuft evergreen weiter — ein
#    Bonus mit abgelaufener Frist macht jedes weitere Versprechen wertlos.
BLOCK_KURS = (
    '<table width="100%" cellpadding="0" cellspacing="0" border="0" '
    'style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;'
    'border-spacing:0px;margin:30px 0 0 0" role="none" data-pitch="ki-kurs"><tr>'
    '<td style="padding:0;Margin:0" align="left">'

    '<p style="Margin:0;mso-line-height-rule:exactly;font-family:Georgia, serif;'
    'line-height:1.35;margin:0 0 12px 0;font-size:21px;font-weight:bold;color:@TINTE@">'
    'Wenn du das bei dir einrichten willst</p>'

    '<p style="Margin:0;mso-line-height-rule:exactly;font-family:Arial, sans-serif;'
    'line-height:1.85;margin:0 0 14px 0;font-size:16px;color:@TINTE@">'
    'Im Kurs <strong>&bdquo;Easy KI f&uuml;r Networkerinnen &mdash; vom Chat zur '
    'Mitarbeiterin&ldquo;</strong> richtest du dir genau das Schritt f&uuml;r '
    'Schritt ein, in deinem eigenen Tempo. Am Ende hast du einen Arbeitsplatz '
    'mit deinem Wissen drin, deinen ersten eigenen Skill f&uuml;r eine Arbeit, '
    'die jede Woche wiederkommt, und einen Bot, der von selbst l&auml;uft.</p>'

    '<p style="Margin:0;mso-line-height-rule:exactly;font-family:Arial, sans-serif;'
    'line-height:1.85;margin:0 0 16px 0;font-size:16px;color:@GRAU@">'
    'Du f&auml;ngst im Chat an, den du schon kennst, und installierst erst '
    'sp&auml;ter etwas. Die Kapitel kommen ab dem 1. November Woche f&uuml;r '
    'Woche, am 30. November ist der Kurs komplett. @KURSFRIST@</p>'

    '<table width="100%" cellpadding="0" cellspacing="0" border="0" '
    'style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;'
    'border-spacing:0px;margin:4px 0 0 0" role="none"><tr>'
    '<td align="left" style="padding:0;Margin:0">'
    '<a href="@KURSSEITE@" style="mso-line-height-rule:exactly;text-decoration:none;'
    'display:inline-block;background-color:@PETROL@;color:#ffffff;'
    'font-family:Arial, sans-serif;font-size:17px;font-weight:bold;'
    'padding:15px 34px;border-radius:30px" target="_blank">Alles zum Kurs</a>'
    '</td></tr></table>'

    '</td></tr></table>'
)
for _s, _w in (("@TINTE@", "#0c1c30"), ("@GRAU@", "#5f5748"), ("@PETROL@", "#12828c"),
               ("@KURSSEITE@", KURSSEITE), ("@KURSFRIST@", KURS_FRIST)):
    BLOCK_KURS = BLOCK_KURS.replace(_s, _w)

TEXT_KURS = (
    "\n\nWENN DU DAS BEI DIR EINRICHTEN WILLST\n\n"
    "Im Kurs „Easy KI für Networkerinnen — vom Chat zur Mitarbeiterin\" richtest du dir "
    "genau das Schritt für Schritt ein, in deinem eigenen Tempo. Am Ende hast du einen "
    "Arbeitsplatz mit deinem Wissen drin, deinen ersten eigenen Skill für eine Arbeit, "
    "die jede Woche wiederkommt, und einen Bot, der von selbst läuft.\n\n"
    "Du fängst im Chat an, den du schon kennst, und installierst erst später etwas. "
    "Die Kapitel kommen ab dem 1. November Woche für Woche, am 30. November ist der "
    "Kurs komplett. Der Frühbucherpreis von 277 gilt bis Donnerstag, 15. Oktober.\n\n"
    + KURSSEITE + "\n")

BLOCK = (
    '<table width="100%" cellpadding="0" cellspacing="0" border="0" '
    'style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;'
    'border-spacing:0px;margin:26px 0 0 0" role="none" data-mba="stimmcheck"><tr>'
    '<td style="background-color:@CREME@;border-radius:14px;padding:24px 24px;" align="left">'

    '<p style="Margin:0;mso-line-height-rule:exactly;font-family:Georgia, serif;'
    'line-height:1.35;margin:0 0 12px 0;font-size:20px;font-weight:bold;color:@TINTE@">'
    'Und wenn du gleich alles willst</p>'

    '<p style="Margin:0;mso-line-height-rule:exactly;font-family:Arial, sans-serif;'
    'line-height:1.75;margin:0 0 14px 0;font-size:16px;color:@GRAU@">'
    'In der Masterclass zeige ich am Schluss die Mum Business Academy: alle vier Kurse, der '
    'KI-Kurs ab dem 1. November inklusive, dazu ein ganzes Jahr Begleitung in '
    'der Gruppe und zweimal im Monat ein Call. Wer live dabei war, bekommt sie '
    'zum Webinar-Preis &mdash; und weil du dir die Aufzeichnung anschaust, '
    'gilt das f&uuml;r dich genauso.</p>'

    '<p style="Margin:0;mso-line-height-rule:exactly;font-family:Arial, sans-serif;'
    'line-height:1.7;margin:0 0 6px 0;font-size:17px;font-weight:bold;color:@TINTE@">'
    '997 statt 1347.</p>'

    '<p style="Margin:0;mso-line-height-rule:exactly;font-family:Arial, sans-serif;'
    'line-height:1.75;margin:0 0 14px 0;font-size:16px;color:@GRAU@">'
    'Oder in sechs Raten zu 166.20, derselbe Betrag auf sechs Monate verteilt. '
    'Das Fenster bleibt einen Tag offen, danach kostet die Academy wieder 1347.</p>'

    '<p style="Margin:0;mso-line-height-rule:exactly;font-family:Arial, sans-serif;'
    'line-height:1.6;margin:0 0 18px 0;font-size:14px;font-weight:bold;'
    'text-transform:uppercase;letter-spacing:1px;color:#b56a24">@FRIST@</p>'

    '<a href="@KASSE@" style="mso-line-height-rule:exactly;text-decoration:none;'
    'display:inline-block;background-color:@ORANGE@;color:#ffffff;'
    'font-family:Arial, sans-serif;font-size:17px;font-weight:bold;'
    'padding:15px 34px;border-radius:30px" target="_blank">'
    'Zur Academy f&uuml;r 997</a>'

    '</td></tr></table>'
)
for _s, _w in (("@CREME@", CREME), ("@TINTE@", TINTE), ("@GRAU@", GRAU),
               ("@ORANGE@", ORANGE), ("@FRIST@", FRIST), ("@KASSE@", KASSE)):
    BLOCK = BLOCK.replace(_s, _w)

TEXT_BLOCK = (
    "\n\nUND WENN DU GLEICH ALLES WILLST\n\n"
    "In der Masterclass zeige ich am Schluss die Mum Business Academy: alle vier Kurse, der KI-Kurs "
    "ab dem 1. November inklusive, dazu ein ganzes Jahr Begleitung in der Gruppe und "
    "zweimal im Monat ein Call. Wer live dabei war, bekommt sie zum Webinar-Preis — "
    "und weil du dir die Aufzeichnung anschaust, gilt das für dich genauso.\n\n"
    "997 statt 1347. Oder in sechs Raten zu 166.20, derselbe Betrag auf sechs Monate "
    "verteilt. Das Fenster bleibt einen Tag offen, danach kostet die Academy wieder "
    "1347.\n\n" + FRIST.upper() + "\n\n" + KASSE.replace("&amp;", "&") + "\n")


def zugang():
    env = {}
    for z in (ROOT / "04-projects/activecampaign-mcp/.env").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*([A-Z_]+)\s*=\s*(.+?)\s*$", z)
        if m:
            env[m.group(1)] = m.group(2).strip("\"'")
    assert env.get("AC_API_KEY"), "AC-Zugang fehlt in der .env"
    return env["AC_API_URL"].rstrip("/"), env["AC_API_KEY"]


U, K = zugang()


def ac(pfad, methode="GET", daten=None):
    r = urllib.request.Request(
        U + "/api/3/" + pfad, method=methode,
        headers={"Api-Token": K, "Content-Type": "application/json"},
        data=json.dumps(daten).encode("utf-8") if daten else None)
    try:
        return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e:
        print("   HTTP %s: %s" % (e.code, e.read().decode("utf-8", "replace")[:220]))
        raise


def sprachpruefung(text):
    """Patricias Verbote. Geprueft wird der SICHTBARE Text, nicht das Markup —
    sonst schlaegt jede Regel auf CSS und Kommentare an."""
    sicht = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text))
    import html as _h
    klar = _h.unescape(sicht)
    raus = []
    for muster, name in [
            (r"[Nn]icht[^.!?]{0,80}[,.]\s*[Ss]ondern", "Nicht-X-sondern-Y"),
            (r"[Ss]tell(e)? dir[^.!?]{0,40}vor", "Stell dir vor"),
            (r"\bnie wieder\b", "nie wieder"),
            (r"ß", "deutsches Eszett")]:
        if re.search(muster, klar):
            raus.append(name)
    # Umlaut-Umschrift: echte ae/oe/ue-Woerter sind erlaubt
    erlaubt = ("auch", "auf", "aus", "neue", "genau", "dauer", "bauen", "heute",
               "zuerst", "frauen", "beque", "abenteuer", "teuer", "treue")
    schlecht = [w for w in re.findall(r"\b\w*(?:ae|oe|ue)\w*\b", klar)
                if not w.lower().startswith(erlaubt)]
    if schlecht:
        raus.append("Umlaut-Umschrift %s" % sorted(set(schlecht))[:3])
    return raus


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--los", action="store_true", help="schreibt nach ActiveCampaign")
    ap.add_argument("--entfernen", action="store_true",
                    help="🔁 nach dem 23.10.: nimmt den MBA-Block wieder heraus")
    args = ap.parse_args()

    name = ac("campaigns/%s" % KAMPAGNE)["campaign"].get("name")
    ms = ac("campaigns/%s/campaignMessages" % KAMPAGNE).get("campaignMessages", [])
    assert ms, "keine Nachricht an der Kampagne"
    mid = ms[0]["message"]
    msg = ac("messages/%s" % mid)["message"]
    h, txt = msg.get("html") or "", msg.get("text") or ""

    print("%s  (Kampagne %s · Nachricht %s)" % (name, KAMPAGNE, mid))
    print("Automation 83 · Zweig „nach Masterclass\" — diese Leute waren "
          "NICHT live dabei.\n")

    if args.entfernen:
        n = h.count('data-mba="stimmcheck"') + h.count('data-pitch="ki-kurs"')
        if not n:
            print("   Keine Pitch-Blöcke drin — nichts zu tun."); return
        neu_h = re.sub(r'<table[^>]*data-mba="stimmcheck".*?</table>', "", h, flags=re.S)
        # 🚨 Der Kurs-Block hat eine INNERE Tabelle (den Knopf). Ein nicht-gieriges
        #    `.*?</table>` wuerde am inneren Ende stoppen und die Huelle stehen
        #    lassen — deshalb bis zum abschliessenden </td></tr></table>.
        neu_h = re.sub(r'<table[^>]*data-pitch="ki-kurs".*?</td></tr></table>\s*</td></tr></table>',
                       "", neu_h, flags=re.S)
        # 🚨 Im Textteil NICHT gegen die Konstanten vergleichen: sobald eine
        #    Frist geaendert wurde, passen sie nicht mehr auf den Stand in AC,
        #    und der alte Absatz bleibt stehen. Von der Ueberschrift bis zum
        #    jeweiligen Link raeumen trifft jede Fassung.
        neu_t = re.sub(r"\n*WENN DU DAS BEI DIR EINRICHTEN WILLST.*?"
                       + re.escape(KURSSEITE) + r"\n*", "\n\n", txt, flags=re.S)
        neu_t = re.sub(r"\n*UND WENN DU GLEICH ALLES WILLST.*?"
                       + re.escape(KASSE.replace("&amp;", "&")) + r"\n*",
                       "\n\n", neu_t, flags=re.S)
        print("   %d Blöcke gefunden · HTML %d → %d" % (n, len(h), len(neu_h)))
        if not args.los:
            print("\nTrockenlauf. Mit --los wird geschrieben."); return
        ac("messages/%s" % mid, "PUT", {"message": {"html": neu_h, "text": neu_t}})
        nach = ac("messages/%s" % mid)["message"].get("html") or ""
        rest = nach.count('data-mba="stimmcheck"') + nach.count('data-pitch="ki-kurs"')
        print("   gespeichert · Gegenprobe: %s" %
              ("sauber ✓" if not rest else "\U0001f6a8 %d STEHEN NOCH DRIN" % rest))
        return

    neu_h, neu_t, getan = h, txt, []

    # --- 1 · toter Anker -> Aufzeichnung -------------------------------------
    if TOT in neu_h:
        neu_h = neu_h.replace(TOT, AUFZEICHNUNG)
        neu_t = neu_t.replace(TOT, AUFZEICHNUNG.replace("&amp;", "&"))
        getan.append("toter Anker → Aufzeichnung")
    elif "vimeo" in neu_h or "ki-masterclass-replay" in neu_h:
        getan.append("Link war schon repariert")
    else:
        print("   \U0001f6a8 Weder toter Anker noch Aufzeichnungs-Link gefunden."); sys.exit(1)

    # --- 2 · beide Pitches, Kurs zuerst -------------------------------------
    #     Patricia am 08.10.2026: „in stimcheck 1 kommt die mba UND der ki kurs.
    #     in mail 2 dann wie schon jetzt drin nur der KI Kurs."
    if 'data-mba="stimmcheck"' in neu_h or 'data-pitch="ki-kurs"' in neu_h:
        print("   Blöcke stehen schon drin — erst --entfernen --los laufen lassen.")
    else:
        n = neu_h.count(ANKER)
        assert n == 1, "Anker kommt %dx vor (erwartet 1): %r" % (n, ANKER)
        neu_h = neu_h.replace(ANKER, ANKER + BLOCK_KURS + BLOCK)
        gruss = "Viel Spass beim Anschauen"
        zusatz = TEXT_KURS.rstrip() + "\n" + TEXT_BLOCK
        neu_t = (neu_t.replace(gruss, zusatz.strip() + "\n\n" + gruss, 1)
                 if gruss in neu_t else neu_t + zusatz)
        getan.append("KI-Kurs-Block und MBA-Block eingesetzt")

    for g in getan:
        print("   ✓ %s" % g)
    print("   HTML : %d → %d (+%d)" % (len(h), len(neu_h), len(neu_h) - len(h)))
    print("   Frist: %s   \U0001f501 danach mit --entfernen --los herausnehmen" % FRIST)

    probleme = sprachpruefung(BLOCK_KURS + BLOCK)
    print("   Sprachprüfung: %s" % ("sauber ✓" if not probleme else " | ".join(probleme)))
    if probleme:
        sys.exit(1)

    if not args.los:
        print("\nTrockenlauf. Mit --los wird geschrieben.")
        return

    ac("messages/%s" % mid, "PUT", {"message": {"html": neu_h, "text": neu_t}})
    nach = ac("messages/%s" % mid)["message"].get("html") or ""
    ok = (TOT not in nach and "vimeo" in nach
          and 'data-mba="stimmcheck"' in nach and "997 statt 1347" in nach)
    print("\n   gespeichert · Gegenprobe: %s" % ("sauber ✓" if ok else "\U0001f6a8 WEICHT AB"))
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
