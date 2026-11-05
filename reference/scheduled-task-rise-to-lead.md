---
tags: [cockpit, routine, doterra]
---

# Auftrag: Rise to Lead — die Gruppen lesen, damit Patricia und ihr Team es nicht müssen (seit 05.11.2026)

Patricia: *„es kommen täglich so viele nachrichten in der gruppe, dass ich und mein team die übersicht
verloren haben was relevant ist. deshalb kommst du zum einsatz. ich würde gerne meine teammitglieder enger
begleiten … vielleicht zwei impulse rsp. aufgaben?“*

Läuft täglich als Scheduled Task `rise-to-lead`, nur solange der Laptop an und die App offen ist. Ersetzt
Schritt 4b im `cockpit-daten-abgleich`, der dort seit dem 23.10. nichts mehr eingetragen hat.

🚨 **Jeder Befehl einzeln über das Bash-Werkzeug, genau so wie hier geschrieben — kein PowerShell, kein `cd`,
kein `&&`.** Nur diese Schreibweise ist freigegeben. Eine Rückfrage beantwortet hier niemand.
🚨 Ans Team geht nie etwas automatisch. Du schreibst nur Entwürfe. Nichts löschen, nicht committen.

`COCKPIT` = `https://claude.ai/artifact/WWF7EWhCiAf2cVi1vytGFM`

## Täglich

1. Nachrichten und Sprachnachrichten holen, dann abtippen:
   ```
   npm --prefix scripts/telegram-userbot run rise-to-lead
   npm --prefix scripts/telegram-userbot run rise-to-lead-audio
   python scripts/doterra/rtl-abtippen.py
   ```
   Das `Error: TIMEOUT` nach dem Holen ist harmlos, wenn davor „→ … Nachrichten“ steht.
2. In `outputs/cockpit/abgleich/business-telegram/eingetragen.json` steht unter `bis` je Chat die letzte
   verarbeitete Nachricht. Nur Nachrichten mit höherer `id` aus `<chatId>.json` lesen, dazu die neuen Transkripte in
   `video/telegram-calls/rise-to-lead/transkripte/`. Whisper verhört sich bei Fachwörtern, nie eine Schreibweise übernehmen.
3. **To-dos für Patricia, nur aus Beiträgen von Danny (Daniela Hülsen) oder Claudia Brunner.** Im Kanal
   „SILVER TO GOLD“ schreiben nur sie, Feld `von` ist dort der Kanalname. Erfolgsmeldungen, Emojis, Rangfeiern und Fragen
   anderer sind keine To-dos. Daraus wird:
   - Aufgabe der Woche → eine Aufgabe, als Handlung formuliert
   - Call, Webinar, Live → Aufgabe am Tag des Termins, Uhrzeit vorne im Titel
   - Sprachnachricht oder Video → „Lernen: „<Thema>“ vom <TT.MM.>“, in `notiz` drei Sätze, was drin ist. So muss sie es nur anhören, wenn es sie anspricht. Fällig am nächsten Tag.
   - neue Aktion → nur, wenn sie etwas zu tun verlangt
   Eine Aufgabe = ein Handgriff. Titel „Rise to Lead · <Termin|Lernen|Kundinnen|Team gewinnen|Überblick>: …“.
   Felder: `id: "rtl-<chatId>-<msgId>"`, `aufgabe`, `datum`, `prio` (Hoch nur bei Frist in 3 Tagen oder Call, sonst Mittel),
   `status: "Geplant"`, `notiz` (woher, Datum, was genau), `erledigt: false`, `bereich: "Business"`,
   `quelle: "Rise to Lead"`, `fuerClaude: false`. Keine Wiederholungen: gibt es die Kennung oder denselben Termin schon, weglassen.
4. Gibt es neue To-dos: `ArtifactData get` auf `COCKPIT`, Sammlung `daten`, Dokument `aufgaben`. Neue Aufgaben **vorne** an `items`,
   `updatedAt` auf jetzt, `set` mit `file_path` und `if_version`. 🚨 Nur anhängen, nichts ändern oder abhaken. Scheitert
   `if_version`, neu lesen und nochmal.
5. `eingetragen.json` auf die neuen höchsten `id` setzen. Erst danach, sonst geht etwas verloren.

## Montags und donnerstags zusätzlich: die Nachricht fürs Team

**Montag = Aufgabe** · **Donnerstag = Impuls.** Kennung `<JJJJ-MM-TT>-aufgabe` bzw. `-impuls`. Gibt es sie schon, nichts tun.

1. Vorher lesen: `doterra-wissen/team-impulse` auf `COCKPIT` (damit sich nichts wiederholt), `context/doterra/energie-story-profil.md`,
   `context/doterra/backoffice/rise-to-lead-2026-10.md`. Quelle ist alles aus den Gruppen seit der letzten Team-Nachricht, **auch was
   andere Mitglieder erzählen, was bei ihnen funktioniert hat** — dort stehen die besten Ideen. Reicht das nicht, nimm etwas aus der Übersicht, das noch nie dran war.
2. Wähle **genau eine** Sache: die, die jemand aus ihrem Team diese Woche ohne Vorbereitung tun kann. Keine Zusammenfassung, keine Liste.
   Passt zum aktuellen Monatsthema der Mentorinnen, wenn möglich.
   - **Aufgabe (Mo):** eine Handlung bis Donnerstag, so konkret, dass man nicht nachdenken muss, mit einem fertigen Satz zum Kopieren.
   - **Impuls (Do):** eine Idee oder ein Gedanke, kurz mit dem Montag verbunden („wie lief es?“), mit einer kleinen Sache fürs Wochenende.
3. Schreiben, 80 bis 150 Wörter, für die Gruppe ihrer Beraterinnen (es sind auch Männer dabei, Anrede „Ihr Lieben“):
   - Patricias Stimme: wie eine Freundin, warm, direkt, ganze ruhige Sätze, kein Stakkato. Schweizer ss, echte Umlaute, höchstens vier Emojis, kein Markdown.
   - Am Schluss eine einfache Bitte zu antworten, nach dem Kommentar-Muster: etwas, das ohne Denkaufwand geht.
   - 🚨 **Nie:** Namen oder Ränge aus der Gruppe · was jemand Privates erzählt (Krankheit, Trauer, Partner, Kinder) · Zoom-, Gruppen- oder Aufzeichnungs-Links ·
     Wortlaut von Danny oder Claudia, Inhalte immer in eigenen Worten · Heilversprechen oder Wirkaussagen (auch nicht als Erfahrungsbericht) · Einkommens- oder Rangversprechen ·
     erfundene Zahlen oder Erlebnisse von Patricia · „sondern“, „nicht X, sondern Y“, KI-Floskeln · Druck.
     Beispiele aus der Gruppe heissen „eine aus meiner Mentoring-Gruppe“. Ein Stand am Markt braucht den Hinweis auf die Abklärung mit Compliance.
4. Text in eine Datei legen und prüfen. Bei einem Fund neu schreiben:
   ```
   python scripts/cockpit/texte-pruefen.py --datei outputs/cockpit/abgleich/business-telegram/impuls.md
   ```
5. Anhängen: `ArtifactData get` Sammlung `doterra-wissen`, Dokument `team-impulse`. Neuer Eintrag **vorne** an `items`:
   `{id, datum, art: "aufgabe"|"impuls", titel, text, fuerDich}`. `fuerDich` = ein Satz für Patricia: woher die Idee stammt. `stand` auf jetzt, `set` mit `file_path` und `if_version`.
6. An Patricia schicken: die Datei `outputs/cockpit/abgleich/business-telegram/nachricht.txt` schreiben mit
   - erste Zeile „Fürs Team, zum Weiterleiten:“, dann eine Leerzeile, dann nur der Text,
   danach
   ```
   python scripts/telegram/senden.py --text-datei outputs/cockpit/abgleich/business-telegram/nachricht.txt
   ```
   Eine zweite Nachricht mit `--text` nur, wenn es neue Termine oder To-dos gab: höchstens drei Zeilen „Für dich: …“.

## Melden

Scheitert etwas, per Telegram:
`python scripts/telegram/senden.py --text "⚠️ Rise to Lead: <Schritt> — <Grund>"`. Keine neuen To-dos an einem normalen Tag → keine Nachricht.
