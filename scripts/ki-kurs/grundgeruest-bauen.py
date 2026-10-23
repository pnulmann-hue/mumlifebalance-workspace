#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Baut das Arbeitsplatz-Grundgerüst, das im KI-Kurs unter Lektion 4.3 liegt.

    python scripts/ki-kurs/grundgeruest-bauen.py

Ergebnis: outputs/produkte/ki-treppe/grundgeruest/Mein-Business/
Patricia lädt den Ordner in die Kursplattform hoch (Download-Reiter).

🚨 Hier kommt NUR hinein, was weitergegeben werden darf:

* Die fünf Ordner mit je einer Liesmich-Datei.
* Eine leere CLAUDE.md zum Ausfüllen (aus der Beilage).
* /start und /shutdown — die IDEE stammt aus einer Kursvorlage, der Text ist
  Patricias eigener. Hier stehen sie bewusst in einer entschlackten Fassung:
  ohne ihre Dateinamen, ohne Git, ohne ihre eigenen Vorfälle.

🚨 Was NICHT hineingehört und auch nie hineingehören wird:
  ihre echten Skills (zeigen auf ihre Datenbanken und Dateien), die
  zugekauften Skills (fremde Arbeit), alles aus context/ und outputs/.

Die Liesmich-Dateien sind bewusst kurz. Wer ein leeres Gerüst herunterlädt,
liest keine Handbücher — er will wissen, was in diesen Ordner gehört.
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WURZEL = Path(__file__).resolve().parents[2]
ZIEL = WURZEL / "outputs" / "produkte" / "ki-treppe" / "grundgeruest" / "Mein-Business"
BEILAGEN = WURZEL / "outputs" / "produkte" / "ki-treppe" / "beilagen"

ORDNER = {
    "context": """# context — dein Wissen

Hier liegt alles, was die KI über dich wissen soll.

## Das legst du jetzt hinein

Vier Dateien hast du in Kapitel 2 schon gebaut. Die kommen hierher — kopier sie
einfach in diesen Ordner:

| Was | Aus Lektion | Nenn es am besten |
|---|---|---|
| **Dein Business-Brief** — die sechs Bausteine | 2.3 | `business-brief.md` |
| **Was bei der Buch-Technik herauskam** | 2.4 | `über-mich.md` |
| **Deine Textproben** — die zwei, drei eigenen Texte | 2.5 | `meine-stimme.md` |
| **Deine Floskel-Liste** — was nie vorkommen darf | 2.2 | `verbotene-woerter.md` |

Wenn sie als Word-Datei oder PDF vorliegen, geht das auch. Schöner ist
Markdown (`.md`), aber lass dich davon nicht aufhalten — du kannst jederzeit
sagen: *„Mach aus dieser Datei eine Markdown-Datei."*

**Danach einmal fragen:** *„Lies alles in context und sag mir in drei Sätzen,
was du über mich weisst."*

Wenn sie dir deine eigene Positionierung zurückgibt, steht das Fundament.

## Was mit der Zeit dazukommt

Deine Angebote, deine Preise, deine Kundinnen-Geschichten — alles, was du sonst
jedes Mal neu erklären müsstest. Nicht auf Vorrat anlegen, sondern immer
dann, wenn dir auffällt, dass du es schon zum zweiten Mal getippt hast.

Faustregel: Was hier liegt, hast **du** geschrieben oder gesagt.
""",
    "outputs": """# outputs — was herauskommt

Alles, was die KI für dich herstellt: Texte, Pläne, Listen, fertige Dateien.

Leg dir Unterordner an, sobald es unübersichtlich wird — nach Monat oder nach
Thema, wie du magst.

Faustregel: Was hier liegt, kann weg, ohne dass etwas kaputtgeht. Es lässt
sich jederzeit neu herstellen.
""",
    "reference": """# reference — Material zum Nachschlagen

Unterlagen, die du **nicht selbst geschrieben** hast und die du trotzdem
griffbereit haben willst: Kursnotizen, Anleitungen, Vorlagen.

Der Unterschied zu `context` ist der wichtigste im ganzen Arbeitsplatz:

* `context` = deins. Darf in deine Texte einfliessen.
* `reference` = von anderen. Zum Nachschlagen, nicht zum Abschreiben.

🚨 Sag der KI in deiner CLAUDE.md, dass sie aus `reference` nie wörtlich
abschreibt. Sonst landet fremder Text in deinen Captions.
""",
    "scripts": """# scripts — kleine Helfer

**Auch diesen Ordner füllst du nicht selbst.** Hier legt die KI kleine
Programme ab, die immer dasselbe tun.

## Woran du merkst, dass hier etwas hingehört

Etwas hat dich zum dritten Mal genervt, und es ist jedes Mal derselbe
Handgriff. Zum Beispiel:

* Bilder auf eine bestimmte Grösse bringen
* aus einer Liste jedes Mal dieselbe Tabelle machen
* alle Dateien in einem Ordner umbenennen

Dann sagst du, was passieren soll — und sie schreibt den Helfer. Du bedienst
ihn danach, indem du ihn nennst. Was darin steht, musst du nie lesen.

## Am Anfang ist dieser Ordner leer

Und das ist richtig so. Du füllst ihn nicht auf Vorrat. Jeder Helfer hier ist
aus einem echten Ärgernis entstanden, nicht aus einer guten Idee.

## Der Unterschied zu einem Befehl

Ein **Befehl** (wie `/start`) ist eine Anweisung an die KI — in Worten.
Ein **Helfer** hier ist ein kleines Programm, das von selbst rechnet. Für
alles, was mit Text und Entscheiden zu tun hat, nimmst du einen Befehl. Für
alles, was stur dasselbe macht, einen Helfer.
""",
    "plans": """# plans — was du vorhast

**Diesen Ordner füllst du nicht selbst.** Hier legt die KI ab, was sie vorhat —
bevor sie es baut.

## So entsteht ein Plan

Du hast etwas vor, das grösser ist als ein einzelner Auftrag: eine neue
Verkaufsseite, ein Bot, eine Umstellung in deinen Ordnern. Dann sagst du:

> *„/create-plan"* — und dazu in einem Satz, was du vorhast.

Sie fragt nach, was ihr fehlt, und schreibt danach eine Datei hierher. Darin
steht:

1. **worum es geht** — in drei Sätzen, in deinen Worten
2. **warum** — welches Problem das löst
3. **die Schritte** — nummeriert, einer nach dem anderen
4. **woran du merkst, dass es fertig ist**
5. **was bewusst nicht dazugehört** — damit es unterwegs nicht grösser wird

**Du liest den Plan und sagst, was daran nicht stimmt.** Gebaut wird erst
danach, mit `/implement`.

## Warum das den Umweg wert ist

Eine KI ohne Plan fängt dreimal von vorne an. Und du merkst erst nach einer
Stunde, dass sie etwas anderes gebaut hat, als du gemeint hast.

Zehn Minuten lesen sparen den halben Nachmittag. Und der Plan bleibt liegen —
in drei Wochen kannst du nachlesen, warum etwas so gebaut wurde.

## Was du hier NICHT ablegst

Einkaufslisten, To-dos, Notizen. Das ist kein Aufgaben-Ordner. Hier liegt nur,
was einen Bauplan braucht.
""",
}

LIESMICH = """# Dein Arbeitsplatz

Willkommen. Das hier ist ein leeres Gerüst — fünf Ordner, eine
Gedächtnis-Datei und vier Befehle. Mehr braucht es nicht für den Anfang.

## In drei Schritten startklar

**1 · Leg den Ordner an einen Platz, den du wiederfindest.**
Nicht in OneDrive, iCloud oder Dropbox. Warum, steht in Kapitel 10.

**2 · Füll die CLAUDE.md aus.**
Fünf Zeilen reichen. Sie wächst von selbst, sobald dich etwas zum dritten Mal
ärgert.

**3 · Leg dein Wissen aus Kapitel 2 in `context`.**
Vier Dateien hast du dort schon gebaut:

* deinen **Business-Brief** (2.3)
* was bei der **Buch-Technik** herauskam (2.4)
* deine **Textproben** (2.5)
* deine **Floskel-Liste** (2.2)

Einfach in den Ordner kopieren — die genaue Liste steht nochmal in
`context/LIESMICH.md`.

Dann frag einmal: *„Lies alles in context und sag mir in drei Sätzen, was du
über mich weisst."*

Wenn sie dir deine eigene Positionierung zurückgibt, läuft alles.

## Die vier Befehle

Zwei brauchst du ab dem ersten Tag:

| | |
|---|---|
| `/start` | am Anfang jeder Sitzung — sie schaut, was hier liegt und was zuletzt war |
| `/shutdown` | am Ende — sie räumt auf und schreibt mit, was dazugelernt wurde |

Du musst sie nicht benutzen. Aber wenn du es tust, musst du nie wieder
erklären, wo du stehst — und deine `CLAUDE.md` wächst von selbst mit, statt
dass du daran denken musst.

Zwei weitere, sobald ein Vorhaben grösser ist als ein Auftrag:

| | |
|---|---|
| `/create-plan` | sie schreibt auf, was sie vorhat, in Schritten — du liest es und sagst, was nicht stimmt |
| `/implement` | arbeitet den Plan ab, Schritt für Schritt, und hakt ihn dabei ab |

Der Plan bleibt als Datei in `plans/` liegen. Du kannst in drei Wochen
nachlesen, warum etwas so gebaut wurde.

## Damit nichts verloren geht

Dieser Ordner liegt auf deinem Rechner. Wenn der kaputtgeht, ist er weg —
genau wie Fotos, die nie gesichert wurden.

Dagegen gibt es **GitHub**: einen Ort im Netz, an dem dein Arbeitsplatz
zusätzlich liegt. Du kannst es dir vorstellen wie eine Cloud für Ordner, die
sich zusätzlich merkt, was sich wann geändert hat. Kaputtgegangenes lässt
sich damit zurückholen — auch eine Datei, die du vor drei Wochen versehentlich
überschrieben hast.

**Du brauchst es nicht, um loszulegen.** Richte es ein, sobald in diesem Ordner
etwas liegt, dessen Verlust dir wehtäte. Sag dann einfach:

> *„Ich will meinen Arbeitsplatz bei GitHub sichern. Erklär mir Schritt für
> Schritt, was ich tun muss — ich habe noch nie damit gearbeitet."*

🚨 **Eine Sache musst du dabei wissen:** Bei GitHub kannst du wählen zwischen
öffentlich und privat. **Öffentlich heisst wirklich öffentlich** — jeder im
Netz kann hineinschauen. Für deinen Arbeitsplatz nimmst du **privat**. Frag
ausdrücklich danach, und lass dir zeigen, wo das steht.

## Wenn etwas klemmt

Zeig ihr die Fehlermeldung im Wortlaut und frag, was sie bedeutet. Das ist
keine Ausrede — das ist der Handgriff, der dich durch den ganzen Kurs trägt.
"""

START = """---
name: start
description: "Beginnt die Sitzung: schaut, was im Arbeitsplatz liegt und was zuletzt passiert ist, fasst es kurz zusammen und fragt dann, woran heute gearbeitet wird."
---

# /start — die Sitzung beginnt

**Ziel:** In zwei Minuten weisst du, wo wir stehen — ohne dass ich es erklären
muss. Lesen, nicht nachfragen. Erst am Schluss eine einzige Frage.

## Schritt 1 · Was liegt hier?

Schau in `CLAUDE.md` und in `context/`. Das ist das Fundament: wer ich bin, wie
ich arbeite, was wo liegt.

Gibt es keine `CLAUDE.md` oder ist sie leer, sag das — und biete an, sie
gemeinsam auszufüllen. Alles andere baut darauf auf.

## Schritt 2 · Was war zuletzt?

Schau, welche Dateien in den letzten Tagen geändert wurden, vor allem in
`outputs/` und `plans/`. Daraus liest du ab, woran ich zuletzt gearbeitet habe.

Liegt in `plans/` etwas Angefangenes, nenn es — unfertige Pläne sind der
häufigste Grund, warum jemand den Faden verliert.

## Schritt 3 · Fass zusammen

Rund zehn Zeilen, nicht mehr:

* was gerade läuft
* was offen aussieht
* was du mir als Nächstes empfehlen würdest, und warum

🚨 **Keine Aufzählung von Dateinamen.** Ich will wissen, woran ich war, nicht
welche Dateien du gefunden hast.

## Schritt 4 · Frag

Genau eine Frage: **„Woran arbeiten wir heute?"**

Dann warte. Fang nichts an, bevor ich geantwortet habe.
"""

SHUTDOWN = """---
name: shutdown
description: "Beendet die Sitzung: räumt auf, schreibt neue Regeln ins Gedächtnis, berichtet kurz und verabschiedet sich."
---

# /shutdown — die Sitzung endet

Gegenstück zu `/start`. Die Schritte der Reihe nach, keinen überspringen.

## Schritt 1 · Was haben wir heute gemacht?

Geh das Gespräch durch und schreib eine kurze Liste: was neu dazugekommen ist,
was geändert wurde, was angefangen und nicht fertig geworden ist.

## Schritt 2 · Räum nur das Eindeutige weg

Zwischendateien aus dieser Sitzung, leere Ordner, Verschnitt.

🚨 **Alles andere bleibt liegen**, auch wenn es verwaist aussieht. Was weg
könnte, kommt als Frage in den Bericht. Löschen ist meine Entscheidung,
nicht deine.

## Schritt 3 · Zieh die CLAUDE.md nach

Frag dich bei allem, was heute passiert ist:

* Gibt es etwas Neues, das du beim nächsten Mal wissen musst?
* Habe ich dich heute korrigiert — und steht die Korrektur schon drin?
* Stimmt noch alles, was dort steht?

🚨 **Was ich dreimal korrigiert habe, gehört als Regel hinein.** Sonst
korrigiere ich es ein viertes Mal. Schreib es in meinen Worten, nicht in
deinen, und zeig mir die Zeile.

## Schritt 4 · Berichte

Kurz, in vier Teilen:

1. **Erledigt heute** — was wir gemeinsam geschafft haben
2. **Aktualisiert** — welche Dateien sich geändert haben
3. **Offen** — was du nicht allein entscheiden durftest
4. **Nächstes Mal** — womit es am sinnvollsten weitergeht

## Schritt 5 · Verabschiede dich

Kurz und freundlich, wie jemand, der Feierabend macht.
"""

PLAN = """---
name: create-plan
description: "Schreibt vor dem Bauen auf, was gemacht werden soll — in Schritten, zum Gegenlesen."
---

# /create-plan — erst aufschreiben, dann bauen

**Ziel:** Bei allem, was grösser ist als ein einzelner Auftrag, steht vorher
auf Papier, was entstehen soll. Du liest es und sagst, was daran nicht stimmt.

## Schritt 1 · Frag nach, was fehlt

Bevor du etwas aufschreibst: Stell die Fragen, die du brauchst, eine nach der
anderen. Lieber drei Fragen jetzt als ein Plan, der am Ziel vorbeigeht.

## Schritt 2 · Schreib den Plan

Als Datei in `plans/`, benannt nach dem Datum und dem Vorhaben
(`2026-10-22-mein-vorhaben.md`). Hinein gehören:

1. **Worum es geht** — in drei Sätzen, in meinen Worten
2. **Warum** — welches Problem das löst
3. **Die Schritte** — nummeriert, jeder einzeln abhakbar
4. **Woran ich merke, dass es fertig ist** — nachprüfbar, nicht „fühlt sich gut an"
5. **Was bewusst nicht dazugehört** — damit es nicht unterwegs grösser wird

## Schritt 3 · Leg ihn vor

Zeig mir den Plan und frag, was daran nicht stimmt. **Bau noch nichts.**
Erst wenn ich Ja sage, geht es mit `/implement` weiter.
"""

IMPLEMENT = """---
name: implement
description: "Arbeitet einen Plan aus plans/ Schritt für Schritt ab und hakt ihn dabei ab."
---

# /implement — den Plan abarbeiten

**Ziel:** Das umsetzen, was im Plan steht. Nicht mehr, nicht weniger.

## Schritt 1 · Lies den Plan

Wenn ich keinen genannt habe, nimm den neuesten in `plans/` und sag mir, welchen
du nimmst. Gibt es keinen, schlag `/create-plan` vor statt einfach anzufangen.

## Schritt 2 · Einen Schritt nach dem anderen

Nach jedem Schritt in einem Satz sagen, was gemacht wurde, und den Schritt im
Plan abhaken. So sehe ich jederzeit, wo wir stehen.

🚨 **Was nicht im Plan steht, wird nicht gebaut.** Fällt unterwegs etwas auf,
das fehlt, sag es — und frag, ob es dazukommen soll. Ein Plan, der unterwegs
wächst, ist kein Plan mehr.

## Schritt 3 · Prüf dein Ergebnis

Geh die Punkte aus „woran ich merke, dass es fertig ist" wirklich durch. Was
nicht stimmt, sagst du selbst, bevor ich es finde.

## Schritt 4 · Berichte

Was fertig ist, was offen blieb und warum. Dazu der nächste sinnvolle Schritt.
"""


def schreib(pfad: Path, text: str) -> None:
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_text(text, encoding="utf-8")


def main() -> None:
    # 🚨 Nicht den ganzen Zielordner löschen — falls Patricia dort etwas
    #    abgelegt hat, wäre es weg. Nur überschreiben, was dieses Skript baut.
    ZIEL.mkdir(parents=True, exist_ok=True)

    schreib(ZIEL / "LIESMICH.md", LIESMICH)
    schreib(ZIEL / ".claude" / "skills" / "start" / "SKILL.md", START)
    schreib(ZIEL / ".claude" / "skills" / "shutdown" / "SKILL.md", SHUTDOWN)
    schreib(ZIEL / ".claude" / "skills" / "create-plan" / "SKILL.md", PLAN)
    schreib(ZIEL / ".claude" / "skills" / "implement" / "SKILL.md", IMPLEMENT)

    for name, text in ORDNER.items():
        schreib(ZIEL / name / "LIESMICH.md", text)

    # Die CLAUDE.md kommt aus der Beilage — eine Quelle, nicht zwei.
    vorlage = BEILAGEN / "claude-md-vorlage.md"
    if vorlage.exists():
        roh = vorlage.read_text(encoding="utf-8")
        # Frontmatter der Beilage raus; im Arbeitsplatz hat es nichts verloren.
        if roh.startswith("---"):
            teile = roh.split("---", 2)
            roh = teile[2].lstrip() if len(teile) >= 3 else roh
        schreib(ZIEL / "CLAUDE.md", roh)
        quelle = "aus der Beilage"
    else:
        schreib(ZIEL / "CLAUDE.md", "# Mein Arbeitsplatz\n\n(hier fängst du an)\n")
        quelle = "PLATZHALTER — Beilage claude-md-vorlage.md fehlt"

    # Gegenprobe: nichts Privates, keine Schlüssel, kein fremder Name.
    import re
    verdacht = []
    for p in sorted(ZIEL.rglob("*.md")):
        t = p.read_text(encoding="utf-8")
        for muster, was in [
            (r"(?i)\bpatricia\b", "Name Patricia"),
            (r"(?i)\bjulia\w*", "fremder Name"),
            (r"(?i)api[_-]?key|secret|sk-[a-z0-9]{8}", "Schlüssel"),
            (r"[\w.+-]+@[\w-]+\.[a-z]{2,}", "Mailadresse"),
            (r"C:\\\\Users", "Pfad vom Rechner"),
            # 🚨 22.10.2026: Die LIESMICH lag mit „fuenf" und „Gedaechtnis" in
            #    den Downloads, die CLAUDE.md-Beilage daneben mit echten
            #    Umlauten. Echte ae/oe/ue-Woerter (bauen, dauert, neue) stehen
            #    bewusst nicht in der Liste — nach dem dritten Fehlalarm liest
            #    niemand mehr hin.
            (r"(?i)\b(fuenf|fuer|ueber|gedaechtnis|aergert|naechst\w*|"
             r"waechst|laeuft|laesst|raeumt|erklaer\w*|gehoert|oeffentlich|"
             r"zusaetzlich|woertlich|ausdruecklich|saetzen|plaene|geruest)\b",
             "umschriebener Umlaut"),
        ]:
            if re.search(muster, t):
                verdacht.append(p.relative_to(ZIEL).as_posix() + " — " + was)

    dateien = sorted(ZIEL.rglob("*"))
    print("Grundgerüst gebaut: " + ZIEL.relative_to(WURZEL).as_posix())
    print("  " + str(sum(1 for d in dateien if d.is_dir())) + " Ordner, "
          + str(sum(1 for d in dateien if d.is_file())) + " Dateien")
    print("  CLAUDE.md: " + quelle)
    if verdacht:
        print("\n  🚨 GEGENPROBE SCHLAEGT AN — das darf so nicht weitergegeben werden:")
        for v in verdacht:
            print("     " + v)
    else:
        print("  Gegenprobe: keine Namen, Schlüssel, Mailadressen oder eigenen Pfade.")

    # 🚨 Das ZIP gehört in denselben Lauf. Am 22.10.2026 lag in Downloads eine
    #    Fassung vom Vortag — zwei Befehle statt vier, umschriebene Umlaute —
    #    und sah genauso aktuell aus wie der gebaute Ordner.
    if "--zip" in sys.argv:
        import zipfile
        ziel = Path.home() / "Downloads" / "Mein-Business-Grundgeruest.zip"
        with zipfile.ZipFile(ziel, "w", zipfile.ZIP_DEFLATED) as z:
            for d in sorted(ZIEL.rglob("*")):
                z.write(d, "Mein-Business/" + d.relative_to(ZIEL).as_posix())
        print("  ZIP: " + str(ziel) + "  (" + str(ziel.stat().st_size // 1024) + " KB)")


if __name__ == "__main__":
    main()
