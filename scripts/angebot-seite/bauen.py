"""Baut die Seite „Angebot auf Knopfdruck“ — die Seitenfassung von /angebot.

Patricia, 27.10.2026: „ne nicht als skill sondern als seite. so wie es julia gemacht hat“.

Die Seite fragt Claude über die Artifact-Fähigkeit `sample`. Eine Artifact-Seite
kommt aber nicht an `context/` — deshalb wird das Markenwissen hier aus dem
erzeugten Brief `wissen-voll.json` (scripts/cockpit/wissen-bauen.py) in die Seite
gelegt, aufgeteilt in zwei Teile:

  allgemein — Stimme, Kern-Schmerz, doTERRA-Schmerzen, Caption, Job-Säulen,
              verbotene Sprache, was wirkt, Stichwörter, laufende Angebote
  hooks     — der ganze Hook-Werkzeugkasten (geht nur bei Storys, Feed und
              Anzeigen mit, sonst schleppt jeder Baustein 76'000 Zeichen mit)
  gehirn    — die 13 Themenbücher aus den Kurs-Transkripten als Einzelpunkte;
              die Seite sucht je Baustein die passenden heraus (seit 29.10.2026)

🚨 Der Hook-Teil enthält zugekauftes Material, und das Repo ist öffentlich.
   Die fertige Seite liegt deshalb in einem gitignored Ordner und wird nur
   privat veröffentlicht — nie teilen.

Ablauf:
  python scripts/cockpit/wissen-bauen.py outputs/cockpit/abgleich   # Brief frisch
  python scripts/angebot-seite/bauen.py                             # Seite bauen
  dann: Artifact publish outputs/angebot-knopfdruck/angebot.html,
        capabilities {"sample": {}, "downloads": true}
"""
import json
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
QUELLE = ROOT / "outputs" / "cockpit" / "abgleich" / "wissen-voll.json"
VORLAGE = pathlib.Path(__file__).with_name("vorlage.html")
ZIEL = ROOT / "outputs" / "angebot-knopfdruck" / "angebot.html"
TEST = ROOT / "outputs" / "angebot-knopfdruck" / "test.html"

HOOK_TITEL = "ALLES ZUM HOOK"
THEMEN = ROOT / "reference" / "julia-trost" / "learnings" / "themen"
# Kapitel, die keine Regeln tragen: Dateilisten und offene Lücken.
SKIP = re.compile(r"^(Vorlagen und Unterlagen|Lücken|Widersprüche)")

# Was in keinem der Quell-Bausteine so klar steht und für ein Angebotspaket
# entscheidet. Jede Zeile stammt aus CLAUDE.md oder dem Gedächtnis — nichts neu.
REGELN = """== REGELN FÜR JEDES ANGEBOTSPAKET ==
- Preis-Kette: Bump günstiger als das Hauptprodukt. Upsell teurer als der Bump, aber günstiger als das Hauptprodukt. Downsell günstiger als das Upsell. Jede Zahl mit Rechnung.
- Minikurse kosten fix 39 CHF. Grosse Kurse bisher 333 CHF. Bei einem grossen Angebot (Kurs, 1:1, Gruppe) gilt der Preis aus dem Bauplan, auch wenn er von 333 abweicht. Die Mum Business Academy (MBA) ist das Endprodukt aller Funnels (997, regulär 1347).
- Keine Geld-zurück-Garantie. Nie.
- Kurse werden über die Veränderung verkauft, nie über Modul-, Kapitel-, Lektions- oder Call-Zahlen. Im Kursaufbau stehen Module, in Verkaufstexten nicht.
- Nichts erfinden: keine Kundinnen-Stimme, keine Zahl, kein Ergebnis, keine Alltagsszene, die nicht in den Angaben steht. Wo etwas fehlt, steht „✏️ PLATZ: …“ mit einer kurzen Anweisung, was dort hingehört.
- Zwei Zielgruppen-Ebenen: Patricias Kundinnen sind Mamas (Network, eigenes Business). Deren Kundschaft ist NICHT weiblich — dort heisst es Kundschaft, Leute, Interessenten, nie „deine Kundin“.
- Schweizer Schreibweise: ss statt ß, echte Umlaute, Franken/CHF.
- Freundin-Stimme, ganze Sätze, kein Stakkato, keine KI-Floskeln, keine fremden Mentorinnen-Namen.
- Die Bestätigungsmail eines Freebies hat einen einzigen Job: den Klick. Kein Angebot darin. Verkauft wird auf der Danke-Seite („nur hier“-Preis) und danach in den Mails.
- Der Pitch kommt erst, wenn das vorherige Produkt ein neues Problem geschaffen hat.
- Anzeigen verlinken immer auf mumlifebalance.ch/<seite>, nie direkt auf die Kasse.
- Nie das Werkzeug im Hook („niemand wacht auf und denkt: ich sollte KI nutzen“). Das Stichwort steht nur am Schluss.
"""


def teile(text):
    """Teilt den Brief an seinen `== TITEL ==`-Zeilen."""
    stuecke = re.split(r"(?m)^(?===+ ?.+? ?==+\s*$)", text)
    allgemein, hooks = [], ""
    for s in stuecke:
        if not s.strip():
            continue
        if s.lstrip("= ").startswith(HOOK_TITEL):
            hooks = s.strip()
        else:
            allgemein.append(s.strip())
    return "\n\n".join(allgemein), hooks


def gehirn():
    """Die 13 Themenbücher aus den Kurs-Transkripten als Nachschlagewerk.

    Patricia, 29.10.2026: „ich habe ja das ganze julia wissen aus den kursen
    transkribiert und will das als gehirn mit meinen transkribtionen dahinter setzen“.
    Zusammen rund 4,8 MB — zu viel für einen Auftrag. Deshalb liegt jeder Punkt
    einzeln in der Seite, und die Seite sucht je Baustein die passenden heraus
    (`fachwissen()` in der Vorlage). Die Fundstelle hinter „ — “ fällt weg, sie
    braucht nur, wer im Workspace nachschlägt.
    """
    buecher, abschnitte, punkte = [], [], []
    for pfad in sorted(THEMEN.glob("*.md")):
        text = pfad.read_text(encoding="utf-8")
        titel = re.search(r"(?m)^# (.+?)(?: — alle Learnings)?\s*$", text)
        kern, abschnitt, h2 = [], -1, ""
        im_kern = False
        for z in text.splitlines():
            if z.startswith("## "):
                h2 = z[3:].strip()
                im_kern = h2.startswith("Das Wichtigste")
                if not im_kern and not SKIP.search(h2):
                    abschnitte.append(h2); abschnitt = len(abschnitte) - 1
                else:
                    abschnitt = -1
                continue
            if z.startswith("### ") and abschnitt >= 0:
                abschnitte.append(h2 + " · " + z[4:].strip()); abschnitt = len(abschnitte) - 1
                continue
            if im_kern:
                kern.append(z)
                continue
            if abschnitt < 0 or not re.match(r"\s*[-*] ", z):
                continue
            t = re.sub(r"^\s*[-*] ", "", z)
            # Fundstelle ab — nur wenn der Schwanz wie eine aussieht (Datei, Kurs: Lektion, Seite),
            # sonst ginge ein Gedankenstrich mitten im Satz mit.
            t = re.sub(r" — ([^—]{3,300})$",
                       lambda m: "" if re.search(r"\.txt|\.pdf|:|S\. ?\d|\d\d:\d\d", m.group(1)) else m.group(0), t).strip()
            if len(t) > 25:
                punkte.append([len(buecher), abschnitt, t])
        buecher.append({"id": pfad.stem, "titel": titel.group(1) if titel else pfad.stem,
                        "kern": "\n".join(kern).strip()})
    assert len(buecher) >= 13, "🚨 Themenbücher fehlen: %d" % len(buecher)
    return {"buecher": buecher, "abschnitte": abschnitte, "punkte": punkte}


def main():
    d = json.loads(QUELLE.read_text(encoding="utf-8"))
    allgemein, hooks = teile(d["text"])
    assert hooks, "🚨 Hook-Teil im Brief nicht gefunden"
    assert "ANGEBOTE, DIE GERADE LAUFEN" in allgemein, "🚨 Angebote fehlen im Brief"

    g = gehirn()
    wissen = {"stand": d.get("stand", ""), "allgemein": REGELN + "\n\n" + allgemein, "hooks": hooks, "gehirn": g}
    roh = json.dumps(wissen, ensure_ascii=False)
    # </script> im Text würde den Datenblock vorzeitig schliessen.
    roh = roh.replace("</", "<\\/")

    vorlage = VORLAGE.read_text(encoding="utf-8")
    assert vorlage.count("/*WISSEN*/") == 1, "🚨 Platzhalter /*WISSEN*/ fehlt oder doppelt"
    seite = vorlage.replace("/*WISSEN*/", roh)

    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    ZIEL.write_text(seite, encoding="utf-8")
    # Lokale Prüffassung: der Artifact-Rahmen setzt Doctype und Viewport selbst.
    TEST.write_text('<!doctype html><html><head><meta charset="utf-8">'
                    '<meta name="viewport" content="width=device-width,initial-scale=1">'
                    '</head><body>' + seite + "</body></html>", encoding="utf-8")

    kb = len(seite.encode("utf-8")) // 1024
    print("Allgemein %d Zeichen · Hooks %d Zeichen · Gehirn %d Bücher, %d Kapitel, %d Punkte · Seite %d KB"
          % (len(wissen["allgemein"]), len(hooks), len(g["buecher"]), len(g["abschnitte"]), len(g["punkte"]), kb))
    assert kb < 15000, "🚨 Seite über 15 MB"
    print("Geschrieben:", ZIEL.relative_to(ROOT))
    print('Danach: Artifact publish, capabilities {"sample": {}, "downloads": true}')


if __name__ == "__main__":
    main()
