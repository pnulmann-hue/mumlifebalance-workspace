# -*- coding: utf-8 -*-
"""Baut den vollständigen Marken-Brief für die Artifacts (14.09.2026).

Warum es das gibt: Content-Studio und Bild-Editor laufen IN einer Artifact-Seite. Eine
Seite kommt nicht an den Workspace, also nicht an `context/` und nicht an die Skills.
Patricia erwartet aber zu Recht, dass das Content-Studio dasselbe weiss wie `/content`.

Also wird der Brief hier **aus den echten Quellen zusammengestellt** und als Dokument
`daten/wissen-voll` in beide Artifact-Datenbanken geschrieben. Damit ist es eine
erzeugte Kopie und keine Abschrift von Hand — ändert sich eine Quelle, lässt man das
Skript laufen und schreibt das Ergebnis neu.

    python scripts/cockpit/wissen-bauen.py outputs/cockpit/abgleich

Danach mit `Artifact write_db` in beide Artifacts, Sammlung `daten`, Dokument
`wissen-voll`.

🚨 Zwei Grenzen sind eingebaut:
- **Keine Namen fremder Mentorinnen.** Die Seiten sind teilbar, und Patricias Regel dazu
  ist eindeutig. Das Skript prüft das nach dem Bauen und bricht ab, wenn einer durchrutscht.
- **Keine zugekauften Kataloge.** Aus dem Hook-Skill kommt die Mechanik, nicht die
  Formel-Sammlungen und Beispiele. Die bleiben lokal.
"""
import io, json, os, re, sys

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

ZIEL = sys.argv[1] if len(sys.argv) > 1 else "outputs/cockpit/abgleich"

# Namen, die in einer teilbaren Seite nichts zu suchen haben
FREMDE_NAMEN = ["Julia Trost", "Julia", "Trost", "Elke Mayr", "Karriere Mum",
                "Jenya Kork", "Kelsie", "Hormozi", "Nadja", "Brandastic",
                "Reichweitenherz", "Olga", "aga.bieschke", "Jens Neubeck"]
ERSATZ = "meiner Mentorin"


def lies(pfad):
    if not os.path.exists(pfad):
        return ""
    t = io.open(pfad, encoding="utf-8").read()
    # Frontmatter weg
    if t.startswith("---"):
        teile = t.split("---", 2)
        if len(teile) == 3:
            t = teile[2]
    return t


def abschnitte(text, titel_liste):
    """Zieht die genannten Abschnitte heraus, jeweils bis zur nächsten Überschrift
    gleicher oder höherer Ebene."""
    raus = []
    zeilen = text.split("\n")
    for titel in titel_liste:
        start = None
        ebene = 0
        for i, z in enumerate(zeilen):
            m = re.match(r"^(#{2,4})\s+(.*)$", z)
            if m and titel.lower() in m.group(2).lower():
                start = i
                ebene = len(m.group(1))
                break
        if start is None:
            # 🚨 Nie stillschweigend weglassen. Am 19.09.2026 wurde ein Abschnitt
            # in der Quelle umbenannt — der Baustein wurde dadurch kleiner, und
            # das faellt nur auf, wenn jemand auf die Zeichenzahl schaut.
            print(f"  WARNUNG: Abschnitt „{titel}“ nicht gefunden — faellt raus.")
            continue
        stueck = [zeilen[start]]
        for z in zeilen[start + 1:]:
            m = re.match(r"^(#{2,4})\s", z)
            if m and len(m.group(1)) <= ebene:
                break
            stueck.append(z)
        raus.append("\n".join(stueck).rstrip())
    return "\n\n".join(raus)


def saeubern(t):
    """Wiki-Links, Verweise auf Dateien und Leerzeilen-Wüsten raus — das versteht
    die Seite ohnehin nicht."""
    t = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", t)
    t = re.sub(r"\[\[([^\]]+)\]\]", r"\1", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    t = re.sub(r"^\s*>\s?", "", t, flags=re.M)
    return t.strip()


# --------------------------------------------------------------- die Bausteine
BAUSTEINE = []


def dazu(titel, inhalt, quelle):
    inhalt = saeubern(inhalt)
    if inhalt:
        BAUSTEINE.append((titel, inhalt, quelle))


# 1 — Stimme
bv = lies("context/brand-voice.md")
dazu("STIMME UND SCHREIBREGELN",
     # „Persönlichkeit zeigen" seit 02.10.2026 dabei: dort stehen Referenztext,
     # Freundinnen-Test, ihre Wörter, derbe Wörter und wie sie verkauft (Interview B).
     abschnitte(bv, ["Tonalität", "Persönlichkeit zeigen", "Schreibregeln",
                     "Kernbotschaft", "Patricias authentische Sprachmuster"]),
     "context/brand-voice.md")

# 2 — Wunschkundin Mentoring
kp = lies("context/kern-painpoint.md")
dazu("WUNSCHKUNDIN MENTORING — der Kern-Schmerz",
     abschnitte(kp, ["Der Satz", "Wie sie es sich selbst stellt",
                     "Sie liebt ihr Network", "Die drei Bedingungen sind deine drei Antworten",
                     "Was daraus folgt", "Was NICHT in den Einstieg gehört"]),
     "context/kern-painpoint.md")

# 3 — Wunschkundin doTERRA
dt = lies("outputs/zielgruppen-research/doterra-2026-04-22.md")
pp = re.findall(r"^### (PP\d+:.*?)$\n(.*?)(?=^### |\Z)", dt, flags=re.M | re.S)
kurz = []
for kopf, koerper in pp[:10]:
    trig = re.search(r"\*\*Haupt-Trigger:\*\*\s*(.+)", koerper)
    kurz.append("- " + kopf.strip() + (" — " + trig.group(1).strip() if trig else ""))
dazu("WUNSCHKUNDIN doTERRA — die zehn Schmerzen mit ihrer Szene",
     "\n".join(kurz) + "\n\nPflicht: keine Heilversprechen, keine Wirkaussagen zu Ölen. "
     "Immer im Rahmen „bei mir war es so“. Nie gegen Ärztinnen oder Medikamente.",
     "outputs/zielgruppen-research/doterra-2026-04-22.md")

# 4 — Captions
cf = lies("context/caption-formeln.md")
dazu("CAPTION — Formeln, CTA und Hashtags",
     abschnitte(cf, ["Formel 1", "Formel 2", "Formel 3", "Formel 4", "Formel 5",
                     "CTA-Varianten", "Hashtag-Strategie",
                     "Die 7 Kaufpsychologie-Trigger", "Copy-Antipatterns",
                     "Copy-Grundregel", "Feature → Transformation Transfer"]),
     "context/caption-formeln.md")

# 5 — Jobs
js = lies("context/job-saeulen.md")
dazu("JOB-SÄULEN — jeder Beitrag hat einen Job",
     abschnitte(js, ["Die 4 Jobs", "Mentoring-Profil — Job-Verteilung",
                     "doTERRA-Profil — Job-Verteilung"]),
     "context/job-saeulen.md")

# 6 — PIE steckt vollständig im Hook-Skill (TEIL 6) und kommt mit Baustein 7 mit.
#      Kein eigener Baustein, sonst steht der Pflicht-Mix zweimal im Auftrag.
hs = lies(".claude/skills/hooks/SKILL.md")

# 7 — Der ganze Hook-Skill
# Patricia am 14.09.2026: „ich will alle ideen drin haben." Also kommt alles mit —
# die vier Säulen, die Reichweiten-Hierarchie, Bewusstseinsstufen, Angles, PIE mit den
# rund 80 Kalender-Formeln, die 27 Formeln, die 10 Reveal-Frameworks, die 50 Vorlagen,
# der Voice-Layer, die Verbote, der Hook-Check, die CTA-Regel und der letzte Check.
# Draussen bleibt nur die Quellen-Liste am Schluss: dort stehen die fremden Kurse
# namentlich, und die Seite ist teilbar.
hook_text = hs
schnitt = hook_text.find("## 📚 Quellen")
if schnitt > 0:
    hook_text = hook_text[:schnitt]
dazu("ALLES ZUM HOOK — der vollständige Werkzeugkasten", hook_text,
     ".claude/skills/hooks/SKILL.md")

# 8 — Verbote
bl = lies("context/ki-phrasen-blackliste.md")
dazu("VERBOTENE SPRACHE",
     abschnitte(bl, ["ABSOLUTE TOP-VERBOTE", "Nicht/Sondern-Konstrukte",
                     "Dreier-Stakkatos", "Pseudo-konkrete Worthülsen",
                     "Abstrakte Content-Benefits", "Stell dir vor"]),
     "context/ki-phrasen-blackliste.md")

# 9 — Was nachweislich wirkt
cr = lies("context/content-radar-juni-2026.md")
dazu("WAS NACHWEISLICH WIRKT UND WAS NICHT",
     abschnitte(cr, ["Was nachweislich funktioniert", "Was nachweislich NICHT funktioniert"]),
     "context/content-radar-juni-2026.md")

# 10 — Keywords
mk = lies("context/manychat-keywords.md")
dazu("KOMMENTAR-STICHWÖRTER",
     abschnitte(mk, ["Mentoring-Profil", "doTERRA-Profil", "Regeln für den Assistenten"]),
     "context/manychat-keywords.md")

# 11 — Angebote
try:
    af = json.load(io.open("context/active-funnels.json", encoding="utf-8"))
    zeilen = []
    for f in af.get("funnels", []):
        if f.get("status", "").startswith("live") or "pilot" in f.get("status", ""):
            zeilen.append("- " + f.get("name", "") + " (" + f.get("typ", "") + ")")
    treppe = json.dumps(af.get("produkttreppe_mentoring", []), ensure_ascii=False, indent=1)
    dazu("ANGEBOTE, DIE GERADE LAUFEN", "\n".join(zeilen) + "\n\nProdukttreppe:\n" + treppe,
         "context/active-funnels.json")
except Exception as e:
    print("Angebote konnten nicht gelesen werden:", e)

# --------------------------------------------------------------- zusammensetzen
text = "\n\n".join("== " + t + " ==\n" + i for t, i, _ in BAUSTEINE)

# Namensfilter — die Seiten sind teilbar.
# `\w*` am Ende, weil „Julias Framework" sonst durchrutscht: nach dem Namen steht
# ein s, also greift die Wortgrenze nicht. Genau so ist es beim ersten Lauf passiert.
for name in FREMDE_NAMEN:
    # Genitiv zuerst: „Julias Framework" wird „Framework meiner Mentorin",
    # sonst stünde da „meiner Mentorin Framework".
    text = re.sub(r"\b" + re.escape(name) + r"s\s+(\w+)", r"\1 " + ERSATZ, text)
    text = re.sub(r"\b" + re.escape(name) + r"\w*", ERSATZ, text)
text = text.replace(ERSATZ + "-" + ERSATZ, ERSATZ)
text = re.sub(r"(" + re.escape(ERSATZ) + r")(\s*[-–]\s*)?(?=" + re.escape(ERSATZ) + r")", "", text)
rest = [n for n in FREMDE_NAMEN if re.search(r"\b" + re.escape(n) + r"\w*", text)]
if rest:
    print("ABBRUCH — fremde Namen noch im Text:", rest)
    sys.exit(1)

# ------------------------------------------------- Wissen je Format
# Patricia am 14.09.2026: „bei reels wäre dann aber das wissen aus skill reel wichtig,
# bei karussell das von karussell und bei story der storyskill."
# Das geht NICHT in den allgemeinen Brief — sonst schleppt jeder Auftrag alle drei mit.
# Stattdessen ein eigener Block je Format, und die Seite hängt nur den passenden an.
rf = lies("context/reels-framework.md")
kf = lies("context/karussell-framework.md")
sf = lies("context/story-framework.md")

FORMATE = {
    "reel": [
        (rf, ["Viral-Mechanik 2026", "Die 3-Sekunden-Regel", "Reel-Typen (für Mum Life Balance)",
              "Struktur-Formel für JEDES Reel", "On-Screen-Text", "Audio-Strategie",
              "Transitions & Cuts", "Licht & Kamera", "Patricias Schwachstellen",
              "Dreh-Anweisung — Talking Head", "Hook-Bauen: Strenger Pflicht-Prozess",
              "Reel-Cover", "Untertitel im Video", "Rechtliches",
              "Reel-Serien", "Posting-Zeiten pro Profil", "Top-5-Hashtags pro Profil"]),
        (lies("context/sprechreels-drehanleitung.md"), None),
    ],
    "karussell": [
        # 🚨 Diese drei standen bis 19.09.2026 NUR im Skill und kamen deshalb nie
        # im Cockpit an — dort wurden Karussells ohne sie geschrieben.
        (kf, ["Die vier Typen sind die Liste", "Funnel-Stufe ist eine Pflicht-Angabe",
              "Erst die Texte freigeben, dann bauen",
              "Grundregeln", "Karussell-Spezifika", "Feed-Aesthetic — das grosse",
              "Bauweisen innerhalb der vier Typen", "Karussell-Doktor-Checkliste",
              "Karussell-Briefing-Template", "Regeln für den Assistenten",
              "Update 2026-04-22"]),
    ],
    "story": [
        (sf, ["Die zwei nicht-verhandelbaren Kernregeln", "Slide-Struktur",
              "Käufertyp-System", "Die 8 Modi", "Erfolgs-Kriterien"]),
        (lies("context/julia-insta-stories-anleitung.md"), None),
        (lies("context/julia-story-ideen.md"), None),
    ],
}

formate = {}
for schluessel, quellen in FORMATE.items():
    teile = []
    for quelle, titel in quellen:
        if not quelle:
            continue
        teile.append(saeubern(abschnitte(quelle, titel) if titel else quelle))
    roh = "\n\n".join(x for x in teile if x)
    for name in FREMDE_NAMEN:
        roh = re.sub(r"\b" + re.escape(name) + r"s\s+(\w+)", r"\1 " + ERSATZ, roh)
        roh = re.sub(r"\b" + re.escape(name) + r"\w*", ERSATZ, roh)
    uebrig = [n for n in FREMDE_NAMEN if re.search(r"\b" + re.escape(n) + r"\w*", roh)]
    if uebrig:
        print("ABBRUCH — fremde Namen im Format " + schluessel + ":", uebrig)
        sys.exit(1)
    formate[schluessel] = roh

daten = {
    "stand": __import__("datetime").date.today().isoformat(),
    "quellen": sorted({q for _, _, q in BAUSTEINE}),
    "bausteine": [t for t, _, _ in BAUSTEINE],
    "zeichen": len(text),
    "text": text,
    "formate": formate,
}

os.makedirs(ZIEL, exist_ok=True)
pfad = os.path.join(ZIEL, "wissen-voll.json")
io.open(pfad, "w", encoding="utf-8", newline="\n").write(
    json.dumps(daten, ensure_ascii=False, indent=1))

print("Gebaut:", pfad)
print("Bausteine:", len(BAUSTEINE))
for t, i, q in BAUSTEINE:
    print("  -", t, "(" + str(len(i)) + " Zeichen, aus " + os.path.basename(q) + ")")
print("Gesamt:", len(text), "Zeichen")
print("Wissen je Format:")
for k in sorted(formate):
    print("  -", k, len(formate[k]), "Zeichen")
if len(text) > 200000:
    print("WARNUNG: ueber 200'000 Zeichen — ein Dokument fasst 256 KB.")
