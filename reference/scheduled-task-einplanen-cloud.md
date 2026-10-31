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

Text in eine Datei schreiben, dann (GET, POST wurde am 31.10. mit 403 abgewiesen):
```
curl -s -G "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" --data-urlencode "chat_id=$TELEGRAM_CHAT_ID" --data-urlencode "text@/tmp/meldung.txt" | head -c 300
```
Die Antwort zeigt `"ok":true` oder die Fehlerbeschreibung von Telegram. Sie enthält keinen Schlüssel, darf also im Bericht stehen.
Format:
```
☁️ Einplanen (Cloud) — eingeplant

✅ Di 3.11. 07:30 · Mentoring · Titel (8 Folien)
⏭ Do 5.11. · übersprungen: keine Caption
```
Im Modus `probe` heisst die erste Zeile `☁️ Probelauf — würde einplanen`.

## Harte Regeln

- Nur Karussells. Nie zweimal einplanen: was auf `geplant` steht, nicht anfassen.
- Nichts erfinden, nichts reparieren: was das Skript nicht durchlässt, wird gemeldet.
- **Nie committen, nie pushen, keine Datei im Repo ändern.** Alles in `outputs/cockpit/freigaben/` ist Wegwerf-Arbeitsstand.
- Nie einen Schlüssel oder Token ausgeben.
- Zwei Varianten am selben Tag (`A · ` und `B · `): beide einplanen, die zweite zwei Stunden später, in der Meldung sagen.
