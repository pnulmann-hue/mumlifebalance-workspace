"""Holt Belege aus den Postfaechern und legt sie benannt ab.

Zwei Wege, dieselbe Ablage:

    python scripts/finanzen/beleg-auspacken.py --postfaecher [--tage 45] [--seit JJJJ-MM-TT] [--trocken] [--melden]
    python scripts/finanzen/beleg-auspacken.py --gmail-liste <liste.json>
    python scripts/finanzen/beleg-auspacken.py <datei.txt> [<datei2.txt> ...]

**GMX und info@** gehen per IMAP, ohne Claude. **Gmail** geht ueber den Connector,
solange kein App-Passwort da ist (siehe unten), und dann auch per IMAP.

🚨 **Der Umweg ueber die Datei ist der ganze Trick beim Connector.** Eine Mail
mit zwei PDF-Anhaengen sind rund 215'000 Zeichen base64 — das passt in keinen
Kontext. Claude holt die Mail mit `messageFormat: RAW`; die Antwort ist zu gross
und wird vom Werkzeug **als Datei** abgelegt. Genau die liest dieses Skript.
🚨 **Das gilt nur fuer grosse Mails** (ab rund 100 KB). Eine kleine Mail kaeme
inline in den Kontext und liesse sich nicht weiterreichen. Fuer die holt Claude
`PLAIN_TEXT` und legt die Antwort als JSON ab; daraus wird eine `.txt`, die sich
ausdruecklich nicht Original nennt. `--gmail-liste` sagt je Mail, welcher Weg gilt.

🚨 **Die Stripe-Links in der Mail helfen nicht.** „Download invoice" und
„Download receipt" verfallen nach einigen Wochen — geprueft am 24.09.2026 an
einem Juni-Beleg: `HTTP 400 · This URL has expired`. Der Anhang verfaellt nicht.

🚨 **Nichts wird veraendert.** Belege muessen im Original aufbewahrt werden;
umbenannt wird die Datei, nie ihr Inhalt. Haengt kein PDF an, wird die
**Originalmail** als `.eml` abgelegt.

🚨 **In den Postfaechern liegt alles durcheinander** — Lohnabrechnung, Arzt,
Netflix und Geschaeftliches. Deshalb wird nur abgelegt, was als geschaeftlich
bekannt ist. Was nach Beleg aussieht und unbekannt ist, wird NICHT abgelegt,
sondern kommt mit Absender und Betreff auf `_zu-pruefen.json`, bis Patricia
entschieden hat. Die Entscheide stehen in `context/finanzen/belege-regeln.json`
(gitignored, Repo ist oeffentlich).

🚨 **Nie als gelesen markieren, nie verschieben, nie loeschen.** Jeder Ordner
wird `readonly` geoeffnet, gelesen wird nur mit `BODY.PEEK`.
"""

import argparse
import base64
import datetime as dt
import email
import email.policy
import email.utils
import html as html_mod
import imaplib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
BELEGE = ROOT / "context" / "finanzen" / "2026" / "belege"
REGELN = ROOT / "context" / "finanzen" / "belege-regeln.json"
AUSGEPACKT = BELEGE / "_ausgepackt.json"
GESEHEN = BELEGE / "_gesehen.json"
ZU_PRUEFEN = BELEGE / "_zu-pruefen.json"

# Wortlisten und Zugang gehoeren dem Mail-Sortierer, nicht einer zweiten Kopie hier.
_spec = importlib.util.spec_from_file_location(
    "sortieren", ROOT / "scripts" / "mail-sortieren" / "sortieren.py")
sortieren = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sortieren)
umschrift, hat, dekodiert = sortieren.umschrift, sortieren.hat, sortieren.dekodiert

BELEGWORTE = sortieren.FINANZEN + ["zahlungsbeleg", "your receipt", "ads invoice"]
KEIN_BELEG = ["fehlgeschlagen", "failed", "mahnung", "zahlungserinnerung", "autorisiert",
              "keine zahlungsbestaetigung", "upcoming", "kuendigung"]

# Absender-Baustein -> kurzer Anbietername fuer den Dateinamen.
# 🚨 Nur der Absender zaehlt, nie der Betreff: sonst macht „Rechnung fuer deinen
# Canva-Kurs" einer Kundin aus der Mail einen Canva-Beleg.
ANBIETER = [
    ("anthropic", "anthropic"),
    ("railway", "railway"),
    ("supabase", "supabase"),
    ("manychat", "manychat"),
    ("tm.openai.com", "openai-ads"),
    ("openai", "openai"),
    ("canva", "canva"),
    ("vercel", "vercel"),
    ("apify", "apify"),
    ("vimeo", "vimeo"),
    ("padlet", "padlet"),
]
# Was in einer PayPal- oder Google-Play-Mail als Artikel oder Empfaenger steht.
ARTIKEL = [
    ("meta verified", "meta-verified"),
    ("microsoft", "microsoft"),
    ("canva", "canva"),
    ("anthropic", "anthropic"),
    ("vimeo", "vimeo"),
]

# 🚨 Der Zwischenraum in der Zahl ist kein Schoenheitsfehler. Aus dem PDF kommt
# „Amount paid $37 .31" — mit Leerzeichen vor dem Punkt, weil die Zahl dort aus
# zwei Textstuecken gesetzt ist. Gefunden am 24.09.2026 an einem Supabase-Beleg.
ZAHL = r"([\d',]+\s*\.\s*\d{2})"

# Bewusst eng: „Amount paid" und „$X paid on" belegen eine Zahlung. Ein „Total"
# allein taete das nicht — auf einer Rechnung mit Gutschrift steht ein Total,
# das nie geflossen ist.
BETRAG = [
    re.compile(r"([A-Z]{0,3}\$|CHF|EUR|USD)\s?" + ZAHL + r"\s+paid on", re.I),
    re.compile(r"Amount paid\s*([A-Z]{0,3}\$|CHF|EUR|USD)?\s?" + ZAHL, re.I),
]
WAEHRUNG = {"$": "USD", "US$": "USD", "CA$": "CAD", "USD": "USD",
            "CHF": "CHF", "EUR": "EUR", "€": "EUR"}

_W = r"(US\$|\$|CHF|EUR|USD|€)"
_Z = r"(\d[\d']*[.,]\d{2})"
# Im Mailtext: nur Stellen, die den bezahlten Gesamtbetrag nennen. `\bTotal`, weil
# in ManyChat-Rechnungen „Subtotal $25.00" davor steht und die Steuer fehlen wuerde.
TEXT_BETRAG = [
    # PayPal schreibt je nach Waehrung „13.95 CHF" oder „€91.23 EUR".
    re.compile(r"Sie haben\s+[€$]?" + _Z + r"\s*(CHF|EUR|USD)\s+an\s"),
    re.compile(r"(?:Abrechnungsbetrag|Rechnungsbetrag|Gesamtbetrag|Zahlungsbetrag|Gesamt|\bSumme|\bTotal|Amount paid)\s*:?\s*"
               + _W + r"\s?" + _Z, re.I),
    re.compile(r"(?:Abrechnungsbetrag|Rechnungsbetrag|Gesamtbetrag|Zahlungsbetrag|Gesamt|\bSumme|\bTotal|Amount paid)\s*:?\s*"
               + _Z + r"\s?" + _W, re.I),
    re.compile(r"invoice\s+\S+\s+for\s+" + _Z + r"\s*" + _W, re.I),
]


def zahl_aus(roh):
    roh = re.sub(r"[\s']", "", roh)
    return float(roh.replace(",", "."))


def betrag_aus_text(text):
    for muster in TEXT_BETRAG:
        m = muster.search(text)
        if m:
            a, b = m.group(1), m.group(2)
            zahl, whr = (a, b) if a[0].isdigit() else (b, a)
            return zahl_aus(zahl), WAEHRUNG.get(whr.upper(), whr.upper())
    return None, None


def betrag_aus_pdf(pfad):
    try:
        import pypdf
    except ImportError:
        return None, None
    try:
        r = pypdf.PdfReader(str(pfad))
        text = "\n".join(p.extract_text() or "" for p in r.pages)
    except Exception:
        return None, None
    for muster in BETRAG:
        m = muster.search(text)
        if m:
            roh, zahl = m.group(1) or "$", m.group(2)
            return (float(re.sub(r"[\s,']", "", zahl)),
                    WAEHRUNG.get(roh.upper().replace("US$", "$"), "USD"))
    return None, None


def lies_json(pfad, leer):
    try:
        return json.loads(pfad.read_text(encoding="utf-8"))
    except Exception:
        return leer


def regeln():
    d = lies_json(REGELN, {})
    return ([umschrift(w) for w in d.get("privat", [])],
            {umschrift(k): v for k, v in d.get("geschaeftlich", {}).items()})


def adresse(von):
    return email.utils.parseaddr(von)[1].lower()


def vorpruefen(von, betreff):
    """Nur aus Absender und Betreff: holen · pruefen · privat · None (kein Beleg)."""
    a, b = umschrift(von), umschrift(betreff)
    adr = adresse(von)
    privat, eigene = regeln()
    if hat(a + " " + b, privat):
        return "privat"
    if adr.endswith(("@paypal.ch", "@paypal.com")):
        return "holen" if b.startswith("beleg fuer") else None
    if adr == "googleplay-noreply@google.com":
        return "holen" if "beleg" in b else None
    if adr.endswith(("business-updates.facebook.com", "facebookmail.com")):
        return "holen" if "zahlungsbeleg" in b else None
    # „Tessa S hat gerade Kurs Rechnungen erstellt" ist eine Kurs-Plattform, kein Beleg.
    if not hat(b, BELEGWORTE) or hat(b, KEIN_BELEG) or re.search(r"hat gerade .* erstellt", b):
        return None
    # Eigene Rechnungen und Verkaeufe sind Einnahmen, und die kommen aus ThriveCart.
    if "thrivecart" in a or "mumlifebalance" in adr or "mum life balance" in b:
        return None
    if hat(a, [k for k, _ in ANBIETER]) or hat(a, list(eigene)):
        return "holen"
    return "pruefen"


def artikel_zu(text):
    t = umschrift(text)
    _, eigene = regeln()
    for wort, name in ARTIKEL + list(eigene.items()):
        if wort in t:
            return name
    return None


def einordnen(von, betreff, text):
    """Mit dem Mailtext: wer ist es, was wurde bezahlt, wird es gebucht?"""
    a = umschrift(von)
    adr = adresse(von)
    betrag, whr = betrag_aus_text(text)
    roh = {"anbieter": None, "betrag": betrag, "waehrung": whr, "form": None}
    _, eigene = regeln()

    if adr.endswith(("@paypal.ch", "@paypal.com")):
        # „Sie haben 13.95 CHF an Google Payment Corpo... gezahlt ... Beschreibung
        # Einzelpreis Menge Betrag Meta Verified (Insta... 13.95 CHF" — der Artikel
        # sagt, wofuer. Ohne „gezahlt" ist es Rueckzahlung oder Hinweis, kein Beleg.
        # Die zweite Bauart heisst „Beleg fuer Ihre PayPal-Zahlung" und nennt den
        # Empfaenger als „Zahlung an NAME adresse@domain".
        m = (re.search(r"Sie haben\s+\S+\s+\S+\s+an\s+(.+?)\s+gezahlt", text)
             or re.search(r"Zahlung an\s+(.+?)\s+\S+@\S+", text))
        if not m:
            return None
        art = re.search(r"Menge\s+Betrag\s+(.+?)\s+[€$]?\d", text)
        roh["anbieter"] = artikel_zu(m.group(1) + " " + (art.group(1) if art else ""))
        roh["form"] = "PayPal-Beleg"
        roh["was"] = (m.group(1) + (" · " + art.group(1) if art else ""))[:80]
        return roh

    if adr == "googleplay-noreply@google.com":
        roh["anbieter"] = artikel_zu(text[:900])
        roh["form"] = "Google-Play-Beleg"
        art = re.search(r"Artikel Preis\s+(.+?)\s+CHF", text)
        roh["was"] = (art.group(1) if art else "Google Play")[:60]
        return roh

    if adr.endswith(("business-updates.facebook.com", "facebookmail.com")):
        # 🚨 Die Mail sagt selbst „Das ist keine Rechnung". Sie belegt die Zahlung,
        # der Betrag gehoert aber zum Werbekonto — sonst stuenden die Ausgaben doppelt
        # da. Die Rechnung selbst bleibt Handarbeit im Business Manager.
        roh.update(anbieter="meta", nur_beleg=True, form="Meta-Zahlungsbeleg")
        z = re.search(r"Zeitraum\s*(\d{2})\.(\d{2})\.(\d{4})", text)
        if z:
            roh["bezug"] = "%s-%s" % (z.group(3), z.group(2))
        return roh

    for baustein, name in ANBIETER + list(eigene.items()):
        if baustein in a:
            roh["anbieter"] = name
            return roh
    return roh


def text_der_mail(msg):
    teil = msg.get_body(preferencelist=("plain", "html"))
    if not teil:
        return ""
    try:
        inhalt = teil.get_content()
    except Exception:
        return ""
    if teil.get_content_type() == "text/html":
        inhalt = re.sub(r"(?is)<(script|style).*?</\1>", " ", inhalt)
        inhalt = re.sub(r"<[^>]+>", " ", inhalt)
        inhalt = html_mod.unescape(inhalt)
    return re.sub(r"\s+", " ", inhalt)


def datum_von(wert):
    try:
        return email.utils.parsedate_to_datetime(wert).date().isoformat()
    except Exception:
        return "0000-00-00"


def freier_name(name, inhalt):
    """Gleicher Name und gleicher Inhalt: schon da. Gleicher Name, anderer Inhalt: -2."""
    ziel = BELEGE / name
    n = 1
    while ziel.exists():
        if ziel.read_bytes() == inhalt:
            return ziel, True
        n += 1
        ziel = BELEGE / re.sub(r"(\.\w+)$", r"-%d\1" % n, name)
    return ziel, False


def ablegen(mime, mail_id, kanal, trocken=False):
    """Eine ganze Mail. Gibt (status, eintraege, kopf) zurueck."""
    msg = email.message_from_bytes(mime, policy=email.policy.default)
    betreff = str(msg.get("Subject") or "").replace("\n", " ")
    von = str(msg.get("From") or "")
    tag = datum_von(msg.get("Date"))
    kopf = {"von": von[:80], "betreff": betreff[:100], "datum": tag}

    vor = vorpruefen(von, betreff)
    if vor != "holen":
        return vor, [], kopf
    info = einordnen(von, betreff, text_der_mail(msg))
    if info is None:
        return None, [], kopf
    if not info["anbieter"]:
        kopf["was"] = ("%s %s %s" % (info.get("was", ""), info["betrag"] or "", info["waehrung"] or "")).strip()
        return "pruefen", [], kopf
    name = info["anbieter"]
    if trocken:
        kopf.update(anbieter=name, betrag=info["betrag"], waehrung=info["waehrung"])
        return "holen", [], kopf

    gemeinsam = {"datum": tag, "anbieter": name, "betreff": betreff, "mail_id": mail_id,
                 "kanal": kanal}
    for feld in ("nur_beleg", "bezug", "was"):
        if info.get(feld):
            gemeinsam[feld] = info[feld]

    BELEGE.mkdir(parents=True, exist_ok=True)
    raus = []
    for teil in msg.walk():
        datei = teil.get_filename()
        if not datei or not datei.lower().endswith(".pdf"):
            continue
        inhalt = teil.get_payload(decode=True)
        if not inhalt:
            continue
        sauber = re.sub(r"[^A-Za-z0-9._-]", "-", datei)
        ziel, _ = freier_name("%s_%s_%s" % (tag, name, sauber), inhalt)
        ziel.write_bytes(inhalt)
        betrag, whr = betrag_aus_pdf(ziel)
        raus.append(dict(gemeinsam, datei=ziel.name, bytes=len(inhalt), betrag=betrag,
                         waehrung=whr, form="PDF-Anhang"))
    if raus:
        # Rechnung ohne „Amount paid" und Quittung gehoeren zusammen; nur wenn gar
        # kein PDF den Betrag nennt, kommt er aus dem Mailtext.
        if not any(r["betrag"] for r in raus) and info["betrag"]:
            raus[0].update(betrag=info["betrag"], waehrung=info["waehrung"])
    else:
        # Siehe Kopf: ohne PDF-Anhang IST die Mail der Beleg.
        zusatz = "paypal_" if info.get("form") == "PayPal-Beleg" else ""
        ziel, _ = freier_name("%s_%s_%smail.eml" % (tag, name, zusatz), mime)
        ziel.write_bytes(mime)
        raus.append(dict(gemeinsam, datei=ziel.name, bytes=len(mime), betrag=info["betrag"],
                         waehrung=info["waehrung"],
                         form=info.get("form") or "Originalmail (kein PDF-Anhang)"))
    return "holen", raus, kopf


def merken(neu, gesehen, schluessel, status, kopf, eintraege=None):
    gesehen[schluessel] = {"status": status or "kein-beleg", "datum": kopf.get("datum"),
                           "am": dt.date.today().isoformat()}
    if eintraege:
        neu.extend(eintraege)
    if status == "pruefen":
        liste = lies_json(ZU_PRUEFEN, [])
        if not any(x.get("id") == schluessel for x in liste):
            liste.append({"id": schluessel, "datum": kopf.get("datum"), "von": kopf.get("von"),
                          "betreff": kopf.get("betreff"), "was": kopf.get("was", "")})
            BELEGE.mkdir(parents=True, exist_ok=True)
            ZU_PRUEFEN.write_text(json.dumps(liste, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    return False


def speichern(neu, gesehen):
    BELEGE.mkdir(parents=True, exist_ok=True)
    # 🚨 Anhaengen, nie ersetzen. Bis zum 04.11.2026 schrieb dieses Skript die Liste bei
    # jedem Lauf neu — der naechste Einzelbeleg haette alles davor weggeworfen, auch die
    # von Hand eingetragene Kreditkartenabrechnung.
    alle = lies_json(AUSGEPACKT, [])
    da = {(e["datei"], e["datum"], e.get("betrag")) for e in alle}
    dazu = [e for e in neu if (e["datei"], e["datum"], e.get("betrag")) not in da]
    if dazu:
        alle.extend(dazu)
        alle.sort(key=lambda x: (x["datum"], x["datei"]))
        AUSGEPACKT.write_text(json.dumps(alle, ensure_ascii=False, indent=2), encoding="utf-8")
    GESEHEN.write_text(json.dumps(gesehen, ensure_ascii=False, indent=1), encoding="utf-8")
    return dazu


def zeigen(alle):
    for a in sorted(alle, key=lambda x: (x["datum"], x["datei"])):
        print("  %s  %-13s %-50s %8s %s%s"
              % (a["datum"], a["anbieter"], a["datei"][:50],
                 ("%.2f" % a["betrag"]) if a.get("betrag") else "—",
                 a.get("waehrung") or "", "  (nur Beleg)" if a.get("nur_beleg") else ""))


# ---------- die Postfaecher per IMAP ----------

UEBERSPRINGEN = re.compile(r"(?i)spam|junk|entw|draft|gesendet|sent|vorlage|template|outbox")


def konten(env):
    k = {s: dict(v) for s, v in sortieren.KONTEN.items()}
    # 🚨 Noch nie gelaufen, solange GMAIL_USER und GMAIL_PASS (App-Passwort) fehlen.
    if env.get("GMAIL_USER") and env.get("GMAIL_PASS"):
        k["gmail"] = {"name": "Gmail", "host": "imap.gmail.com", "user": "GMAIL_USER",
                      "pass": "GMAIL_PASS", "nur_ordner": ['"[Gmail]/All Mail"', '"[Gmail]/Alle Nachrichten"']}
    return k


def ordner_von(imap, konto):
    if konto.get("nur_ordner"):
        return konto["nur_ordner"]
    typ, zeilen = imap.list()
    raus = []
    for z in zeilen if typ == "OK" else []:
        if not z or b"\\Noselect" in z:
            continue
        m = re.search(rb'"([^"]+)"\s*$', z) or re.search(rb"\s(\S+)$", z)
        name = m.group(1).decode() if m else ""
        if name and not UEBERSPRINGEN.search(name):
            raus.append('"%s"' % name)
    return raus


def postfach(schluessel, konto, env, seit, gesehen, neu, trocken):
    """Gibt (Zahl neuer Pruefzeilen, Fehlertext oder None) zurueck."""
    host = env.get(schluessel.upper() + "_HOST", konto["host"])
    pruef = 0
    try:
        imap = imaplib.IMAP4_SSL(host, 993)
        imap.login(env[konto["user"]], env[konto["pass"]])
    except (KeyError, OSError, imaplib.IMAP4.error) as e:
        return 0, "%s: Anmeldung gescheitert (%s)" % (konto["name"], type(e).__name__)
    felder = "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE MESSAGE-ID)])"
    gezaehlt = 0
    for ordner in ordner_von(imap, konto):
        typ, _ = imap.select(ordner, readonly=True)   # siehe Kopf: nie schreibend
        if typ != "OK":
            continue
        typ, d = imap.uid("SEARCH", None, "SINCE", seit.strftime("%d-%b-%Y"))
        uids = d[0].split() if typ == "OK" and d and d[0] else []
        for i in range(0, len(uids), 200):
            typ, antwort = imap.uid("FETCH", b",".join(uids[i:i + 200]).decode(), felder)
            for t in antwort if typ == "OK" else []:
                if not isinstance(t, tuple):
                    continue
                uid = re.search(rb"UID (\d+)", t[0])
                k = email.message_from_bytes(t[1])
                von = dekodiert(k.get("From", ""))
                betreff = dekodiert(k.get("Subject", "")).replace("\n", " ")
                schl = (k.get("Message-ID") or "").strip() or "%s/%s/%s" % (schluessel, ordner, uid.group(1).decode())
                if schl in gesehen:
                    continue
                vor = vorpruefen(von, betreff)
                if vor in (None, "privat"):
                    continue          # nicht merken, Regeln duerfen sich aendern
                if vor != "holen":
                    kopf = {"von": von[:80], "betreff": betreff[:100],
                            "datum": datum_von(k.get("Date"))}
                    if trocken:
                        print("  [%s] %s | %s | %s" % (vor, konto["name"], von[:40], betreff[:60]))
                    else:
                        pruef += merken(neu, gesehen, schl, vor, kopf)
                    continue
                typ2, roh = imap.uid("FETCH", uid.group(1).decode(), "(BODY.PEEK[])")
                teil = [x for x in roh if isinstance(x, tuple)] if typ2 == "OK" else []
                if not teil:
                    continue
                status, eintraege, kopf = ablegen(teil[0][1], schl, schluessel, trocken)
                gezaehlt += 1
                if status == "privat":
                    continue
                if trocken:
                    print("  [%s] %s | %s | %s %s | %s" % (status, konto["name"], kopf.get("datum"),
                          kopf.get("anbieter", kopf.get("was", "")), kopf.get("betrag", ""), betreff[:50]))
                else:
                    pruef += merken(neu, gesehen, schl, status, kopf, eintraege)
    imap.logout()
    print("  %s: %d Belegmails gelesen" % (konto["name"], gezaehlt))
    return pruef, None


def melden(text):
    subprocess.run([sys.executable, str(ROOT / "scripts" / "telegram" / "senden.py"), "--text", text],
                   check=False)


def alle_postfaecher(a):
    env = sortieren.lade_env()
    seit = (dt.date.fromisoformat(a.seit) if a.seit else dt.date.today() - dt.timedelta(days=a.tage))
    gesehen = lies_json(GESEHEN, {})
    neu, fehler, pruef = [], [], 0
    for schluessel, konto in konten(env).items():
        p, f = postfach(schluessel, konto, env, seit, gesehen, neu, a.trocken)
        pruef += p
        if f:
            fehler.append(f)
    if a.trocken:
        print("Probelauf: nichts abgelegt.")
    else:
        dazu = speichern(neu, gesehen)
        zeigen(dazu)
        print("  %d neue Belegdateien · %d neu zu pruefen" % (len(dazu), pruef))
        if a.melden and (dazu or pruef):
            melden("🧾 Belege: %d neue Dateien%s" % (
                len(dazu), " · %d unbekannte Absender warten auf dein Urteil" % pruef if pruef else ""))
    for f in fehler:
        print("  ⚠️ " + f)
        if a.melden:
            melden("⚠️ Belege holen: " + f)
    return 1 if fehler else 0


# ---------- Gmail ueber den Connector ----------

GROSS_AB = 100_000   # darunter kaeme RAW inline in den Kontext, siehe Kopf


def gmail_liste(pfad):
    """Sagt zu einer Trefferliste aus search_threads, welche Mail wie zu holen ist."""
    gesehen = lies_json(GESEHEN, {})
    raw, text, pruef = [], [], 0
    neu = []
    for m in json.loads(Path(pfad).read_text(encoding="utf-8")):
        schl = m["id"]
        if schl in gesehen or "TRASH" in (m.get("labelIds") or []):
            continue
        kopf = {"von": m.get("sender", "")[:80], "betreff": m.get("subject", "")[:100],
                "datum": (m.get("date") or "")[:10]}
        vor = vorpruefen(m.get("sender", ""), m.get("subject", ""))
        if vor in (None, "privat"):
            continue
        if vor != "holen":
            pruef += merken(neu, gesehen, schl, vor, kopf)
            continue
        (raw if (m.get("sizeEstimate") or 0) >= GROSS_AB else text).append(schl)
    speichern([], gesehen)
    print(json.dumps({"raw": raw, "plain_text": text, "neu_zu_pruefen": pruef}))


def entpacke(rohdatei):
    """Eine gespeicherte Connector-Antwort: RAW (Original) oder PLAIN_TEXT (kleine Mail)."""
    try:
        d = json.loads(rohdatei.read_text(encoding="utf-8"))
    except Exception:
        return None, [], None
    schl = d.get("id")
    if d.get("raw"):
        roh = d["raw"]
        mime = base64.urlsafe_b64decode(roh + "=" * (-len(roh) % 4))
        status, eintraege, kopf = ablegen(mime, schl, "gmail")
        return status, eintraege, kopf
    if d.get("plaintextBody"):
        von, betreff = d.get("sender", ""), d.get("subject", "")
        tag = (d.get("date") or "0000-00-00")[:10]
        kopf = {"von": von[:80], "betreff": betreff[:100], "datum": tag}
        vor = vorpruefen(von, betreff)
        if vor != "holen":
            return vor, [], kopf
        # Der Connector setzt Tabellen als Markdown: „| Total | |---| | ### $16.22 |".
        text = re.sub(r"\s+", " ", re.sub(r"[|#]|-{3,}", " ", d["plaintextBody"]))
        info = einordnen(von, betreff, text)
        if info is None:
            return None, [], kopf
        if not info["anbieter"]:
            kopf["was"] = info.get("was", "")
            return "pruefen", [], kopf
        name = info["anbieter"]
        inhalt = ("Von: %s\nDatum: %s\nBetreff: %s\nGmail-Kennung: %s\n"
                  "Abschrift ueber den Connector, nicht die Originalmail. Original in Gmail.\n\n%s"
                  % (von, d.get("date"), betreff, schl, d["plaintextBody"])).encode("utf-8")
        BELEGE.mkdir(parents=True, exist_ok=True)
        ziel, _ = freier_name("%s_%s_mailtext.txt" % (tag, name), inhalt)
        ziel.write_bytes(inhalt)
        eintrag = {"datei": ziel.name, "datum": tag, "anbieter": name, "bytes": len(inhalt),
                   "betrag": info["betrag"], "waehrung": info["waehrung"], "betreff": betreff,
                   "mail_id": schl, "kanal": "gmail", "form": info.get("form") or "Mailtext (Abschrift)"}
        if info.get("was"):
            eintrag["was"] = info["was"]
        return "holen", [eintrag], kopf
    return None, [], None


def dateien(pfade):
    gesehen = lies_json(GESEHEN, {})
    neu, pruef = [], 0
    for e in pfade:
        for f in (sorted(e.glob("*.txt")) + sorted(e.glob("*.json"))) if e.is_dir() else [e]:
            status, eintraege, kopf = entpacke(f)
            if kopf is None:
                continue
            schl = json.loads(f.read_text(encoding="utf-8")).get("id")
            if status != "privat":
                pruef += merken(neu, gesehen, schl, status, kopf, eintraege)
    dazu = speichern(neu, gesehen)
    zeigen(dazu)
    print("\n  %d neue Belegdateien in %s · %d neu zu pruefen" % (len(dazu), BELEGE, pruef))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("dateien", nargs="*", type=Path, help="gespeicherte Connector-Antworten")
    p.add_argument("--postfaecher", action="store_true", help="GMX und info@ (und Gmail mit App-Passwort)")
    p.add_argument("--gmail-liste", help="JSON-Liste aus search_threads: id, sender, subject, date, sizeEstimate, labelIds")
    p.add_argument("--tage", type=int, default=45)
    p.add_argument("--seit", help="JJJJ-MM-TT, statt --tage")
    p.add_argument("--trocken", action="store_true", help="nur anzeigen, nichts ablegen")
    p.add_argument("--melden", action="store_true", help="Neues und Fehler per Telegram")
    a = p.parse_args()
    if a.postfaecher:
        sys.exit(alle_postfaecher(a))
    if a.gmail_liste:
        return gmail_liste(a.gmail_liste)
    if a.dateien:
        return dateien(a.dateien)
    p.print_help()


if __name__ == "__main__":
    main()
