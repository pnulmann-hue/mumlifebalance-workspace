"""Sortiert die ungelesenen Mails in GMX und info@mumlifebalance.ch.

Dieselben Regeln wie beim Gmail-Aufräumen vom 01.10.2026:
Werbung, Technik, Rezepte, Garten und Belege wandern in eigene Ordner,
alles, was Patricia selbst ansehen sollte, bleibt im Posteingang.

    python scripts/mail-sortieren/sortieren.py            # nur anzeigen (trocken)
    python scripts/mail-sortieren/sortieren.py --los      # wirklich verschieben
    python scripts/mail-sortieren/sortieren.py --nur gmx  # nur ein Postfach

Regeln:
- Nichts wird gelöscht, nichts als gelesen markiert (BODY.PEEK, Flags bleiben).
- Ohne --los wird nur gezählt und der Bericht geschrieben.
- Zugangsdaten nur aus scripts/mail-sortieren/.env (gitignored).
"""

import argparse
import datetime as dt
import email
import email.utils
import imaplib
import re
import sys
from email.header import decode_header, make_header
from pathlib import Path

HIER = Path(__file__).resolve().parent
WURZEL = HIER.parent.parent
BERICHTE = WURZEL / "outputs" / "mail-sortieren"

KONTEN = {
    # GMX lehnt weitere Ordner mit "quota exceeded" ab (01.10.2026) -> bestehende Ordner nehmen.
    "gmx": {"name": "GMX", "host": "imap.gmx.net", "user": "GMX_USER", "pass": "GMX_PASS",
            "ordner": {"finanzen": "INBOX/Rechnungen", "garten": "INBOX/Garteninfos",
                       "rezepte": "INBOX/Backen", "pakete": "Archiv", "technik": "Archiv",
                       "community": "Archiv", "betrug": "INBOX/Zu löschen",
                       "erledigt": "Archiv"}},
    "info": {"name": "info@mumlifebalance.ch", "host": "mail.mumlifebalance.ch",
             "user": "INFO_USER", "pass": "INFO_PASS"},
}

# Ordner, in die verschoben wird. Alles andere bleibt im Posteingang.
ORDNER = {
    "newsletter": "Sortiert/Newsletter und Werbung",
    "technik": "Sortiert/Technik und Bots",
    "rezepte": "Sortiert/Rezepte",
    "garten": "Sortiert/Garten",
    "finanzen": "Sortiert/Finanzen",
    "pakete": "Sortiert/Pakete und Lieferungen",
    "community": "Sortiert/Community-Benachrichtigungen",
    "betrug": "Sortiert/Betrug",
    "erledigt": "Sortiert/Erledigt",
}

BLEIBT = {
    "sicherheit": "Konto & Sicherheit",
    "business": "Business & Verkäufe",
    "doterra": "doTERRA (Bestellung/Konto)",
    "technik-fehler": "Technik — Fehler, der Handeln verlangt",
    "privat": "Privat & Familie",
    "mensch": "Persönlich / nicht eindeutig",
}


def umschrift(s):
    s = s.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        s = s.replace(a, b)
    return s


def hat(text, woerter):
    return any(w in text for w in woerter)


SICHERHEIT = ["neue anmeldung", "new sign-in", "new sign in", "sicherheitswarnung", "security alert",
              "passwort", "password", "bestaetigungscode", "verification code", "sicherheitscode",
              "zwei-faktor", "two-factor", "2fa", "neues geraet", "new device", "login-versuch",
              "konto gesperrt", "account locked", "verdaechtig"]
FINANZEN = ["rechnung", "invoice", "receipt", "quittung", "beleg", "zahlungsbestaetigung",
            "payment received", "your payment", "ihre zahlung", "deine zahlung", "abrechnung",
            "kontoauszug", "gutschrift", "mahnung", "zahlungserinnerung", "order confirmation",
            "bestellbestaetigung", "kaufbestaetigung"]
BUSINESS_ABSENDER = ["thrivecart", "activecampaign", "activehosted", "stripe.com", "jotform",
                     "manychat", "mumlifebalance.ch", "wordpress", "elementor"]
BUSINESS_BETREFF = ["neuer verkauf", "new sale", "new order", "neue bestellung", "anmeldung eingegangen",
                    "kontaktformular", "anfrage", "kooperation", "zusammenarbeit", "auszahlung", "payout"]
TECHNIK = ["github", "vercel", "blotato", "supabase", "railway", "apify", "anthropic", "openai",
           "claude.com", "canva", "notion", "google search console", "cloudflare", "hostpoint",
           "cyon", "infomaniak", "plesk", "cpanel"]
TECHNIK_FEHLER = ["error", "fehler", "failed", "fehlgeschlagen", "limit", "paused", "pausiert",
                  "action required", "handlungsbedarf", "suspended", "gesperrt", "deprecat",
                  "abgelaufen", "expired", "laeuft ab", "speicher voll", "quota", "ausfall", "down"]
REZEPTE = ["eatyourway", "mybodyadvice", "rezept", "fooby", "bettybossi", "betty bossi", "kochen"]
GARTEN = ["garten", "samen", "saatgut", "wurzelwerk", "sativa", "bioterra", "permakultur",
          "kraut & rueben", "kraut und rueben", "pflanzen"]
PRIVAT = ["families-noreply", "family link", "schule", "gemeinde", "arzt", "praxis", "termin",
          "post.ch", "dhl", "planzer", "dpd", "ricardo", "tutti", "krankenkasse", "swica", "css.ch",
          "helsana", "sanitas", "visana", "verein"]
PAKETE = ["sendungsstatus", "zugestellt", "unterwegs:", "versandbereit", "heute da:", "paket wartet",
          "bestellung versendet", "bestellung wurde versandt", "lieferung am", "status deiner bestellung",
          "ihre lieferung", "shipped", "out for delivery", "delivered"]
NEWSLETTER_ABSENDER = ["swisslos", "polittrends", "presseshop", "ifttt", "intesis", "galaxus", "fleurop",
                       "just-eat", "goldkindchen", "comparis", "letsfamily", "swiss life", "odec"]
BUSINESS_WICHTIG = ["alert", "connection lost", "verbindung", "vat", "mwst", "tax", "steuer"]
WERBUNG = ["newsletter", "news@", "noreply", "no-reply", "marketing", "promo", "angebot", "rabatt",
           "sale", "% ", "gratis", "webinar", "masterclass", "einladung zum", "nur heute",
           "letzte chance", "black friday"]


def einordnen(absender, betreff, liste):
    """Gibt (schluessel, verschieben?) zurück."""
    a = umschrift(absender)
    b = umschrift(betreff)
    ab = a + " " + b

    # Von Patricia am 01.10.2026 als Betrug bestätigt (sie hat kein Apple-Gerät).
    if hat(ab, ["waiiet", "spende zu erhalten", "serafi", "rueckerstattung wartet auf bestaetigung",
                "krypto meisterschaft", "bitcoin helix"])             or ("apple" in a and "zahlungsmethode" in b)             or re.search("[฀-๿]", absender):
        return "betrug", True
    if "doterra" in ab:
        if hat(b, ["bestell", "order", "lrp", "versand", "shipped", "lieferung", "konto", "account",
                   "rechnung", "invoice", "zahlung"]):
            return "doterra", False
        return "newsletter", True
    if re.search(r"hat gerade .* erstellt", b):
        return "community", True
    if hat(b, PAKETE) and not hat(b, ["zoll", "zahlung"]):
        return "pakete", True
    if hat(b, SICHERHEIT) and not liste:
        return "sicherheit", False
    if hat(a, BUSINESS_ABSENDER) or hat(b, BUSINESS_BETREFF):
        if liste and not hat(b, BUSINESS_BETREFF + BUSINESS_WICHTIG):
            return "newsletter", True
        if hat(b, FINANZEN) and not hat(a, ["thrivecart"]):
            return "finanzen", True
        return "business", False
    if hat(a, TECHNIK):
        if hat(b, TECHNIK_FEHLER):
            return "technik-fehler", False
        if hat(b, FINANZEN):
            return "finanzen", True
        return "technik", True
    if hat(b, FINANZEN) or hat(a, ["paypal", "twint", "postfinance", "raiffeisen", "ubs.com", "zkb"]):
        if liste and not hat(b, FINANZEN):
            return "newsletter", True
        return "finanzen", True
    if hat(a, NEWSLETTER_ABSENDER) or hat(b, ["jackpot", "befragung", "neuigkeiten:"]):
        return "newsletter", True
    if hat(a, REZEPTE):
        return "rezepte", True
    if hat(a, GARTEN):
        return "garten", True
    if hat(ab, PRIVAT) and not liste:
        return "privat", False
    if liste or hat(a, WERBUNG) or hat(b, WERBUNG[6:]):
        return "newsletter", True
    return "mensch", False


def dekodiert(wert):
    if not wert:
        return ""
    try:
        return str(make_header(decode_header(wert)))
    except Exception:
        return wert


def lade_env():
    pfad = HIER / ".env"
    if not pfad.exists():
        sys.exit(f"Fehlt: {pfad} — Vorlage siehe README.md")
    werte = {}
    for zeile in pfad.read_text(encoding="utf-8").splitlines():
        zeile = zeile.strip()
        if zeile and not zeile.startswith("#") and "=" in zeile:
            k, v = zeile.split("=", 1)
            werte[k.strip()] = v.strip().strip('"').strip("'")
    return werte


def utf7(name):
    """IMAP-Ordnernamen in modifiziertes UTF-7 (RFC 3501) umwandeln."""
    aus, puffer = [], []

    def leeren():
        if puffer:
            import base64
            roh = "".join(puffer).encode("utf-16-be")
            aus.append("&" + base64.b64encode(roh).decode().rstrip("=").replace("/", ",") + "-")
            puffer.clear()

    for z in name:
        if 0x20 <= ord(z) <= 0x7e:
            leeren()
            aus.append("&-" if z == "&" else z)
        else:
            puffer.append(z)
    leeren()
    return "".join(aus)


def namensraum(imap):
    """Präfix und Trennzeichen der eigenen Ordner (z.B. 'INBOX.' und '.')."""
    praefix, trenner = "", "/"
    try:
        typ, daten = imap.namespace()
        if typ == "OK" and daten and daten[0]:
            m = re.search(rb'\(\("([^"]*)" (?:"(.)"|NIL)\)', daten[0])
            if m:
                praefix = m.group(1).decode()
                trenner = (m.group(2) or b"/").decode()
    except Exception:
        pass
    if trenner == "/" or not praefix:
        typ, daten = imap.list('""', '""')
        if typ == "OK" and daten and daten[0]:
            m = re.search(rb'\) "(.)" ', daten[0])
            if m:
                trenner = m.group(1).decode()
    return praefix, trenner


def ordnername(roh, praefix, trenner):
    return praefix + roh.replace("/", trenner)


def sicherstellen(imap, ordner):
    q = f'"{utf7(ordner)}"'
    typ, daten = imap.list('""', q)
    if typ == "OK" and daten and daten[0]:
        return  # existiert schon — kein CREATE, sonst zählt der Server Fehler und bricht ab
    typ, daten = imap.create(q)
    if typ != "OK":
        raise SystemExit(f"Ordner {ordner} lässt sich nicht anlegen: {daten}")
    imap.subscribe(q)


def verschieben(imap, uids, ziel, kann_move):
    menge = ",".join(uids)
    ziel_q = f'"{utf7(ziel)}"'
    if kann_move:
        typ, _ = imap.uid("MOVE", menge, ziel_q)
        return typ == "OK"
    typ, _ = imap.uid("COPY", menge, ziel_q)
    if typ != "OK":
        return False
    imap.uid("STORE", menge, "+FLAGS.SILENT", r"(\Deleted)")
    if "UIDPLUS" in imap.capabilities:
        imap.uid("EXPUNGE", menge)
    else:
        # ohne UIDPLUS würde EXPUNGE auch fremde \Deleted-Mails entfernen
        print("    ⚠️ Server kann kein MOVE und kein UID EXPUNGE — Kopie liegt im Ordner,"
              " Original ist nur als gelöscht markiert.")
    return True


def postfach(schluessel, env, los, alle):
    k = KONTEN[schluessel]
    user, pw = env.get(k["user"]), env.get(k["pass"])
    if not user or not pw:
        print(f"\n— {k['name']}: Zugangsdaten fehlen in .env ({k['user']}/{k['pass']}), übersprungen.")
        return None
    host = env.get(schluessel.upper() + "_HOST", k["host"])
    print(f"\n— {k['name']} ({host})")
    imap = imaplib.IMAP4_SSL(host, 993)
    try:
        imap.login(user, pw)
    except imaplib.IMAP4.error as e:
        print(f"  Anmeldung abgelehnt: {e}")
        return None
    # Viele Server nennen MOVE/UIDPLUS erst nach der Anmeldung (info@ am 01.10.2026).
    typ, cap = imap.capability()
    if typ == "OK" and cap and cap[0]:
        imap.capabilities = tuple(cap[0].decode().upper().split())

    imap.select("INBOX")
    typ, daten = imap.uid("SEARCH", None, "ALL" if alle else "UNSEEN")
    uids = daten[0].split() if typ == "OK" and daten and daten[0] else []
    print(f"  {len(uids)} {'Mails' if alle else 'ungelesene Mails'} im Posteingang")

    eintraege = []
    felder = "(FLAGS BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE LIST-UNSUBSCRIBE LIST-ID)])"
    heute = dt.datetime.now(dt.timezone.utc)
    for i in range(0, len(uids), 200):
        stueck = b",".join(uids[i:i + 200]).decode()
        typ, antwort = imap.uid("FETCH", stueck, felder)
        for teil in antwort:
            if not isinstance(teil, tuple):
                continue
            m = re.search(rb"UID (\d+)", teil[0])
            if not m:
                continue
            kopf = email.message_from_bytes(teil[1])
            name, adresse = email.utils.parseaddr(dekodiert(kopf.get("From", "")))
            betreff = dekodiert(kopf.get("Subject", "")).replace("\n", " ").strip()
            liste = bool(kopf.get("List-Unsubscribe") or kopf.get("List-Id"))
            gelesen = rb"\Seen" in teil[0]
            try:
                zeit = email.utils.parsedate_to_datetime(kopf.get("Date"))
                if zeit.tzinfo is None:
                    zeit = zeit.replace(tzinfo=dt.timezone.utc)
                datum = zeit.strftime("%d.%m.%Y")
                alter = (heute - zeit).days
            except Exception:
                datum, alter = "?", 999
            kat, weg = einordnen(f"{name} {adresse}", betreff, liste)
            # Gelesen = schon gesehen. Im Posteingang bleibt davon nur, was von einem
            # Menschen kommt und jünger als 14 Tage ist (vielleicht ist eine Antwort offen).
            if gelesen and not weg and not (kat == "mensch" and alter <= 14):
                kat, weg = "erledigt", True
            eintraege.append({"uid": m.group(1).decode(), "von": name or adresse, "adresse": adresse,
                              "betreff": betreff, "datum": datum, "kat": kat, "weg": weg})

    praefix, trenner = namensraum(imap)
    kann_move = "MOVE" in imap.capabilities
    for kat, roh in ORDNER.items():
        betroffen = [e["uid"] for e in eintraege if e["kat"] == kat]
        if not betroffen:
            continue
        eigen = k.get("ordner", {}).get(kat)
        if eigen:
            roh = eigen
        ziel = ordnername(roh, praefix, trenner)
        print(f"  {len(betroffen):>4} → {roh}")
        if los:
            if not eigen:
                sicherstellen(imap, ordnername("Sortiert", praefix, trenner))
                sicherstellen(imap, ziel)
            for j in range(0, len(betroffen), 100):
                if not verschieben(imap, betroffen[j:j + 100], ziel, kann_move):
                    print(f"    ⚠️ Verschieben nach {roh} fehlgeschlagen")
    for kat, titel in BLEIBT.items():
        n = sum(1 for e in eintraege if e["kat"] == kat)
        if n:
            print(f"  {n:>4} bleiben im Posteingang · {titel}")
    imap.logout()
    return {"name": k["name"], "eintraege": eintraege}


def bericht(ergebnisse, los):
    BERICHTE.mkdir(parents=True, exist_ok=True)
    heute = dt.date.today().isoformat()
    z = ["---", "tags: [misc, mail]", "---", "",
         f"# Mail-Sortierung {heute}{'' if los else ' (Probelauf, nichts verschoben)'}", ""]
    for erg in ergebnisse:
        e = erg["eintraege"]
        weg = sum(1 for x in e if x["weg"])
        z += [f"## {erg['name']}", "", f"{len(e)} Mails · {weg} in Ordner · {len(e) - weg} im Posteingang", ""]
        for kat, titel in BLEIBT.items():
            treffer = [x for x in e if x["kat"] == kat]
            if not treffer:
                continue
            z += [f"### {titel} ({len(treffer)})", ""]
            for x in treffer[:200]:
                z.append(f"- {x['datum']} · {x['von']} · {x['betreff'] or '(ohne Betreff)'}")
            if len(treffer) > 200:
                z.append(f"- … und {len(treffer) - 200} weitere")
            z.append("")
        absender = {}
        for x in e:
            if x["weg"]:
                absender.setdefault(x["kat"], {}).setdefault(x["adresse"], 0)
                absender[x["kat"]][x["adresse"]] += 1
        if absender:
            z += ["### Verschoben, nach Absender (zum Gegenprüfen)", ""]
            for kat, d in absender.items():
                top = sorted(d.items(), key=lambda t: -t[1])[:15]
                z.append(f"- **{ORDNER[kat]}**: " + ", ".join(f"{a} ({n})" for a, n in top))
            z.append("")
    pfad = BERICHTE / f"{heute}.md"
    pfad.write_text("\n".join(z), encoding="utf-8")
    print(f"\nBericht: {pfad.relative_to(WURZEL)}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--los", action="store_true", help="wirklich verschieben (sonst nur Probelauf)")
    p.add_argument("--nur", choices=list(KONTEN), help="nur ein Postfach")
    p.add_argument("--alle", action="store_true", help="auch gelesene Mails im Posteingang")
    a = p.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    env = lade_env()
    if not a.los:
        print("Probelauf — es wird nichts verschoben. Mit --los wird sortiert.")
    ergebnisse = []
    for s in ([a.nur] if a.nur else KONTEN):
        erg = postfach(s, env, a.los, a.alle)
        if erg:
            ergebnisse.append(erg)
    if ergebnisse:
        bericht(ergebnisse, a.los)


if __name__ == "__main__":
    main()
