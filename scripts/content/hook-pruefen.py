"""
Prueft Hooks gegen alle harten Regeln, bevor irgendetwas gebaut wird.

Das Skript findet, was sich mechanisch finden laesst — verbotene Formeln,
Loesungswoerter, Blacklist-Muster, Stakkato, fehlender Network-Anker, Zahlen.
Die zwei wichtigsten Fragen kann es NICHT beantworten; es stellt sie und
verlangt, dass sie beantwortet werden:

  1. Wuerde man das so zu einer Freundin sagen, die gerade im Network ist
     und noch nichts verdient?
  2. Fuehlt sich jemand mit diesen Painpoints gesehen?

Aufruf:
  python scripts/content/hook-pruefen.py "Mein Hook"
  python scripts/content/hook-pruefen.py --datei hooks.txt      # eine Zeile pro Hook
  echo "Mein Hook" | python scripts/content/hook-pruefen.py -
"""
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROT, GELB, GRUEN = "FEHLER", "PRUEFEN", "ok"

# --- Was gar nicht geht -----------------------------------------------------

VERBOTEN = [
    (r"\bsondern\b",
     "„nicht X, sondern Y“ — Blackliste. Zwei eigene Saetze draus machen."),
    (r"Kennst du (das|das Gefuehl|dieses)",
     "„Kennst du das“ — Blackliste."),
    (r"[Ss]tell dir vor",
     "„Stell dir vor“ ist in Instagram-Content gesperrt."),
    (r"ß",
     "scharfes S — Patricia schreibt Schweizer ss."),
    (r"\b(fuer|ueber|waere|koennen|muessen|taeglich|groesser|schoen)\b",
     "ae/oe/ue statt echter Umlaute."),
    (r"^(Guten Morgen|Hallo ihr Lieben|Hey ihr Lieben)",
     "Kein Knall am Anfang — Hook-Knall-Pflicht."),
]

# --- Nicht verboten, aber begruenden ----------------------------------------
# Anleitungs-Formeln standen bis 13.09.2026 auf Rot. Der Beleg dafuer war ein
# einziges Reel (10.09.), das gleichzeitig drei Probleme hatte: Anleitungs-
# Formel UND Loesungswort („eigenes Thema“) UND ein business-internes Thema aus
# der roten Liste. Welche der drei Variablen die Reichweite gekostet hat, ist
# nicht belegt — genau der Methodenfehler, den der Testlog selbst benennt.
# Erfolgreiche Content-Posterinnen nutzen diese Formeln regelmaessig.
# Deshalb: gelb. Fuer kalte Reichweite zurueckhaltend, fuer warme Zielgruppe
# (Stories, Mails, Lead-Posts) regulaer einsetzbar.

ZU_PRUEFEN = [
    (r"\bSo (findest|machst|baust|kommst|gehst|schaffst) du\b",
     "Anleitungs-Formel („So findest du …“) — fuer kalte Reichweite zurueckhaltend "
     "einsetzen, fuer warme Zielgruppe in Ordnung. Sauber nachtesten."),
    (r"\bIn \d+ Schritten\b|\bSchritt für Schritt\b",
     "Anleitungs-Formel („In 3 Schritten …“) — siehe oben."),
    (r"\b\d+ Tipps\b|\bDie \d+ Fehler\b",
     "Listen-Formel („5 Tipps …“ / „Die 3 Fehler …“) — Struktur-Hook, braucht "
     "eigenes Video und eine Caption, die das Versprechen aufloest."),
]

# --- Loesungswoerter: das ist Patricias Antwort, nicht ihr Schmerz ----------

LOESUNGSWOERTER = [
    "eigenes thema", "positionierung", "leadmagnet", "e-mail-liste", "mailingliste",
    "digitales produkt", "digitale produktwelt", "hybridmodell", "funnel",
    "sichtbar werden", "reichweite", "algorithmus", "content-strategie",
    "passives einkommen", "personal brand", "conversion", "zielgruppe",
]

# --- Anker, die die Network-Mama vom allgemeinen Mama-Publikum trennen ------

ANKER = [
    "network", "team", "teamcall", "teamchat", "sponsorin", "upline", "downline",
    "provision", "namensliste", "autoship", "produktabend", "bestellung",
    "nachbestell", "rang", "volumen", "punkte", "partnerin", "vertrieb",
]

# --- Formulierungen, die das Network angreifen statt den Schmerz zu zeigen --

GEGEN_NETWORK = [
    (r"[Nn]etwork (funktioniert nicht|bringt nichts|ist tot)", "greift das Network an"),
    (r"\b(steig|steigt) aus\b|\baussteigen\b", "fordert den Ausstieg"),
    (r"\bhör auf mit\b", "fordert den Ausstieg"),
    (r"\bSchneeball", "greift das Network an"),
]



# --- Schon mal benutzt? ----------------------------------------------------
# Patricia erkennt wiederholte Hooks sofort ("das hatten wir schon mal"), das
# Skript bisher nicht. Deshalb ein Abgleich gegen alles, was schon geschrieben
# wurde: outputs/ und context/.

SUCHORTE = ["outputs", "context", "reference/julia-trost"]
STOPP = set("""der die das ein eine einem einen einer und oder aber wenn dass ich du
mir dir mich dich sich ist sind war hab habe hat haben werden wird wurde nicht kein
keine mein meine dein deine für von mit auf aus bei zu im in am an es so wie noch
schon mal doch ja nein auch nur als wir ihr sie er man denn dann da""".split())


def stamm(w):
    """Grobe Endungs-Kappung, damit stehe/steht/stehen zusammenfallen."""
    for e in ("ungen", "enden", "ende", "esten", "sten", "erin", "innen",
              "en", "er", "es", "em", "et", "st", "te", "e", "n", "s"):
        if len(w) > 5 and w.endswith(e):
            return w[:-len(e)]
    return w


def kerne(text):
    """Inhaltswoerter auf den Stamm gekappt — Umformulierungen fallen so auf."""
    woerter = [stamm(w) for w in re.findall(r"[a-zäöü]+", text.lower())
               if w not in STOPP and len(w) > 2]
    return set(woerter)


def schon_benutzt(hook, wurzel=None):
    """Sucht Zeilen, die denselben Gedanken schon einmal gesagt haben.

    Nicht nach exakter Wiederholung, sondern nach Ueberdeckung der
    Inhaltswoerter — Patricia erkennt einen Hook auch dann wieder, wenn er
    umformuliert ist ("das hatten wir schon mal").
    """
    wurzel = Path(wurzel or Path(__file__).resolve().parents[2])
    gesucht = kerne(hook)
    if len(gesucht) < 3:
        return []
    treffer = []
    for ort in SUCHORTE:
        basis = wurzel / ort
        if not basis.is_dir():
            continue
        for datei in basis.rglob("*.md"):
            try:
                inhalt = datei.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for nr, zeile in enumerate(inhalt.splitlines(), 1):
                if len(zeile) < 25 or len(zeile) > 400:
                    continue
                andere = kerne(zeile)
                if len(andere) < 3:
                    continue
                gemeinsam = gesucht & andere
                # Gegen die laengere Seite messen: sonst meldet jeder Satz,
                # der zufaellig drei gleiche Woerter enthaelt, einen Treffer.
                anteil = len(gemeinsam) / max(len(gesucht), len(andere))
                if anteil >= 0.5 and len(gemeinsam) >= 3:
                    treffer.append((datei.relative_to(wurzel), nr,
                                    zeile.strip()[:110], round(anteil * 100)))
    # Nur die deutlichsten zeigen — eine Warnung, die dauernd faelschlich
    # anschlaegt, wird nach drei Tagen ignoriert.
    treffer.sort(key=lambda t: -t[3])
    return treffer[:3]


def saetze(text):
    return [s.strip() for s in re.split(r"(?<=[.!?“])\s+", text) if s.strip()]


def pruefe(hook):
    befunde = []

    for muster, hinweis in VERBOTEN:
        if re.search(muster, hook):
            befunde.append((ROT, hinweis))

    for muster, hinweis in ZU_PRUEFEN:
        if re.search(muster, hook):
            befunde.append((GELB, hinweis))

    klein = hook.lower()
    for w in LOESUNGSWOERTER:
        if w in klein:
            befunde.append((ROT, "Loesungswort „%s“ im Hook — das ist die Antwort, "
                                 "nicht ihr Schmerz." % w))

    for muster, hinweis in GEGEN_NETWORK:
        if re.search(muster, hook):
            befunde.append((ROT, "%s — sie liebt ihr Network und verteidigt es dann."
                            % hinweis))

    if not any(a in klein for a in ANKER):
        befunde.append((GELB, "Kein Network-Anker in der Zeile — koennte jede Mama "
                              "mit Smartphone unterschreiben. Anker: Teamcall, "
                              "Sponsorin, Provision, Namensliste, Bestellung …"))

    # Stakkato: drei kurze Saetze hintereinander
    lang = [len(s.split()) for s in saetze(hook)]
    lauf = 0
    for n in lang:
        lauf = lauf + 1 if n <= 4 else 0
        if lauf >= 3:
            befunde.append((ROT, "Stakkato — drei kurze Saetze hintereinander."))
            break

    if re.search(r"\d", hook):
        befunde.append((GELB, "Zahl im Hook — stammt sie aus patricia-expertise.md "
                              "oder von Patricia selbst? Sonst raus."))

    for datei, nr, zeile, anteil in schon_benutzt(hook):
        befunde.append((GELB, "Das hatten wir schon (%d%% Ueberdeckung) — %s:%d\n"
                              "           „%s“" % (anteil, datei, nr, zeile)))

    erste = hook.strip().splitlines()[0] if hook.strip() else ""
    if len(erste) > 95:
        befunde.append((GELB, "Erste Zeile ist lang (%d Zeichen) — sie muss allein "
                              "catchen." % len(erste)))

    return befunde


TORE = """
  Diese zwei Fragen beantwortet kein Skript. Beantworte sie schriftlich,
  bevor der Hook gebaut wird:

  1  Wuerdest du das so zu einer Freundin sagen, die gerade im Network ist
     und noch nichts verdient?
     -> Wenn es sich geschrieben anfuehlt statt gesprochen: umschreiben.

  2  Fuehlt sich jemand mit diesen Painpoints gesehen?
     -> Welcher Schmerz aus context/kern-painpoint.md genau? Benenne ihn.
        Findest du keinen, ist es kein Hook, sondern eine Aussage.
"""


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    if args[0] == "-":
        hooks = [z for z in sys.stdin.read().splitlines() if z.strip()]
    elif args[0] == "--datei":
        hooks = [z for z in Path(args[1]).read_text(encoding="utf-8").splitlines()
                 if z.strip()]
    else:
        hooks = [" ".join(args)]

    schwer = 0
    for hook in hooks:
        print("\n" + "-" * 72)
        print(hook)
        befunde = pruefe(hook)
        if not befunde:
            print("  %s — mechanisch sauber" % GRUEN)
        for stufe, hinweis in befunde:
            print("  %-8s %s" % (stufe, hinweis))
            if stufe == ROT:
                schwer += 1

    print("\n" + "=" * 72)
    print(TORE)
    print("=" * 72)
    if schwer:
        print("%d harte Verstoesse. Erst umschreiben, dann bauen." % schwer)
        sys.exit(1)
    print("Mechanisch in Ordnung. Jetzt die zwei Fragen oben beantworten.")


if __name__ == "__main__":
    main()
