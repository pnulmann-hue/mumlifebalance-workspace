---
tags: [cockpit, routine]
---

# Auftrag: Heute dran — Telegram am Morgen und am Abend (seit 03.11.2026)

Patricia: *„wie können wir gewährleisten, dass mir die dinge aufploppen?“* Im Cockpit steht
die Liste „Heute dran“ ganz oben auf Mein Tisch. Diese Routine schickt dieselbe Liste aufs
Handy: **07:00** alles für den Tag, **20:00** nur, was noch offen ist. Ist nichts offen,
geht **keine** Nachricht raus.

Routine „Cockpit: Heute dran (Telegram)“, Umgebung „Cockpit-Einplanen“ (dort liegen
`TELEGRAM_BOT_TOKEN` und `TELEGRAM_CHAT_ID`). Cron in UTC — im Winter 06:00 und 19:00,
im Sommer 05:00 und 18:00.

🚨 **Diese Routine liest nur.** Kein Schreiben in die Datenbank, kein Einplanen, nichts an
das Team. Nie committen, nie pushen, nie einen Schlüssel ausgeben.

## Schritt 1 — Welche Runde?

`TZ=Europe/Zurich date +%H` — vor 12 ist es die Morgenrunde, sonst die Abendrunde (`--abend`).

## Schritt 2 — Die Dokumente holen

Für jedes der fünf Dokumente einen Aufruf, alle in denselben Ordner:

`ArtifactData` · `action: "get"` · `url: "https://claude.ai/artifact/WWF7EWhCiAf2cVi1vytGFM"` ·
`collection: "daten"` · `doc_id:` `aufgaben` · `termine` · `rising-leaders` ·
`wochenbogen-notizen` · `tagebuch` · `out_dir: "/tmp/hd"`

Meldet ein Aufruf „No document“, ist das kein Fehler — das Dokument gibt es erst, wenn
Patricia den Teil im Cockpit benutzt hat. Weiter mit dem nächsten.

## Schritt 3 — Die Nachricht bauen

```bash
python3 scripts/cockpit/heute-dran.py --ordner /tmp/hd --datei /tmp/hd.txt
```

(Abendrunde: zusätzlich `--abend`.) Endet das Skript mit Code 3, ist nichts offen:
**Lauf zu Ende, keine Nachricht.**

## Schritt 4 — Schicken

```bash
python3 scripts/cockpit/telegram-rueckkanal.py senden --datei /tmp/hd.txt
```

Den Text nicht umschreiben und nichts dazuerfinden. Scheitert Schritt 2 bei **allen** fünf
Dokumenten oder Schritt 3 mit einem anderen Code als 0 oder 3, eine kurze Telegram-Meldung
„Heute dran: Lauf gescheitert (<Schritt>)“ schicken, damit ein stiller Ausfall auffällt.
