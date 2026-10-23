---
name: create-plan
description: "Schreibt vor dem Bauen auf, was gemacht werden soll — in Schritten, zum Gegenlesen. Dran bei /create-plan und bei allem, was grösser ist als ein einzelner Auftrag."
---

# /create-plan — erst aufschreiben, dann bauen

**Ziel:** Bei allem, was grösser ist als ein einzelner Auftrag, steht vorher auf
Papier, was entstehen soll. Patricia liest es und sagt, was daran nicht stimmt.

🚨 **Die Herkunft:** Die Idee eines Plan-Befehls vor dem Bauen stammt aus der
Ordner-Vorlage von Julias Claude-Kurs. Der Text hier ist auf diesen Workspace
geschrieben. Die entschlackte Fassung für den KI-Kurs liegt in
`scripts/ki-kurs/grundgeruest-bauen.py` (Konstante `PLAN`) — **beide müssen
dasselbe sagen**, sonst zeigt der Kurs etwas anderes, als Patricia selbst nutzt.

## Schritt 1 · Frag nach, was fehlt

Bevor etwas aufgeschrieben wird: die nötigen Fragen stellen, eine nach der
anderen. Lieber drei Fragen jetzt als ein Plan, der am Ziel vorbeigeht.

Dazu lesen, was im Workspace schon dazu existiert — `CLAUDE.md`, der passende
Abschnitt in `context/`, vorhandene Dateien. **Ein Plan, der etwas neu anlegt,
was es schon gibt, ist der häufigste Fehler** (siehe Gedächtnis
`feedback_KRITISCH-eine-sache-eine-datei`).

## Schritt 2 · Schreib den Plan

Als Datei in `plans/`, benannt nach Datum und Vorhaben:
`2026-10-22-mein-vorhaben.md`. Mit Frontmatter-Tags nach der
Obsidian-Konvention. Hinein gehören:

1. **Worum es geht** — in drei Sätzen, in Patricias Worten
2. **Warum** — welches Problem das löst, und woran man das heute merkt
3. **Die Schritte** — nummeriert, jeder einzeln abhakbar
4. **Woran wir merken, dass es fertig ist** — nachprüfbar, nicht „fühlt sich
   gut an". Wo möglich eine Gegenprobe, die anschlagen muss, und eine, die
   nicht anschlagen darf
5. **Was bewusst nicht dazugehört** — damit es unterwegs nicht grösser wird
6. **Was es berührt** — welche bestehenden Dateien, Skripte oder Artifacts
   mitgeändert werden müssen

## Schritt 3 · Leg ihn vor

Den Plan zeigen und fragen, was daran nicht stimmt. **Noch nichts bauen.**
Erst nach ihrem Ja geht es mit `/implement` weiter.

🚨 Bei einem Vorhaben, das CLAUDE.md, einen Skill oder ein Artifact ändert,
gehört in den Plan, **welche Stelle sonst noch dasselbe sagt** — ein Termin, ein
Preis oder eine Regel steht in diesem Workspace selten nur an einer Stelle
(siehe `feedback_KRITISCH-termin-aenderung-alle-stellen`).
