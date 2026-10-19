# -*- coding: utf-8 -*-
"""
Baut die Nachkauf-Mails für „Easy KI für Networkerinnen" als fertige Mail-HTMLs.

Das Gerüst (Kopf, Farben, Fuss, Outlook-Tabellen, Umlaut-Wächter, Kopierseite)
kommt aus scripts/startklar/mails-bauen.py und wird importiert, nicht kopiert —
eine Stelle, an der das Mail-Design gepflegt wird.

  python scripts/ki-kurs/mails-bauen.py

Ausgabe: outputs/produkte/ki-kurs/mails/
  mail-00-willkommen.html · index.html (Kopierseite mit Kopier-Knöpfen)

Gehört in ActiveCampaign in die Automation 85 „KI Kurs" (derzeit inaktiv und
noch mit den sieben Startklar-Mails gefüllt, weil sie als Kopie entstanden ist).

🚨 Der Einladungslink steht in scripts/ki-kurs/.env, nicht hier. Wer ihn hat,
   kommt in die Gruppe der zahlenden Kundinnen — und das Repo ist öffentlich.
   Deshalb ist auch die Ausgabe gitignored.

🚨 KEIN Zugangslink zum Kurs in dieser Mail. Die Rechnung schickt ThriveCart in
   einer eigenen Mail, und den Kursbereich gibt es erst am 1. November.
"""
import importlib.util
import io
import os
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]

# --- Das Gerüst importieren, nicht kopieren -------------------------------
spec = importlib.util.spec_from_file_location(
    "sk", ROOT / "scripts" / "startklar" / "mails-bauen.py")
sk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sk)

absatz, kasten, liste, knopf = sk.absatz, sk.kasten, sk.liste, sk.knopf
h2, ps, gruss, merken = sk.h2, sk.ps, sk.gruss, sk.merken
PETROL, ORANGE, NACHT, CREME = sk.PETROL, sk.ORANGE, sk.NACHT, sk.CREME

ZIEL = ROOT / "outputs" / "produkte" / "ki-kurs" / "mails"

# --- Der Gruppenlink kommt aus der .env, nie aus dem Code -----------------
ENV = ROOT / "scripts" / "ki-kurs" / ".env"
GRUPPE = ""
if ENV.exists():
    for zeile in ENV.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*KI_TELEGRAM_GRUPPE\s*=\s*(\S+)", zeile)
        if m:
            GRUPPE = m.group(1)
GRUPPE = os.environ.get("KI_TELEGRAM_GRUPPE", GRUPPE)

if not GRUPPE:
    sys.exit("KI_TELEGRAM_GRUPPE fehlt.\n"
             "Trag den Einladungslink in scripts/ki-kurs/.env ein:\n"
             "  KI_TELEGRAM_GRUPPE=https://t.me/+...\n"
             "Die Datei ist gitignored, der Link gehoert nicht ins Repo.")

INSTAGRAM = "https://www.instagram.com/mumlifebalance_patricia_ulmann/"

# ============================================================================
#  DIE STRECKE
# ============================================================================

MAILS = [

# --------------------------------------------------------------------- Tag 0
{
 "datei": "mail-00-willkommen.html", "tag": 0, "warten": "sofort nach dem Kauf",
 "marke": "mumlifebalance · Easy KI",
 "betreff": "Du bist dabei — und das passiert als Nächstes",
 "betreff2": "Dein Platz im KI-Kurs steht",
 "wann": "sofort nach dem Kauf (Automation 85 „KI Kurs“)",
 "preheader": "Der Kurs startet am 1. November. Heute brauchst du nur einen Klick.",
 "h1": "Schön, dass du dabei bist!",
 "unterzeile": "Am Ende steht ein Arbeitsplatz, der weiss, wer du bist &mdash; "
               "und der dir Arbeit abnimmt, nicht deine Handschrift.",
 "notiz": """
🚨 KEIN Zugangslink in dieser Mail. ThriveCart schickt eine eigene Mail, und die
   trägt den Kurszugang — nicht nur die Rechnung. Deshalb heisst der Kasten
   „Dein Zugang": das ist, was sie sucht. Die Kapitel kommen ab 1. November.
🚨 Der einzige Klick in dieser Mail ist die Gruppe. Zwischen Kauf und Start
   liegen bis zu vier Wochen — ohne die Gruppe ist das vier Wochen Funkstille.
🚨 Kein Hinweis auf den Preis und keine Frist. Sie hat gerade gekauft.
""",
 "bloecke": [
   absatz("Hey %FIRSTNAME%,"),
   absatz("schön, dass du dabei bist. Du hast dir gerade einen Platz in "
          "<strong>Easy KI für Networkerinnen</strong> gesichert, und ich freue mich "
          "richtig darauf, dir zu zeigen, was mir in den letzten Jahren den Alltag "
          "umgekrempelt hat."),
   absatz("Damit du weisst, woran du bist: <strong>Der Kurs startet am 1. November.</strong> "
          "Bis dahin musst du nichts vorbereiten, nichts installieren und nichts lesen. "
          "Geniess die Zeit bis dahin, der Rest kommt von allein."),

   h2("Heute nur eine Sache"),
   absatz("Unsere Gruppe auf Telegram ist ab sofort offen. Dort beantworte ich "
          "<strong>dienstags und donnerstags</strong> deine Fragen, dort landen alle "
          "Hinweise zum Start, und dort siehst du, woran die anderen gerade sitzen. "
          "Geh am besten gleich rein, dann verpasst du nichts."),
   knopf("Zur Gruppe", GRUPPE),
   absatz("Wenn der Link bei dir nicht aufgeht, antworte einfach auf diese Mail &mdash; "
          "dann schicke ich ihn dir nochmal."),

   h2("Die Termine auf einen Blick"),
   liste("Merk dir schon mal", [
       "<strong>So, 1. November</strong> &mdash; die ersten Kapitel liegen in deinem Bereich",
       "<strong>Mi, 18. November, abends</strong> &mdash; erster Live-Call, zu deinem "
       "Arbeitsplatz und deinem ersten festen Auftrag",
       "<strong>Do, 10. Dezember, abends</strong> &mdash; zweiter Live-Call, für alles, "
       "was bis dahin aufgetaucht ist",
       "<strong>Und danach</strong> &mdash; die Gruppe bleibt. Sie hört nicht auf, "
       "wenn der Kurs durch ist.",
   ]),
   absatz("Beide Calls werden aufgezeichnet. Wenn du an einem Abend nicht kannst, "
          "schick deine Frage vorher in die Gruppe &mdash; dann beantworte ich sie im "
          "Call, und du schaust sie dir an, wann es dir passt."),

   h2("Dein Zugang"),
   kasten("<p style=\"margin:0;font-family:Arial,sans-serif;font-size:15px;color:%s;"
          "line-height:1.75;\">Deinen <strong>Zugang zum Kursbereich</strong> bekommst du "
          "in einer separaten Mail, zusammen mit der Rechnung. Dort meldest du dich an "
          "&mdash; die Kapitel erscheinen dann ab dem 1. November nach und nach. "
          "Falls die Mail nicht ankommt, schau kurz im Spam-Ordner nach und schreib mir "
          "sonst, dann kümmere ich mich darum.</p>" % NACHT, "#e4f3f4", rand=PETROL),

   absatz("Falls dir zwischendurch eine Frage kommt: Schreib mir. Auf diese Mail, in "
          "der Gruppe oder auf <a href=\"%s\" style=\"color:%s;\">Instagram</a>. "
          "Ich antworte selbst." % (INSTAGRAM, PETROL)),
   gruss("Bis ganz bald,"),
   ps("Wenn du magst, stell dich in der Gruppe kurz vor &mdash; wer du bist und was du "
      "machst. Dann weiss ich beim ersten Kapitel schon, für wen ich schreibe."),
 ],
},

]


# ============================================================================
#  BAUEN
# ============================================================================

def in_zwischenablage(datei, nur_rumpf=False):
    """Die fertige Mail in die Zwischenablage legen.

    Ohne `nur_rumpf` kommt das ganze HTML (mit doctype und head) — das gehört
    in ActiveCampaigns **Code-Editor**.
    Mit `--rumpf` kommt nur, was zwischen <body> und </body> steht — das
    gehört in einen **HTML-Inhaltsblock** im Drag-and-drop-Editor. Wer das
    ganze HTML dort einfügt, bekommt zerschossene Abstände, weil der Editor
    doctype und head herauswirft und die äussere Tabelle mit umbaut.
    """
    import subprocess
    roh = io.open(ZIEL / datei, encoding="utf-8").read()
    sauber = re.sub(r"<!--[\s\S]*?-->", "", roh).strip()
    if nur_rumpf:
        von, bis = sauber.find("<body"), sauber.rfind("</body>")
        if von == -1 or bis == -1:
            print("  Kein <body> gefunden — es bleibt beim ganzen HTML.")
        else:
            sauber = sauber[sauber.find(">", von) + 1:bis].strip()
    ps = ("$t = [Console]::In.ReadToEnd(); Set-Clipboard -Value $t")
    p = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                       input=sauber.encode("utf-8"), capture_output=True)
    if p.returncode:
        print("  Zwischenablage ging nicht:", p.stderr.decode("utf-8", "replace")[:200])
    else:
        print("  in der Zwischenablage: %s (%d Zeichen, %s)"
              % (datei, len(sauber),
                 "nur Rumpf — fuer einen HTML-Inhaltsblock" if nur_rumpf
                 else "ganzes HTML — fuer den Code-Editor"))


def main():
    if "--kopieren" in sys.argv or "--rumpf" in sys.argv:
        datei = MAILS[0]["datei"]
        for a in sys.argv[1:]:
            if a.endswith(".html"):
                datei = a
        return in_zwischenablage(datei, nur_rumpf="--rumpf" in sys.argv)

    ZIEL.mkdir(parents=True, exist_ok=True)
    gebaut = []
    probleme = []

    for m in MAILS:
        html_text = sk.bauen(m)
        pfad = ZIEL / m["datei"]
        io.open(pfad, "w", encoding="utf-8", newline="\n").write(html_text)
        gebaut.append((m, html_text))
        probleme += sk.umlaute_pruefen(m["datei"], html_text) or []
        print("  %-28s  %6d Zeichen   %s" % (m["datei"], len(html_text), m["betreff"]))

    # Kopierseite — dieselbe Vorlage wie bei Startklar
    import html as _html
    karten = []
    for m, _ in gebaut:
        kennung = re.sub(r"[^a-z0-9]+", "", m["datei"].lower())
        karten.append(sk.KARTE.format(
            tag=m["tag"], h1=m["h1"], warten=m["warten"],
            betreff=_html.escape(m["betreff"], quote=False),
            betreff_roh=_html.escape(m["betreff"], quote=True),
            datei=m["datei"], id=kennung))
    seite = sk.KOPIERSEITE.format(karten="\n".join(karten))

    # Der Kopf kommt aus dem Startklar-Geruest und stimmt hier nicht.
    # Gegenprobe bei jeder Ersetzung: sonst laeuft sie still ins Leere, wenn
    # sich die Vorlage aendert, und oben steht weiter „Sieben Mails".
    for alt, neu in [
        ("Mailstrecke · Startklar", "Mailstrecke · Easy KI"),
        ("Startklar · Mailstrecke kopieren", "Easy KI · Mailstrecke kopieren"),
        ("Sieben Mails vom Kauf bis zur Übergabe an die Engine.",
         "Die Mails nach dem Kauf des KI-Kurses."),
    ]:
        if alt not in seite:
            print("  ⚠ Kopfzeile nicht gefunden, bleibt stehen: %r" % alt)
            continue
        assert seite.count(alt) == 1, "mehrdeutig: %r" % alt
        seite = seite.replace(alt, neu)

    # Der Hinweiskasten erklaert die Startklar-Taktung (Tag 12/15, Ziel auf den
    # Kauf-Tag der Kundenmaschine). Hier gibt es eine Mail, die sofort rausgeht.
    # Ueber den ganzen Block ersetzt, nicht ueber den Wortlaut: im erzeugten
    # HTML steht ein echtes Em-Dash statt &mdash;, und daran ist der erste
    # Versuch gescheitert.
    KASTEN = ('<div class="warnung">\n'
              '    <b>Beim Einrichten:</b> Diese Mail geht <b>sofort nach dem Kauf</b> '
              'raus, in der Automation „KI Kurs“. Nimm den Knopf <b>Nur Inhalt</b> und '
              'setz ihn in einen HTML-Block &mdash; das ganze HTML gehört nur in den '
              'Code-Editor.\n  </div>')
    neu_seite, n = re.subn(r'<div class="warnung">[\s\S]*?</div>', KASTEN, seite, count=1)
    if n != 1:
        print("  ⚠ Hinweiskasten nicht gefunden — er bleibt wie im Geruest.")
    else:
        seite = neu_seite
        assert "Tag 12 oder 15" not in seite, "Startklar-Taktung steht noch da"

    io.open(ZIEL / "index.html", "w", encoding="utf-8", newline="\n").write(seite)
    print("  %-28s  Kopierseite mit Kopier-Knoepfen" % "index.html")

    print()
    print("Gruppe:", GRUPPE[:18] + "…  (aus scripts/ki-kurs/.env)")
    print("Ausgabe:", ZIEL)
    if probleme:
        print("UMLAUT-WAECHTER:", " | ".join(str(p) for p in probleme))
    else:
        print("Umlaut-Waechter: sauber.")


if __name__ == "__main__":
    main()
