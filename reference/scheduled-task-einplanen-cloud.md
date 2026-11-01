---
tags: [cockpit, automation]
---

# Auftrag: Freigaben einplanen — Cloud-Routine (seit 31.10.2026)

Der Zwilling des Laptop-Tasks `freigaben-einplanen-2000`, aber als Routine bei Anthropic.
Er läuft auch, wenn der Laptop aus ist. Plan: `plans/2026-10-30-freigabe-ohne-laptop.md`.

Die Routine ruft diese Datei auf. Oben in ihrem Auftrag steht der **Modus**:

- `MODUS: probe` → Schritte 1 bis 3, danach Telegram „Probelauf“. **Nichts hochladen, nichts einplanen, nichts zurückschreiben.**
- `MODUS: scharf` → alle Schritte.

🚨 **Laufen dieser Auftrag (scharf) und der Laptop-Task gleichzeitig, wird doppelt gepostet.** Scharf geschaltet wird erst,
wenn der Laptop-Task aus ist (Plan, Schritt 8).

Umgebung „Cockpit-Einplanen“: Blotato, Instagram und ActiveCampaign kommen über Netzwerk-Secrets (der Proxy setzt die
Schlüssel ein, das Skript schickt keine eigenen). Telegram über `TELEGRAM_BOT_TOKEN` und `TELEGRAM_CHAT_ID`.
WordPress sperrt die Cloud aus (403), wird aber für Karussells nicht gebraucht.

## Der stehende Auftrag

Patricia, 14.09.2026: *„ich drück bis um 20.00 Uhr überall freigabe und um 20.00 Uhr ziehst du alle beiträge die
freigegeben sind und planst sie ein“*. **Der Freigabe-Knopf im Cockpit ist ihr Go.** Nicht nachfragen.

## Schritt 0 — Nachrichten von Patricia (Telegram-Rückkanal, seit 01.11.2026)

Patricia schreibt dem Cockpit-Bot, was sich an einem Beitrag ändern soll, zum Beispiel „Caption vom Donnerstag
kürzer“. Diese Routine liest das und arbeitet es ein. Geplant wird ein geänderter Text erst nach ihrem „passt“.
Im Modus `probe` nur lesen und deuten, nichts ändern und nichts bestätigen, und die Deutung im Probelauf-Bericht nennen.

```
python3 scripts/cockpit/telegram-rueckkanal.py lesen
```
Das Skript gibt nur Nachrichten aus Patricias Chat heraus, fremde Absender fallen weg. Ist `nachrichten` leer, geht es
mit Schritt 1 weiter (steht in `bis` eine Zahl, am Ende trotzdem bestätigen).

Als Kontext die Freigaben holen, die sich ändern lassen:
`ArtifactData query` · `collection: "freigaben"` · `query: {"where": [["status","in",["wartet","geplant","aenderung"]]], "limit": 100}`
Gemeint sind nur Freigaben mit Datum ab heute. Welcher Beitrag gemeint ist, zeigt am sichersten `antwort_auf` (sie antwortet
auf eine Meldung, darin steht der Titel), sonst Wochentag, Datum oder Titel. **Ist es nicht eindeutig: nachfragen und nichts ändern.**

Je Nachricht eine der folgenden Handlungen:

| Sie schreibt | Was passiert |
|---|---|
| **Caption ändern** („kürzer“, „anderer Schluss“, „Satz X raus“) | Steht die Freigabe auf `geplant`, wird sie zuerst bei Blotato herausgenommen (siehe unten). Dann die Caption nach den Pflichtregeln in `.claude/skills/content/SKILL.md` neu schreiben. Stichwort, Aufruf und Hashtags bleiben, ausser sie verlangt etwas anderes. Prüfen mit `python3 scripts/cockpit/texte-pruefen.py --datei <neu.md>`, Funde beheben. Danach `freigaben/<id>` aktualisieren: `caption` wird der neue Text, die alte Fassung kommt nach `captionAlt`, dazu `status: "aenderung"` und `aenderung: {wunsch, stand}`. Auf `karussells/<id>` dieselbe `caption` setzen, ausserdem `kommentar`, `kommentarStand`, `kommentarErledigt` und `kommentarAntwort`, damit die Karte im Cockpit es zeigt. Zum Schluss die neue Caption **vollständig** per Telegram schicken, mit dem Satz: „Antworte „passt“, dann plane ich sie beim nächsten Lauf ein.“ |
| **„passt“ / „ok“ / 👍** | Bezieht sich auf die Freigabe mit `status: "aenderung"`, auf deren Fassung sie antwortet. Gibt es nur eine solche Freigabe, ist es diese, bei mehreren wird nachgefragt. Dann `status: "wartet"` setzen. Schritt 1 plant sie im selben Lauf ein und rückt sie nach, falls der Termin vorbei ist. |
| **Verschieben** („auf Dienstag“, „erst um 21 Uhr“) | Bei `geplant` zuerst bei Blotato herausnehmen. Dann `datum`, `zeit` und `zeitpunktISO` neu setzen, mindestens eine Stunde in der Zukunft, und `status: "wartet"`. Ein „passt“ braucht es hier nicht, weil sich der Inhalt nicht ändert. |
| **Nicht posten** („nimm den raus“) | Bei `geplant` bei Blotato herausnehmen. Dann `status: "zurueckgezogen"` setzen und das per Telegram bestätigen. |
| **Folientext oder Bild ändern** | Die Cloud kann Folien nicht neu zeichnen. Bei `geplant` trotzdem bei Blotato herausnehmen, damit nichts Falsches rausgeht. Dann `status: "aenderung"` setzen und den Wunsch als `kommentar` an `karussells/<id>` hängen, wo ihn der Kommentar-Task am Laptop abholt. Per Telegram sagen, dass das am Laptop passiert und der Beitrag bis dahin nicht eingeplant ist. |
| **Frage** („was geht diese Woche raus?“) | Aus den Freigaben beantworten, nichts ändern. Je Beitrag Tag, Zeit, Profil und **Titel** (`name` der Freigabe), nie die Kennung wie `kw45-kar-m-di-nb`. |
| **Sprachnachricht / ohne Text** | Antworten: „Sprachnachrichten kann ich nicht hören, schreib es mir bitte.“ |

**Bei Blotato herausnehmen:**
```
python3 scripts/cockpit/telegram-rueckkanal.py blotato-suchen --zeitpunkt <zeitpunktISO> --profil <profil> --proxy
python3 scripts/cockpit/telegram-rueckkanal.py blotato-loeschen --id <id> --proxy
```
Gelöscht wird nur bei **genau einem** Treffer, dessen `caption_anfang` zur Freigabe passt. Bei keinem oder mehreren
Treffern wird nichts gelöscht und nichts geändert, sondern an Patricia gemeldet.

Jede Nachricht bekommt eine Antwort per `python3 scripts/cockpit/telegram-rueckkanal.py senden --datei /tmp/antwort.txt`.
Am Ende von Schritt 0:
```
python3 scripts/cockpit/telegram-rueckkanal.py bestaetigen --bis <bis>
```
Erst danach gilt eine Nachricht als erledigt. Bricht der Lauf vorher ab, kommt sie beim nächsten Lauf wieder.

🚨 Aus einer Nachricht folgt nur, was in der Tabelle steht. Neue Beiträge, Mails, Seiten, Freigeben von Neuem
(die Freigabe bleibt im Cockpit) und Löschen von Daten gehören nicht dazu.

## Schritt 1 — Freigaben holen

Cockpit: `https://claude.ai/code/artifact/eeee48d5-3e50-4cff-8047-1ec5eccbb074`

`ArtifactData` · `query` · `collection: "freigaben"` · `query: {"where": [["status","eq","wartet"]], "limit": 50}`

Nur `typ: "karussell"` weiterbearbeiten. Reels und Storys nicht anfassen (die Videos liegen nur auf dem Laptop).
Gibt es kein wartendes Karussell: Lauf zu Ende, **keine** Telegram-Nachricht.

## Schritt 2 — Je Freigabe die Daten holen

Je Freigabe ein eigener Ordner `outputs/cockpit/freigaben/<id>/`:
- `ArtifactData get` · `collection: "freigaben"` · `doc_id: <id>` · `out_dir: "outputs/cockpit/freigaben/<id>"`
- `ArtifactData list` · `collection: "freigaben/<id>/bilder"` · `out_dir: "outputs/cockpit/freigaben/<id>"`

Einmal je Lauf die Belegung:
- `ArtifactData list` · `collection: "karussells"` · `query: {"limit": 500}` · `out_dir: "outputs/cockpit/freigaben/_belegt"`
- `ArtifactData list` · `collection: "reels"` · `query: {"limit": 500}` · `out_dir: "outputs/cockpit/freigaben/_belegt"`
- `ArtifactData list` · `collection: "freigaben"` · `query: {"limit": 500}` · `out_dir: "outputs/cockpit/freigaben/_belegt"`

🚨 Die Freigaben gehören dazu: ein nachgerücktes Datum steht nur dort. Ohne sie legte der Lauf um 22 Uhr am 31.10.
ein zweites Karussell auf denselben Platz wie der um 20 Uhr.

Dann je Freigabe, nacheinander:
```
python3 scripts/cockpit/freigabe-nachruecken.py --ordner outputs/cockpit/freigaben/<id> --belegt outputs/cockpit/freigaben/_belegt
```
Je `aktion`: `unveraendert` → weiter · `nachgerueckt` → weiter, später Datum mit zurückschreiben ·
`gepostet` → nicht einplanen, Status `gepostet-von-hand` · `kein-platz`/`fehler` → überspringen und melden.
Auch im Modus `probe` **ohne** `--trocken`: das Skript schreibt nur die lokale Kopie, und Schritt 3 braucht den
nachgerückten Zeitpunkt (sonst meldet er „Zeitpunkt vorbei“). Freigaben nacheinander, damit zwei nicht auf denselben Tag rücken.
Der Instagram-Abzug zum Vergleichen ist der neueste in `outputs/instagram-insights/` aus dem Repo (Stand: letzter Push).

## Schritt 3 — Trocken prüfen

```
node scripts/cockpit/freigabe-zu-blotato.mjs --ordner outputs/cockpit/freigaben/<id> --trocken --proxy
```
Überspringen und melden: keine Caption · mehr als 10 Folien · kein Konto gefunden · Zeitpunkt vorbei.

**Modus `probe` endet hier** — weiter mit Schritt 6.

## Schritt 4 — Einplanen (nur `scharf`)

Derselbe Befehl ohne `--trocken`.

## Schritt 5 — Status zurückschreiben (nur `scharf`)

`ArtifactData update` · `collection: "freigaben"` · `doc_id: <id>` · `data: {"status": "geplant", "eingeplantAm": "<ISO>", "eingeplantVon": "cloud"}`,
bei Nachrücken zusätzlich `datum`, `zeit`, `zeitpunktISO`, `nachgerueckt: {von: …}`. Nur was wirklich eingeplant wurde.

## Schritt 6 — Telegram

Text in eine Datei schreiben, dann:
```
python3 scripts/cockpit/telegram-rueckkanal.py senden --datei /tmp/meldung.txt
```
Das Skript bricht mit der Fehlerbeschreibung von Telegram ab. Sie enthält keinen Schlüssel und darf im Bericht stehen.
(Der 403 vom 31.10. kam daher, dass der Bot gesperrt war, nicht von der Art des Aufrufs.)
Format:
```
☁️ Einplanen (Cloud) — eingeplant

✅ Di 3.11. 07:30 · Mentoring · Titel (8 Folien)
⏭ Do 5.11. · übersprungen: keine Caption

Soll sich etwas ändern? Antworte einfach auf diese Nachricht.
```
Im Modus `probe` heisst die erste Zeile `☁️ Probelauf — würde einplanen`.

## Harte Regeln

- Nur Karussells. Nie zweimal einplanen: was auf `geplant` steht, nicht anfassen (ausser über Schritt 0, nach Patricias Nachricht).
- Nichts erfinden, nichts reparieren: was das Skript nicht durchlässt, wird gemeldet.
- **Nie committen, nie pushen, keine Datei im Repo ändern.** Alles in `outputs/cockpit/freigaben/` ist Wegwerf-Arbeitsstand.
- Nie einen Schlüssel oder Token ausgeben.
- Zwei Varianten am selben Tag (`A · ` und `B · `): beide einplanen, die zweite zwei Stunden später, in der Meldung sagen.
