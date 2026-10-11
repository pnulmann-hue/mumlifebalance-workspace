# -*- coding: utf-8 -*-
"""Baut den Ordner, den Patricia im Webinar bei ChatGPT hochlaedt.

    python scripts/ki-kurs/demo-ordner-bauen.py [--ziel <Pfad>]

Warum ein eigener Ordner und nicht die Dateien aus dem Workspace:

* Beim Hochladen sieht man den Dateidialog, und darin die Nachbarordner.
  Neben `context/` liegen `persoenlich` und `finanzen`. Ein eigener Ordner
  zeigt nur das, was gezeigt werden soll.
* Die Quelldateien tragen Verweise auf fremde Kurse und echte Umsatzzahlen.
  Beides hat in einem Chat nichts zu suchen, den jemand mitliest.
* Die Dateinamen SIND sichtbar. Also heissen sie wie das, was drinsteht.

Der Waechter am Ende prueft jede erzeugte Datei. Faellt er an, wird nichts
geschrieben \u2014 lieber kein Ordner als einer mit fremden Namen darin.
"""
import io, os, re, sys, datetime

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ZIEL = os.path.join(os.path.expanduser("~"), "Desktop", "webinar-demo")
if "--ziel" in sys.argv:
    ZIEL = sys.argv[sys.argv.index("--ziel") + 1]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def lies(pfad, von=None, bis=None):
    zeilen = io.open(os.path.join(WURZEL, pfad), encoding="utf-8").read().splitlines()
    return "\n".join(zeilen[(von - 1 if von else 0):(bis if bis else len(zeilen))])


def ohne_meta(text, bis_abschnitt=None):
    """Wirft interne Meta-Hinweise raus: Konfliktregeln zwischen Dokumenten,
    Verweise auf fremde Kurse, Entscheidungs-Historie. In einem Chat, den
    jemand mitliest, hat beides nichts zu suchen — und als Anweisung an die
    KI taugt es auch nicht, weil es von Dokumenten handelt, die sie nicht hat."""
    if bis_abschnitt:
        i = text.find(bis_abschnitt)
        if i > 0:
            text = text[:i].rstrip() + chr(10)
    MARKER = ("Julia", "Trost", "Agent 3", "Framework-Docs", "Jens-Neubeck",
              "scripts/", "python ")
    raus = [z for z in text.splitlines()
            if not any(m in z for m in MARKER)]
    # Verweise auf Dateien, die ChatGPT nicht hat, machen aus einer Regel
    # eine Fehlermeldung ("ich kann diese Datei nicht lesen"). Also raus damit,
    # ohne die Regel daneben zu opfern.
    ERSATZ = [
        ("(`context/kundinnen-geschichten.md`)", ""),
        ("_Detaillierte Analyse: `context/patricia-expertise.md` (Teil 2). "
         "Kurzliste hier als Quick-Reference._", ""),
        ("Zahlen nur aus `context/patricia-expertise.md` oder aus dem, was ich "
         "dir gebe.", "Zahlen nur aus dem, was ich dir gebe."),
        ("`context/`", "meinen Unterlagen"),
    ]
    sauber2 = []
    for z in raus:
        for a, b in ERSATZ:
            if a in z:
                z = z.replace(a, b)
        sauber2.append(z)
    raus = sauber2

    # TEIL-Nummern stammen aus einem groesseren Dokument und ergeben hier keinen Sinn
    raus = [z.replace("## TEIL 10: VOICE-LAYER — die neun Kniffe",
                      "## Neun Kniffe, damit es nach mir klingt")
             .replace("## TEIL 11: VERBOTE — was nie in einen Hook kommt",
                      "## Was nie in einen Hook kommt")
             .replace("## TEIL 12: 🚨 DER HOOK-CHECK — Pflicht vor der Auslieferung",
                      "## Der letzte Check vor der Abgabe")
             .replace("## TEIL 5: ANGLES — aus welcher Richtung du schaust",
                      "## Aus welcher Richtung du schaust")
            for z in raus]

    # keine drei Leerzeilen am Stueck, wo etwas entfernt wurde
    sauber, leer = [], 0
    for z in raus:
        leer = leer + 1 if not z.strip() else 0
        if leer <= 2:
            sauber.append(z)
    return chr(10).join(sauber)


def abschnitte(pfad, titel_liste):
    """Holt benannte Abschnitte aus einer Markdown-Datei.
    Warnt je Titel, der nicht gefunden wurde \u2014 sonst schrumpft die Datei
    still, und das faellt nur auf, wenn jemand auf die Zeichenzahl schaut."""
    text = io.open(os.path.join(WURZEL, pfad), encoding="utf-8").read()
    raus = []
    for titel in titel_liste:
        m = re.search(r"^(#{2,3} .*%s.*)$" % re.escape(titel), text, re.M | re.I)
        if not m:
            print("   WARNUNG: Abschnitt nicht gefunden: %s" % titel)
            continue
        start = m.start()
        ebene = len(m.group(1)) - len(m.group(1).lstrip("#"))
        folge = re.search(r"^#{1,%d} " % ebene, text[m.end():], re.M)
        raus.append(text[start:m.end() + folge.start()] if folge else text[start:])
    return "\n\n".join(raus)


# --------------------------------------------------------------- die Dateien
HEUTE = datetime.date.today().isoformat()

DATEIEN = {}

DATEIEN["1-wer-meine-leute-sind.md"] = ohne_meta(lies("context/kern-painpoint.md"))

DATEIEN["2-wie-ich-rede.md"] = (
    "# Wie ich rede\n\n"
    "Das ist meine Stimme. Jeder Text, den du mir schreibst, muss so klingen.\n\n"
    + ohne_meta(lies("context/brand-voice.md", von=9, bis=260)))

DATEIEN["3-was-einen-hook-traegt.md"] = (
    "# Was einen guten Hook ausmacht\n\n"
    "Die erste Zeile entscheidet, ob jemand weiterliest. Diese Regeln gelten "
    "f\u00fcr jede erste Zeile, die du mir schreibst.\n\n"
    "## Die drei Prinzipien\n\n"
    "1. **Eine Frage, die sie kennt** \u2014 nicht \u201eWillst du produktiver werden?\u201c, "
    "sondern eine Frage, auf die sie innerlich mit \u201ewoher weisst du das\u201c antwortet.\n"
    "2. **Szene statt Thema** \u2014 eine Uhrzeit, ein Ort, eine Handlung. Etwas, das "
    "man vor sich sieht.\n"
    "3. **Mein Gegenbild daneben** \u2014 erst ihre Lage, dann meine. In dieser "
    "Reihenfolge.\n\n"
    "## Was ich gemessen habe\n\n"
    "Beitr\u00e4ge, deren erste Zeile eine **Frage** ist, laufen bei mir rund "
    "2,6-mal besser als der Schnitt. Beitr\u00e4ge, die mit \u201eFolge mir, wenn \u2026\u201c "
    "anfangen, laufen schlechter als alles andere.\n\n"
    + ohne_meta(abschnitte(".claude/skills/hooks/SKILL.md",
                 ["VOICE-LAYER", "VERBOTE", "DER HOOK-CHECK", "ANGLES"])))

DATEIEN["4-was-nie-vorkommt.md"] = (
    "# W\u00f6rter und Wendungen, die nie vorkommen d\u00fcrfen\n\n"
    "Wenn du eines davon benutzt, schreibe den Satz neu.\n\n"
    + ohne_meta(lies("context/ki-phrasen-blackliste.md", von=3),
                bis_abschnitt="## Verbindlichkeits-Regel"))

def angebote():
    """Was ich anbiete — ohne Preise. Fuer einen Hook zaehlt, WORAUF er
    zulaeuft und fuer wen, nicht was es kostet. Und ohne Preise bleibt der
    Waechter scharf, der Geldbetraege verbietet."""
    import json
    d = json.loads(lies("context/active-funnels.json"))
    fl = d.get("funnels") or d
    if isinstance(fl, dict):
        fl = list(fl.values())
    zeilen = ["# Was ich anbiete", "",
              "Ein Hook laeuft immer auf etwas zu. Das hier sind meine Angebote —",
              "damit du weisst, wohin ein Beitrag fuehren kann.", ""]
    for f in fl:
        if not isinstance(f, dict):
            continue
        if "live" not in str(f.get("status") or f.get("aktiv") or ""):
            continue
        name = (f.get("name") or f.get("titel") or "").strip()
        wofuer = (f.get("transformation") or f.get("versprechen")
                  or f.get("beschreibung") or f.get("ziel") or "").strip()
        if not name:
            continue
        zeilen.append("- **%s**%s" % (name, (" — " + wofuer) if wofuer else ""))
    return chr(10).join(zeilen) + chr(10)


DATEIEN["5-was-ich-anbiete.md"] = angebote()

DATEIEN["WAS-DU-DAZU-SAGST.txt"] = (
    "WAS IN DEM DOKUMENT STEHT - du laedst EINE Datei hoch:" + chr(10) +
    "ALLES-IN-EINEM.md" + chr(10) +
    "Zum Ansagen, während du hochlädst. Du zeigst sie nicht." + chr(10) +
    chr(10) +
    "1 - Wer meine Leute sind" + chr(10) +
    "   Der eine Satz, den meine Kundin denkt, bevor sie weiss, dass es eine" + chr(10) +
    "   Lösung gibt. Dazu, wie sie ihn sich selber stellt — in ihren Worten," + chr(10) +
    "   nicht in meinen. Und was sie nie hören will." + chr(10) +
    chr(10) +
    "2 - Wie ich rede" + chr(10) +
    "   Meine Stimme. Wie lang meine Sätze sind, wie ich jemanden anspreche," + chr(10) +
    "   wie viel von mir vorkommt. Und der Unterschied zwischen meiner Kundin" + chr(10) +
    "   und deren Kundschaft — den verwechselt jede KI." + chr(10) +
    chr(10) +
    "3 - Was einen Hook trägt" + chr(10) +
    "   Die drei Dinge, die bei mir immer funktionieren: eine Frage, die sie" + chr(10) +
    "   kennt. Eine Szene statt eines Themas. Mein Gegenbild daneben." + chr(10) +
    "   Dazu die Zahl: Beiträge mit einer Frage in Zeile eins laufen bei mir" + chr(10) +
    "   rund zweieinhalbmal besser." + chr(10) +
    chr(10) +
    "4 - Was nie vorkommt" + chr(10) +
    "   Die Wörter und Wendungen, an denen man eine KI sofort erkennt." + chr(10) +
    "   Meine Liste, über Monate gewachsen." + chr(10) +
    chr(10) +
    "5 - Was ich anbiete" + chr(10) +
    "   Worauf ein Beitrag zulaufen kann. Ohne das schreibt eine KI einen" + chr(10) +
    "   schönen Satz, der nirgendwohin führt." + chr(10) +
    chr(10) +
    "---" + chr(10) +
    chr(10) +
    "DIE POINTE, wenn beide Ergebnisse nebeneinander stehen:" + chr(10) +
    chr(10) +
    "   Der Prompt war gut. Genau so einer kursiert auf Instagram, und wer" + chr(10) +
    "   ihn benutzt, macht nichts falsch. Er sagt: Frauen zwischen 30 und 45." + chr(10) +
    "   Das sind Millionen - und keine einzige bestimmte. Rechts steht" + chr(10) +
    "   derselbe Prompt, Wort für Wort. Der Unterschied ist nicht, was ich" + chr(10) +
    "   gesagt habe. Der Unterschied ist, was sie vorher gelesen hat." + chr(10) +
    chr(10) +
    "UND DANN - darum geht es im ganzen Webinar:" + chr(10) +
    chr(10) +
    "\"Das hier habe ich jetzt einmal hochgeladen. Morgen, im nächsten Chat," + chr(10) +
    " ist es wieder weg - dann lade ich es wieder hoch. Bei meinem Arbeitsplatz" + chr(10) +
    " liegen genau diese Dateien an ihrem Platz, und sie werden bei JEDEM" + chr(10) +
    " Auftrag gelesen, ohne dass ich etwas tue. Ich habe sie einmal" + chr(10) +
    " geschrieben. Das ist der Unterschied zwischen einem guten Prompt und" + chr(10) +
    " einer KI, die dich kennt.\"" + chr(10) +
    chr(10) +
    "Und wenn jemand fragt, wie diese Dateien entstehen:" + chr(10) +
    "\"Genau das machen wir im Kurs zusammen.\"" + chr(10))

DATEIEN["AUFTRAG-zum-kopieren.txt"] = (
    "Du bist ein erfahrener Social-Media-Texter mit zehn Jahren Erfahrung in" + chr(10) +
    "Online-Marketing und Personal Branding." + chr(10) +
    chr(10) +
    "Deine Aufgabe: Schreibe mir fünf aufmerksamkeitsstarke Hooks für ein" + chr(10) +
    "Instagram-Reel." + chr(10) +
    chr(10) +
    "Thema: Niemand reagiert auf meine Beiträge." + chr(10) +
    "Zielgruppe: Frauen zwischen 30 und 45, die sich neben der Familie etwas" + chr(10) +
    "Eigenes aufbauen wollen." + chr(10) +
    "Ziel: Maximale Reichweite und Verweildauer." + chr(10) +
    "Tonalität: Locker, nahbar, auf Augenhöhe. Kein Werbesprech." + chr(10) +
    chr(10) +
    "Beachte dabei:" + chr(10) +
    "- Der Hook muss in den ersten drei Sekunden fesseln" + chr(10) +
    "- Nutze Neugier, Emotion oder einen überraschenden Einstieg" + chr(10) +
    "- Höchstens zwölf Wörter pro Hook" + chr(10) +
    "- Sprich die Zielgruppe direkt mit du an" + chr(10) +
    chr(10) +
    "Gib die fünf Hooks als nummerierte Liste aus." + chr(10))


# --- Eine Datei aus allen fuenf. ChatGPT nimmt nur einen Upload an. -------
# Die Reihenfolge ist Absicht: erst WER (ohne das ist alles andere wirkungslos),
# dann WIE ich rede, dann die Hook-Mechanik, dann die Verbote, zuletzt wohin
# es fuehrt. Die Verbote stehen spaet, weil die letzten Anweisungen am besten
# haften.
TEILE = ["1-wer-meine-leute-sind.md", "2-wie-ich-rede.md",
         "3-was-einen-hook-traegt.md", "4-was-nie-vorkommt.md",
         "5-was-ich-anbiete.md"]

_kopf = (
    "# Mein Hintergrundwissen" + chr(10) + chr(10) +
    "Lies das hier ganz durch, bevor du mir etwas schreibst. Alles, was du "
    "danach formulierst, muss dazu passen: zu meinen Leuten, zu meiner "
    "Sprache, zu meinen Regeln." + chr(10) + chr(10) +
    "Es sind fünf Teile:" + chr(10) + chr(10) +
    "1. Wer meine Leute sind" + chr(10) +
    "2. Wie ich rede" + chr(10) +
    "3. Was einen Hook trägt" + chr(10) +
    "4. Was nie vorkommt" + chr(10) +
    "5. Was ich anbiete" + chr(10) + chr(10) +
    "Wenn ein Vorschlag gegen Teil 4 verstösst, schreib ihn neu. Wenn du "
    "zwischen Teil 2 und einer allgemeinen Schreibregel wählen musst, "
    "gewinnt Teil 2." + chr(10) + chr(10) +
    "---" + chr(10) + chr(10))

def _ohne_frontmatter(text):
    """Obsidian-Tags am Dateianfang raus. In einem zusammengefuegten Dokument
    stehen sie mitten im Text und sehen aus wie ein Abschnittstrenner."""
    z = text.splitlines()
    if z and z[0].strip() == "---":
        for _k in range(1, min(len(z), 12)):
            if z[_k].strip() == "---":
                return chr(10).join(z[_k + 1:]).lstrip()
    return text


_voll = [_kopf]
for _i, _n in enumerate(TEILE, 1):
    _raus, _erste = [], True
    for _z in _ohne_frontmatter(DATEIEN[_n]).splitlines():
        if _z.startswith("# "):
            if _erste:
                _raus.append("# TEIL %d — %s" % (_i, _z[2:].strip()))
                _erste = False
            else:
                # eine zweite H1 in derselben Quelle wird Unterabschnitt,
                # sonst steht "TEIL 4" zweimal da
                _raus.append("## " + _z[2:].strip())
        elif _z.startswith("#"):
            _raus.append("#" + _z)   # alles darunter eine Ebene tiefer
        else:
            _raus.append(_z)
    _voll.append(chr(10).join(_raus).strip() + chr(10) + chr(10) + "---" + chr(10))

DATEIEN["ALLES-IN-EINEM.md"] = chr(10).join(_voll)


# --------------------------------------------------------- der Waechter
FREMD = [r"Julia\w*", r"juliatrost", r"Trost-Sync", r"Frau Trost", r"Kevin\b",
         r"Fiedler", r"Elke\s*Mayr", r"Nikoleta", r"Reichweitenherz",
         r"Katrin\s*Hill", r"Dascha", r"F\u00fchlbarmacherin", r"Hormozi",
         r"Kelsie", r"Blevins", r"Jenya", r"Kork", r"Raabe", r"Apeli",
         r"karriere\.mum", r"Anni\s*Hoffmann", r"Herr\s*Tech", r"Brandastic",
         r"Nadja", r"Submagic"]
GELD = r"CHF\s*[0-9][0-9'\.]*|[0-9][0-9'\.]*\s*(?:CHF|EUR|Franken)"
MAIL = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

fehler = []
for name, text in DATEIEN.items():
    for muster in FREMD:
        for m in re.finditer(muster, text, re.I):
            fehler.append("%s: fremder Name %r" % (name, m.group(0)))
    for m in re.finditer(GELD, text):
        fehler.append("%s: Geldbetrag %r" % (name, m.group(0)))
    for m in re.finditer(MAIL, text):
        fehler.append("%s: Mailadresse %r" % (name, m.group(0)))

if fehler:
    print("ABBRUCH \u2014 der Ordner wurde NICHT geschrieben:")
    for f in fehler[:25]:
        print("   " + f)
    if len(fehler) > 25:
        print("   \u2026 und %d weitere" % (len(fehler) - 25))
    sys.exit(1)

os.makedirs(ZIEL, exist_ok=True)
for name, text in DATEIEN.items():
    with io.open(os.path.join(ZIEL, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(text if text.endswith("\n") else text + "\n")
    print("  %-34s %6d Zeichen" % (name, len(text)))

print("\nOrdner: %s" % ZIEL)
print("W\u00e4chter: keine fremden Namen, keine Betr\u00e4ge, keine Mailadressen.")
