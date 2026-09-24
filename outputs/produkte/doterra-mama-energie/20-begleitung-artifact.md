---
tags: [produkt, doterra, energieroutine, tools]
---

# Die Begleitung — das Artifact für die 30 Tage

**Stand:** 24.09.2026, Version 10 · **Für die Teilnehmerinnen**, nicht für Patricia.

**Adresse:** https://claude.ai/artifact/16dg1sYzwKdjvHhAqVpA7u

🚨 **Noch privat.** Teilnehmerinnen kommen erst rein, wenn Patricia über das
**Share-Menü** auf der Artifact-Seite freigibt. Das kann Claude nicht — vorher in
einem privaten Fenster testen.

---

## Was drin ist

| Reiter | Inhalt |
|---|---|
| **Heute** | Tagesimpuls · mitwachsende Checkliste · Krafttraining (3 Punkte je Woche) · „Was ist dir heute aufgefallen?" · Tagebuch der bisherigen Einträge |
| **Dein Plan** | 30-Tage-Gitter, füllt sich mit jedem Haken · die vier Wochen · je Woche drei Leseempfehlungen, die in die Bibliothek springen |
| **Rezepte** | **120** mit Suche und Mahlzeiten-Filter · **Portionsrechner** · **Protein-Tabelle** (33 Lebensmittel) |
| **Vorrat** | 35 Zeilen in 5 Gruppen, abhakbar, gestaffelt nach Woche |
| **Bibliothek** | **47 Artikel** in 8 Regalen, öffnen sich Tag für Tag — neu: „So nimmst du deine Nährstoffe“ (Tag 1, also schon vor dem Start offen) |

---

## 🚨 Die Führung ist der Kern

Patricias Vorgabe: *„ich will sie schritt für schritt durch den prozess führen. auch
mit den wissensunterlagen. jeden tag wird wieder was zugeschaltet."* — und dazu:
*„die rezepte sollten schon von anfang an drin sein."*

| | wann sichtbar |
|---|---|
| **Rezepte** | **alle 120 ab Tag 1** — hier wird nichts zurückgehalten |
| Haken Frühstück · Nährstoffe · Wasser | Woche 1 |
| Haken Schritte · Krafttraining | Woche 2 |
| Haken Abendritual | Woche 3 |
| Bibliotheks-Artikel | je nach `tag`, 1 bis 30 — **jeder Tag schaltet mindestens einen frei** |
| Vorrat Kühlschrank · Proteinquellen | Woche 1 |
| Vorrat Vorratsschrank · Gemüse | Woche 2 |
| Vorrat Tiefkühler | Woche 3 |

Verschlossene Artikel stehen sichtbar da („ab Tag 18") und lassen sich nicht
öffnen. Oben in der Bibliothek steht, warum — sonst wirkt ein Regal voller grauer
Zeilen am Tag 1 wie eine leere Seite statt wie etwas, auf das man sich freut.

---

## Der Starttag stellt sich selbst ein (seit 24.09.)

Wer in Monat M kauft, startet am 10. von M+1 (Bestellschluss Ende Vormonat), und den
Link bekommt sie gleich beim Kauf. Deshalb setzt die Seite beim **ersten Öffnen** den
**10. des nächsten Monats** und **hält ihn fest** (`enr.start`). Das Feld bleibt
veränderbar — nötig nur, wenn jemand den Link erst nach Monatsende öffnet.

🚨 **Version 7 hatte zwei Fehler, gefunden an Patricias Frage „am 12.10. dann den
10.11.?“:** Die Regel „bis zum 20. laufende Runde“ hätte eine Käuferin vom 15.9. in die
September-Runde gesetzt (Tag 6 am ersten Tag). Und der Starttag wurde **nicht
gespeichert**, sondern bei jedem Öffnen neu gerechnet — am 21.10. wäre er mitten in der
Runde auf den 10.11. gesprungen und alles wieder zu gewesen. Behoben in Version 8. **Vor dem Start** zeigt der Kopf „16 Tage
bis zum Start", der Impuls heisst „Bevor es losgeht", die Checkliste ist versteckt —
vorher hiess es „nimm heute deine Nährstoffe zum ersten Mal", obwohl das Paket noch
unterwegs sein kann.

🚨 **Die Seite zählt, aber sie stupst nicht an.** Ein Artifact schickt keine Nachricht —
den Anstoss gibt die Telegram-Gruppe.

**Knopf „Per Telegram an Patricia schicken"** unter der Tagesnotiz: `t.me/<name>?text=…`,
erscheint erst, wenn sie etwas eingetippt hat. `TELEGRAM = "mumlifebalance_patricia"`
in `inhalte.py` (angelegt 24.09., geprüft über t.me). Ist das Feld leer, fehlt der Knopf.

**Einnahme** (nur doTERRA-Produktblätter EU, Stand 2026): VMG+ 1 Sachet in 150–240 ml
kaltes Getränk · EO Mega+ **Softgel** 3 täglich zu einer Mahlzeit (das EU-Sachet ist
eine andere Form: 1 Sachet mit oder ohne Essen) · **PB Restore** Kapsel 1 täglich vor
einer Mahlzeit, nach dem Öffnen in den Kühlschrank. „Nüchtern" steht nirgends.
🚨 **Im Paket ist PB Restore, nicht PB Assist+** (Patricia, 24.09.) — sie nimmt es selbst,
und der „bei mir"-Frame trägt nur bei Produkten, die sie selbst nimmt. Ältere Unterlagen
(`06-produktpaket-21-tage.md`, `business-info.md`) nennen noch PB Assist+. Nichts aus der Ölschule-Akademie — fremdes, bezahltes Material.

## Wie es gebaut wird

```bash
python scripts/begleitung/cockpit-bauen.py
```

| Datei | Was drinsteht |
|---|---|
| `scripts/begleitung/cockpit-bauen.py` | die Seite: Markup, CSS, JS, Prüfungen |
| `scripts/begleitung/inhalte.py` | Wochen · Haken (`abWoche`) · Vorrat · Protein-Tabelle · Mengenwörter · Hinweis |
| `scripts/begleitung/bibliothek.py` | **46 Artikel** (je mit `tag`) und **30 Tagesimpulse** |
| `outputs/.../12-30-fruehstuecke.md` | 30 Frühstücke |
| `outputs/.../17-mittagessen.md` | 30 Mittagessen |
| `outputs/.../18-abendessen.md` | 30 Abendessen |
| `outputs/.../19-zwischenmahlzeiten.md` | 30 Zwischenmahlzeiten |

Alle Rezepte laufen durch **denselben Parser** wie die Webseiten:
`scripts/rezepte/bauen.py`, Funktion `lies(pfad)`. Format der Überschrift:
`### <Nr> · <Name> · <Zeit> · <Protein>`, darunter die Felder mit ihren Marken.

Lokal ansehen: `preview_start {"name": "energie-begleitung"}` → Port 4394.

---

## 🚨 Regeln, die nicht gelockert werden dürfen

**Keine Artifact-Fähigkeiten.** Sobald die Seite `db` oder `assets` deklariert,
kommen nur angemeldete Leute aus der Organisation hinein — für Kundinnen unbrauchbar.
Alles Eingetragene läuft über `localStorage`. Das Bauskript **warnt**, wenn
`capabilities` oder `claude.use(` in der Seite landen.

**Deshalb: alles bleibt auf ihrem Gerät.** Patricia sieht es nicht, und beim
Gerätewechsel fängt sie bei null an. Das steht so auf der Seite — als Zusage
formuliert („es soll dich niemand kontrollieren"), weil eine Zusage, die die Technik
nicht halten kann, schlimmer wäre als keine.

**Nur grünes Material.** Patricias eigene Rezepte, ihr Plan, Fakten aus ihren Büchern
mit Autor und Titel, ihre Immunwoche, Allgemeinwissen in eigenen Worten. **Kein Satz
aus den bezahlten Coachings** (feel.gut Darmbalance, MyBodyAdvice). Herkunft und
Grenze: `context/persoenlich/ernaehrungswissen/`.

**Keine Heilversprechen, keine Diagnosen.** Wo es medizinisch wird, steht der
Verweis im Text, nicht im Kleingedruckten. **Hormonersatztherapie kommt bewusst nicht
vor**, obwohl das Buch ein Kapitel dazu hat.

---

## 🚨 Drei Fallen, die schon zugeschnappt sind

**Ersetzungen ohne Gegenprobe laufen still ins Leere.** Drei `str.replace`-Aufrufe
hatten ein Leerzeichen zu viel im Suchtext und haben nichts getan — die ganze
Freischaltung funktionierte dadurch nicht, und der Bau meldete trotzdem Erfolg.
**Jede Ersetzung mit `assert alt in t` und `assert t.count(alt) == 1`.**

**Backslashes in JS-Regex.** Sie laufen durch Heredoc, Python und f-String. Das
Prüfskript dafür liegt im Scratchpad-Muster: ungültige Escape-Sequenzen suchen, und
den Bau mit `python -W error::SyntaxWarning` laufen lassen, damit er abbricht statt
still etwas Kaputtes zu erzeugen.

**Einheiten als ganzes Wort prüfen.** `rest.indexOf("g") === 0` hält **„grosse"**
und **„Gurken"** für Gramm — aus 24 Kartoffeln wurden 25. Gefunden am echten Rezept,
nicht am Code.

**Deutsche Anführungszeichen in Python-Zeichenketten.** Ein `"` statt `“` beendet die
Zeichenkette und legt den Bau lahm. In Texten `„` und `“` schreiben.

---

## Der Portionsrechner

Basis ist **6 Personen** — so sind die Rezepte geschrieben, und das steht auf jeder
Karte als Marke. Der Rechner skaliert von dort.

Gerundet wird nach Einheit: Gramm auf 10er ab 100 g sonst 5er · kg und l wechseln bei
kleinen Mengen auf g und ml · EL und TL auf halbe (mit ½) · Stückzahlen ganz, nie
unter 1. Ein- und Mehrzahl über die Tabelle `MENGENWORT` in `inhalte.py` — aus den
echten Rezepten gezogen, nicht geraten.

**Gegenprobe nach jeder Änderung:** bei 6 Personen muss jede der 120 Familienzeilen
**exakt** dem Rohtext entsprechen.

---

## Was noch offen ist

- ✅ **Verkaufsseite auf den Umfang gezogen** (24.09.) — 120 Rezepte, Begleitung auf dem
  Handy, 46 Artikel, Vorratsliste, Protein-Tabelle; Zahlen aus den Bauskripten gezählt.
  Text in `10-landingpage-…md`, Seite in `landingpage/index.html`.
- Die erste Anmeldung hat den Umfang noch nicht gesehen.
- Artifact freigeben (Share-Menü) und den Link in die Willkommens-Mail.

---

## 🔗 Verwandte Notizen

- [[11-30-tage-plan]] · [[12-30-fruehstuecke]] · [[17-mittagessen]] · [[18-abendessen]] · [[19-zwischenmahlzeiten]]
- [[16-belegte-fakten]] · [[15-wissens-dump-fragen]]
- [[10-landingpage-30-tage-energieroutine]]
