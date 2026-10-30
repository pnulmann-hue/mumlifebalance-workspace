---
tags: [plan, cockpit, automation]
---

# Freigabe ohne Laptop — Cockpit freigeben, eingeplant wird in der Cloud

## 1 · Worum es geht

Patricia gibt Beiträge weiter **im Cockpit** frei, so wie bisher (ihr Entscheid, 30.10.2026).
Neu ist, dass das Einplanen bei Blotato auch dann passiert, wenn ihr Laptop aus ist.
Dazu kommt ein Telegram-Bot: Er meldet, was eingeplant wurde. Schreibt sie ihm
„Caption kürzer“, schreibt Claude die Caption um, zeigt sie neu und plant erst nach ihrem „passt“.

Formate: **Karussells und Sprechreels**, wie heute. B-Roll und Storys postet sie weiter selbst.

## 2 · Warum

- Der Einplan-Lauf `freigaben-einplanen-2000` ist ein Scheduled Task der Desktop-App.
  Er läuft nur, wenn die App auf dem Laptop offen ist.
- Vom 10. bis 16.10. und vom 26. bis 29.10. hing er. Zwei Karussells standen zwei Wochen auf „wartet“.
- Anlass ist Julias Workshop vom 29.10.: Dort chattet ihre Mitarbeiterin über Telegram mit Claude,
  auch wenn ihr Laptop aus ist.

## 3 · Der Knackpunkt zuerst

Die Freigaben liegen in der **Datenbank des Cockpits** (Artifact). Ein gewöhnlicher Server
kommt nicht hinein. Auch das Cockpit selbst kann keinen fremden Server anrufen.
Hinein kommt nur Claude.

Die Lösung wäre deshalb ein **Cloud-Auftrag von Claude Code** (Routine, läuft bei Anthropic
nach Zeitplan, ohne Laptop). Ob ein solcher Lauf an die Artifact-Datenbank kommt, ist **nicht
belegt**. Schritt 1 ist darum ein Test. Fällt er negativ aus, wird der Plan neu vorgelegt
(siehe Rückfallweg unten), und es wird nicht weitergebaut.

## 4 · Die Schritte

**Teil A — geht es überhaupt?**

> **Ergebnis Test 30.10.2026** (Routine `trig_0165cW7BmvhXXUiFqJDCtKUV`, Umgebung „Default“, Sonnet 5.5, 38 s):
> - ✅ **Die Cockpit-Datenbank ist aus der Cloud lesbar.** `ArtifactData list freigaben` lieferte 42 Dokumente: geplant 12 · selber-posten 17 · zurückgezogen 7 · fehlgeschlagen 3 · wartet 2 · gepostet-von-hand 1.
> - ❌ **Das Netz nach aussen ist gesperrt.** Blotato, mumlifebalance.ch und Telegram brachen alle ab mit `CONNECT tunnel failed, response 403`. Die Standard-Umgebung lässt nur freigegebene Adressen durch.
> - ➜ **Nächster Schritt:** In den Einstellungen der Cloud-Umgebung (claude.ai/code → Umgebung) den Netzzugang für `backend.blotato.com`, `mumlifebalance.ch` und `api.telegram.org` freigeben. Am besten in einer eigenen Umgebung, nicht in „Default“. Danach den Netztest wiederholen.
> - Das Klonen des Repos dauert rund 90 Sekunden je Lauf.

1. [x] Eine Test-Routine in der Cloud anlegen. Sie liest nur `freigaben` aus dem Cockpit und meldet die Anzahl per Telegram. Schreiben und Einplanen gibt es dabei nicht.
2. [~] Prüfen, was die Cloud-Umgebung kann (Repo ✅, Netz ❌, Geheimwerte offen): Repo aus GitHub (`main`), geheime Werte als Umgebungsvariablen, Netz zu Blotato, WordPress und Telegram.
3. [ ] **Entscheidungspunkt.** Patricia bekommt das Ergebnis. Bei einem Nein geht es mit dem Rückfallweg weiter.

**Teil B — Einplanen in der Cloud**
4. [ ] `freigabe-zu-blotato.mjs` und `freigabe-nachruecken.py` sollen die Zugangsdaten zusätzlich aus Umgebungsvariablen lesen. Heute lesen sie sie nur aus `.env`-Dateien, die es in der Cloud nicht gibt. Im Code steht dabei kein Schlüssel.
5. [ ] Die Werte für Blotato, das WordPress-App-Passwort und Telegram als Geheimwerte der Cloud-Umgebung hinterlegen. Das macht Patricia selbst, nie im Chat.
6. [ ] Der Auftrag der Routine ist der Auftrag des heutigen 20:00-Tasks. Er wird nicht neu geschrieben, sondern übernommen: Freigaben auf `wartet` lesen, nachrücken, erst trocken, dann einplanen, `freigaben` zurückschreiben, Telegram melden.
7. [ ] Den Takt festlegen, zum Beispiel alle zwei Stunden von 08:00 bis 22:00. Damit verfällt auch kein Zeitpunkt mehr, weil man um zehn freigegeben hat.
8. [ ] Den Laptop-Task `freigaben-einplanen-2000` abschalten, **erst nachdem** die Cloud-Routine zweimal sauber gelaufen ist. Laufen beide gleichzeitig, wird doppelt gepostet.

**Teil C — der Telegram-Rückkanal**
9. [ ] Einen kleinen Dienst auf Vercel bauen, der Telegram-Nachrichten annimmt und in eine Warteschlange legt. Dafür reicht eine einzige Tabelle in der Supabase, die es für den Kochbot schon gibt. Der Dienst selbst plant nichts ein und kommt nicht an das Cockpit.
10. [ ] Die Routine liest bei jedem Lauf die Warteschlange. Eine Änderung („Caption kürzer“) landet im bestehenden Feld `kommentar` am Beitrag. Damit greift dieselbe Mechanik wie bei der Kommentarzeile, und es entsteht keine zweite.
11. [ ] Claude arbeitet die Änderung ein und schickt die neue Caption per Telegram. Der Beitrag wartet, bis Patricia „passt“ antwortet. Geplant wird erst danach.
12. [ ] Eine Sicherung gegen falsche Absender: Der Dienst nimmt nur Nachrichten aus Patricias Chat-ID an.

**Teil D — nachziehen**
13. [ ] CLAUDE.md: Die Abschnitte „Cockpit-Artifact — Content-Pipeline“ und „Version 102“ beschreiben den 20:00-Task und gehören angepasst.
14. [ ] `reference/scheduled-task-kommentare.md` und der Auftrag des 19:30-Tasks: Klären, ob die Kommentare künftig ebenfalls in der Cloud laufen. Der Vorschlag ist ja, weil sonst nur die Hälfte ohne Laptop geht.

## 5 · Woran wir merken, dass es fertig ist

- **Gegenprobe, die anschlagen muss:** Der Laptop ist aus, Patricia gibt am Handy ein Karussell frei, und zur nächsten vollen Runde steht es bei Blotato eingeplant. Die Telegram-Meldung kommt mit Datum und Uhrzeit.
- **Gegenprobe, die nicht anschlagen darf:** Ein B-Roll oder eine Story mit Freigabe wird **nicht** eingeplant. Ein schon eingeplanter Beitrag wird beim nächsten Lauf nicht ein zweites Mal eingeplant.
- Patricia schreibt „Caption kürzer“, bekommt die neue Fassung aufs Handy und erst nach „passt“ die Bestätigung, dass er eingeplant ist.
- Eine Nachricht aus einem fremden Chat bewirkt nichts.

## 6 · Bewusst nicht dabei

- Freigeben über Telegram: Die Freigabe bleibt im Cockpit.
- Der Freitags-Content-Lauf in der Cloud: Er braucht lokale Videos und gitignorte Dateien und bleibt deshalb vorerst auf dem Laptop.
- B-Roll und Storys einplanen.
- Den alten Cockpit-Bot auf Railway wiederbeleben. Er bleibt aus.

## 7 · Rückfallweg, falls die Cloud nicht an die Cockpit-Datenbank kommt

Dann muss die Freigabe an einen Ort, an den ein Server kommt. Die naheliegende Lösung: Der Freitags-Lauf legt jeden fertigen Beitrag zusätzlich in die Supabase-Tabelle. Freigegeben würde dann über Telegram, also anders, als Patricia es gewählt hat. Deshalb wird dieser Weg nur nach ihrem neuen Ja gebaut.

## 8 · Was es berührt

| Stelle | Was |
|---|---|
| `scripts/cockpit/freigabe-zu-blotato.mjs` | Zugangsdaten auch aus Umgebungsvariablen |
| `scripts/cockpit/freigabe-nachruecken.py` | dasselbe, falls es Zugänge liest |
| Scheduled Task `freigaben-einplanen-2000` | wird nach dem Umzug abgeschaltet |
| Scheduled Task `kommentare-einarbeiten` | Umzug klären (Schritt 14) |
| Cockpit (`outputs/cockpit/mlb-cockpit.html`) | keine Änderung nötig; der Text „wartet auf 20:00“ auf der Karte müsste angepasst werden |
| Supabase (Kochbot-Projekt) | eine neue Tabelle für die Telegram-Warteschlange |
| CLAUDE.md, Gedächtnis `project_cockpit-content-pipeline` | Beschreibung des Einplanens |

🚨 Die Zeitangabe „wartet auf 20:00“ steht an mehreren Stellen: auf der Cockpit-Karte, in CLAUDE.md und in der Task-Datei. Vor dem Ändern alle Stellen mit `grep` suchen.
