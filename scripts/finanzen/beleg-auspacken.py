"""Packt die Belege aus Gmail-RAW-Antworten aus und legt sie benannt ab.

🚨 **Der Umweg ueber die Datei ist der ganze Trick.** Eine Mail mit zwei
PDF-Anhaengen sind rund 215'000 Zeichen base64 — das passt in keinen Kontext.
Claude holt die Mail mit `messageFormat: RAW`; die Antwort ist zu gross und
wird vom Werkzeug **als Datei** abgelegt. Genau die liest dieses Skript. Der
Beleg kommt im Original heraus, ohne je durch den Kontext zu laufen.

🚨 **Die Stripe-Links in der Mail helfen nicht.** „Download invoice" und
„Download receipt" verfallen nach einigen Wochen — geprueft am 24.09.2026 an
einem Juni-Beleg: `HTTP 400 · This URL has expired`. Wer sich darauf verlaesst,
merkt es erst, wenn er den Beleg braucht. Der Anhang verfaellt nicht.

🚨 **Nichts wird veraendert.** Belege muessen im Original aufbewahrt werden;
umbenannt wird die Datei, nie ihr Inhalt. Haengt kein PDF an, wird die
**Originalmail** als `.eml` abgelegt — ein selbstgebautes PDF daraus waere kein
Original mehr, sondern eine Abschrift.

🚨 **Der Betrag wird aus dem PDF gelesen, nicht aus dem Mailtext.** Im PDF
stehen zusaetzlich MwSt-Nummer und Rechnungsadresse — das ist es, was eine
Rechnung zur Rechnung macht.

    python scripts/finanzen/beleg-auspacken.py <ordner-mit-raw-dateien>
    python scripts/finanzen/beleg-auspacken.py <datei.txt> [<datei2.txt> ...]
"""

import base64
import email
import email.policy
import email.utils
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
BELEGE = ROOT / "context" / "finanzen" / "2026" / "belege"

# Absender-Baustein -> kurzer Anbietername fuer den Dateinamen.
ANBIETER = [
    ("anthropic", "anthropic"),
    ("railway", "railway"),
    ("supabase", "supabase"),
    ("manychat", "manychat"),
    ("openai", "openai"),
    ("canva", "canva"),
    ("vercel", "vercel"),
    ("apify", "apify"),
    ("thrivecart", "thrivecart"),
    ("paypal", "paypal"),
    ("microsoft", "microsoft"),
    ("vimeo", "vimeo"),
    ("padlet", "padlet"),
    ("telegram", "telegram"),
    ("meta platforms", "meta"),
    ("facebookmail", "meta"),
]

# 🚨 Der Zwischenraum in der Zahl ist kein Schoenheitsfehler. Aus dem PDF kommt
# „Amount paid $37 .31" — mit Leerzeichen vor dem Punkt, weil die Zahl dort aus
# zwei Textstuecken gesetzt ist. Ein Muster ohne den Zwischenraum findet den
# Betrag nicht, und ein fehlender Betrag sieht aus wie ein fehlender Beleg.
# Gefunden am 24.09.2026 an einem Supabase-Beleg.
ZAHL = r"([\d',]+\s*\.\s*\d{2})"

# Bewusst eng: „Amount paid" und „$X paid on" belegen eine Zahlung. Ein „Total"
# allein taete das nicht — auf einer Rechnung mit Gutschrift steht ein Total,
# das nie geflossen ist.
BETRAG = [
    re.compile(r"([A-Z]{0,3}\$|CHF|EUR|USD)\s?" + ZAHL + r"\s+paid on", re.I),
    re.compile(r"Amount paid\s*([A-Z]{0,3}\$|CHF|EUR|USD)?\s?" + ZAHL, re.I),
]
WAEHRUNG = {"$": "USD", "US$": "USD", "CA$": "CAD", "USD": "USD",
            "CHF": "CHF", "EUR": "EUR"}


def anbieter_aus(absender, betreff):
    text = (absender + " " + betreff).lower()
    for baustein, name in ANBIETER:
        if baustein in text:
            return name
    return "unbekannt"


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


def entpacke(rohdatei):
    try:
        d = json.loads(rohdatei.read_text(encoding="utf-8"))
    except Exception:
        return []          # keine Werkzeug-Antwort, sondern etwas anderes
    roh = d.get("raw")
    if not roh:
        return []

    mime = base64.urlsafe_b64decode(roh + "=" * (-len(roh) % 4))
    msg = email.message_from_bytes(mime, policy=email.policy.default)

    betreff = str(msg.get("Subject") or "")
    absender = str(msg.get("From") or "")
    try:
        tag = email.utils.parsedate_to_datetime(msg.get("Date")).date().isoformat()
    except Exception:
        tag = "0000-00-00"
    name = anbieter_aus(absender, betreff)

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
        ziel = BELEGE / ("%s_%s_%s" % (tag, name, sauber))
        ziel.write_bytes(inhalt)
        betrag, whr = betrag_aus_pdf(ziel)
        raus.append({"datei": ziel.name, "datum": tag, "anbieter": name,
                     "bytes": len(inhalt), "betrag": betrag, "waehrung": whr,
                     "betreff": betreff, "mail_id": d.get("id"),
                     "form": "PDF-Anhang"})

    if not raus:
        # Siehe Kopf: ohne PDF-Anhang IST die Mail der Beleg.
        ziel = BELEGE / ("%s_%s_mail.eml" % (tag, name))
        ziel.write_bytes(mime)
        raus.append({"datei": ziel.name, "datum": tag, "anbieter": name,
                     "bytes": len(mime), "betrag": None, "waehrung": None,
                     "betreff": betreff, "mail_id": d.get("id"),
                     "form": "Originalmail (kein PDF-Anhang)"})
    return raus


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    eingang = [Path(a) for a in sys.argv[1:]]
    dateien = []
    for e in eingang:
        dateien.extend(sorted(e.glob("*.txt")) if e.is_dir() else [e])

    alle = []
    for f in dateien:
        alle.extend(entpacke(f))

    alle.sort(key=lambda x: (x["datum"], x["datei"]))
    for a in alle:
        print("  %s  %-10s %-52s %8s %s"
              % (a["datum"], a["anbieter"], a["datei"][:52],
                 ("%.2f" % a["betrag"]) if a["betrag"] else "—",
                 a["waehrung"] or ""))
    ohne = [a for a in alle if a["form"] != "PDF-Anhang"]
    print()
    print("  %d Belege in %s" % (len(alle), BELEGE))
    if ohne:
        print("  %d davon als Originalmail, weil kein PDF anhing: %s"
              % (len(ohne), ", ".join(sorted({a["anbieter"] for a in ohne}))))

    if alle:
        (BELEGE / "_ausgepackt.json").write_text(
            json.dumps(alle, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
