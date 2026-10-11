# -*- coding: utf-8 -*-
"""Gibt dem Content-Studio im Cockpit die Hook-Mechanik mit (14.09.2026).

Warum es nötig ist: Das Content-Studio läuft IN der Artifact-Seite. Eine Seite kommt
nicht an den Workspace, also auch nicht an `.claude/skills/hooks/SKILL.md`. Bisher
bestand sein ganzes Wissen aus den sieben Feldern unter „Mein Wissen" — Ton und
Zielgruppe, aber keine Hook-Regeln und keine Qualitätsabnahme.

Was hier hineinkommt: die Mechanik in Patricias Worten — Bewusstseinsstufen, Angles,
der letzte Check, der Beitrags-Check. **Nicht** die Formel-Kataloge und Beispiele aus
den zugekauften Kursen; die bleiben im Skill, der aus gutem Grund nicht im Repo liegt.

🚨 Wenn sich der Hook-Skill ändert, muss diese Fassung nachgezogen werden. Sie ist eine
Abschrift, keine Verbindung.

Wiederholbares Skript — schon Gesetztes wird übersprungen.
"""
import io, os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PFAD = "outputs/cockpit/mlb-cockpit.html"

HOOKREGELN = '''  /* Die Hook-Mechanik. Abschrift aus dem Hook-Skill, weil eine Artifact-Seite
     nicht an die Dateien im Workspace kommt. Aendert sich der Skill, gehoert das
     hier nachgezogen. */
  var HOOKREGELN = [
    "HOOK-MECHANIK",
    "",
    "Reihenfolge der Hebel: Wen du ansprichst schlaegt das Thema, das Thema schlaegt die",
    "Formulierung. Ein guter Hook auf dem falschen Thema rettet nichts.",
    "",
    "Bewusstseinsstufen — wen der Hook gerade abholt:",
    "1 unbewusst: spuert nichts Konkretes. Szene aus dem Leben, kurz und bildhaft.",
    "2 problembewusst: spuert den Schmerz, kennt keinen Weg. Ihr eigener Gedanke, woertlich.",
    "3 loesungsbewusst: kennt Wege, weiss nicht welchen. Warum ausgerechnet so.",
    "4 angebotsbewusst: kennt Patricia, zoegert. Einwand aufgreifen, Beweis zeigen.",
    "5 kaufbereit: will nur den Anstoss. Angebot und echter Anlass.",
    "In der Praxis: Reichweiten-Beitraege auf Stufe 1 bis 2 — der Hook stellt IHRE Frage",
    "und gibt nicht schon Patricias Antwort. Lead-Beitraege mit Kommentar-Stichwort auf",
    "Stufe 2 bis 3. Erst Stories, Mails und Launch duerfen auf 4 bis 5.",
    "Pruefsatz: \\u201eMeine Posts funktionieren nicht\\u201c ist schon Stufe 3. Stufe 2 klingt nach",
    "\\u201eich stecke so viel rein und es kommt nichts zurueck\\u201c.",
    "",
    "Angles — aus welcher Richtung geschaut wird. Nicht zu verwechseln mit der Formel:",
    "die Formel sagt, wie ein Hook KLINGT, der Angle sagt, worauf er ZIELT.",
    "Schmerz (der Zustand, wie er sich anfuehlt) · Ergebnis (wie es aussieht, wenn es",
    "geloest ist) · Beweis (was andere erlebt haben) · Kontraer (die verbreitete Annahme",
    "stimmt nicht) · Identitaet (fuer genau die, die ...) · Neugier (der uebersehene Hebel) ·",
    "Vergleich (anders als der uebliche Weg).",
    "Regel: ueber ein Set von Hooks mindestens DREI verschiedene Angles mischen. Zehn Hooks",
    "koennen formal bunt sein und trotzdem alle denselben Nerv treffen — wen der erste nicht",
    "abholt, den holt auch der zehnte nicht ab.",
    "",
    "Laenge: kurz. Die erste Zeile muss allein ziehen, bevor jemand auf Mehr anzeigen tippt.",
    "",
    "DER LETZTE CHECK — vier Fragen, bevor ein Hook stehen bleibt.",
    "Eine einzige Frage mit Nein, und der Hook wird neu geschrieben. Nie die Caption",
    "nachbessern, um einen schwachen Hook zu retten.",
    "1. Trifft es wirklich einen Schmerz? Nicht \\u201esie wuerde zustimmen\\u201c, sondern es trifft.",
    "   Benenne den Schmerz woertlich. Wenn du keinen benennen kannst, ist es kein Hook,",
    "   sondern eine Aussage.",
    "2. Denkt sie \\u201ekrass, wieso weiss die, was ich denke\\u201c? Das ist die Latte — nicht",
    "   \\u201einteressant\\u201c, nicht \\u201eguter Punkt\\u201c. Zustimmung ist kein Stopp.",
    "   Test: Hat diese Frau das gestern Abend wirklich gedacht?",
    "3. Wuerdest du das so am Kuechentisch zu einer Freundin sagen?",
    "4. Ist die Loesung draussen? Die Loesung kommt nie im Hook. Der Hook stellt ihre Frage.",
    "",
    "DER BEITRAGS-CHECK — vier Fragen fuer den ganzen Beitrag.",
    "Beruehrt es. Nimmt sie etwas Konkretes mit. Warum sollte sie das speichern oder",
    "weiterschicken. Warum sollte sie kommentieren.",
    "Hintergrund: Patricias Engagement lag bei 0,3 bis 0,5 Prozent, der Richtwert ist 1 bis 3.",
    "Der Befund war: zu nuechtern und zu abstrakt — weder beruehrt noch konkret weitergeholfen.",
    "",
    "CTA nach der 3+1-Regel: drei Reichweiten-Beitraege mit Teilen-Aufruf, einer als",
    "Lead-Beitrag mit Kommentar-Stichwort. Reichweiten-Beitraege nie mit Verkauf ueberladen."
  ].join("\\n");

'''

t = io.open(PFAD, encoding="utf-8").read()
vorher = t
getan, schon = [], []

# 1) Die Regeln in die Seite legen, direkt vor wissenText()
anker = "  function wissenText() {"
if "var HOOKREGELN" not in t:
    assert anker in t, "Anker wissenText() nicht gefunden"
    t = t.replace(anker, HOOKREGELN + anker)
    getan.append("Hook-Mechanik in die Seite gelegt")
else:
    schon.append("Hook-Mechanik war schon drin")

# 2) In den Wissenstext aufnehmen — damit sie bei JEDEM Auftrag mitgeht
alt = '    teile.push("PIE:\\nJeder Beitrag ist Persönlichkeit, Inspiration oder Expertise.");\n    return teile.join("\\n\\n");'
neu = ('    teile.push("PIE:\\nJeder Beitrag ist Persönlichkeit, Inspiration oder Expertise.");\n'
       '    teile.push(HOOKREGELN);\n'
       '    return teile.join("\\n\\n");')
if alt in t:
    t = t.replace(alt, neu)
    getan.append("Hook-Mechanik geht bei jedem Auftrag mit")
else:
    schon.append("Hook-Mechanik war schon im Wissenstext")

# 3) Im Content-Studio ausdruecklich abnehmen lassen
alt = ('      "\\n\\nHalte dich streng an Ton, Hookregeln und Verbote. Schreibe so, dass es nach ihr klingt und nicht nach Marketingtext.\\n\\n" +')
neu = ('      "\\n\\nHalte dich streng an Ton, Hookregeln und Verbote. Schreibe so, dass es nach ihr klingt und nicht nach Marketingtext.\\n" +\n'
       '      "Bevor du antwortest: geh die vier Fragen vom letzten Check und die vier vom Beitrags-Check durch. " +\n'
       '      "Was eine davon nicht besteht, schreibst du neu, statt es abzuliefern.\\n\\n" +')
if alt in t:
    t = t.replace(alt, neu)
    getan.append("Content-Studio nimmt jeden Entwurf selbst ab")
else:
    schon.append("Abnahme war schon gesetzt")

if t != vorher:
    io.open(PFAD, "w", encoding="utf-8", newline="\n").write(t)

print("Geaendert:")
for z in getan:
    print("  +", z)
if schon:
    print("Schon so:")
    for z in schon:
        print("  =", z)
if not getan:
    print("  (nichts zu tun)")
