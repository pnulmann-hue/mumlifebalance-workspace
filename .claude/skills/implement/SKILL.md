---
name: implement
description: "Arbeitet einen Plan aus plans/ Schritt für Schritt ab und hakt ihn dabei ab. Dran bei /implement und bei „setz den Plan um“."
---

# /implement — den Plan abarbeiten

**Ziel:** Umsetzen, was im Plan steht. Nicht mehr, nicht weniger.

🚨 **Die Herkunft:** Die Idee stammt aus der Ordner-Vorlage von Julias
Claude-Kurs; der Text hier ist auf diesen Workspace geschrieben. Die
entschlackte Kursfassung liegt in `scripts/ki-kurs/grundgeruest-bauen.py`
(Konstante `IMPLEMENT`) — **beide müssen dasselbe sagen**.

## Schritt 1 · Lies den Plan

Hat Patricia keinen genannt, den neuesten in `plans/` nehmen und sagen, welcher
genommen wird. Gibt es keinen, `/create-plan` vorschlagen statt einfach
anzufangen.

## Schritt 2 · Einen Schritt nach dem anderen

Nach jedem Schritt in einem Satz sagen, was gemacht wurde, und den Schritt im
Plan abhaken. So ist jederzeit sichtbar, wo wir stehen.

🚨 **Was nicht im Plan steht, wird nicht gebaut.** Fällt unterwegs etwas auf,
das fehlt: sagen und fragen, ob es dazukommt. Ein Plan, der unterwegs wächst,
ist kein Plan mehr.

🚨 **Bestehende Dateien ändern, nicht neue danebenlegen.** Wenn ein Schritt eine
zweite Datei zum selben Thema erzeugen würde, ist der Plan an der Stelle falsch
— das vorher sagen.

## Schritt 3 · Prüf dein Ergebnis

Die Punkte aus „woran wir merken, dass es fertig ist" wirklich durchgehen, nicht
behaupten. Jede neue Prüfung an einem bekannt fehlerhaften Stand testen **und**
an einer Gegenprobe, die nicht anschlagen darf. Was nicht stimmt, selbst sagen,
bevor Patricia es findet.

Bei Bild- oder Video-Ausgaben zusätzlich die Visual-QA aus CLAUDE.md.

## Schritt 4 · Berichte

Was fertig ist, was offen blieb und warum. Dazu der nächste sinnvolle Schritt.
Wenn dabei etwas gelernt wurde, das beim nächsten Mal zählt: in CLAUDE.md oder
ins Gedächtnis, nicht nur in diese Antwort.
