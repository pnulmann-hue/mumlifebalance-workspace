Notiz-System für Patricia — schnelles Erfassen und Abrufen von Gedankenstützen.

Die zentrale Datei ist `outputs/notizen/notiz-inbox.md`.

## Verhalten je nach Eingabe

### Fall A: `/notiz` OHNE Text (nur der Command) → ABRUFEN
1. Lies `outputs/notizen/notiz-inbox.md`.
2. Gib die **offenen** Notizen kompakt und lesbar wieder (neueste zuerst, mit Datum).
3. Wenn es viele sind: gruppiere grob nach Thema/Tag.
4. Frage am Ende, ob Patricia etwas davon aufgreifen, abhaken oder ergänzen will.
5. Wenn die Inbox leer ist: sag das freundlich und lade zum Erfassen ein.

### Fall B: `/notiz <text>` MIT Text → ERFASSEN
1. Lies `outputs/notizen/notiz-inbox.md`.
2. Erzeuge einen neün Eintrag in der Sektion `## 🟢 Offen`, **ganz oben** (neueste zuerst):
   ```markdown
   ### <heutiges Datum YYYY-MM-DD> — <selbst gewählter Kurztitel>
   <der Notiz-Text im Volltext, leicht aufgeräumt aber inhaltlich unverändert>
   ```
   - Kurztitel selbst aus dem Inhalt ableiten (3-6 Wörter).
   - Wenn ein Thema erkennbar ist (Content, doTERRA, Garten, Business, Privat …), hänge ein `#tag` an.
   - Ersetze den Platzhalter-Satz „_Noch keine offenen Notizen…_", falls er noch dasteht.
3. Bestätige kurz: „✅ Notiz gespeichert: <Kurztitel>".
4. **WICHTIG:** Änderung committen und pushen, damit sie am Laptop verfügbar ist
   (Branch beibehalten, `git push -u origin <branch>`), es sei denn Patricia sagt ausdrücklich „nur lokal".

### Fall C: „Notiz X erledigt" / „hak ab" → ARCHIVIEREN
1. Verschiebe den Eintrag aus `## 🟢 Offen` nach `## ✅ Erledigt / Archiv`, mit `✅`-Präfix am Titel.
2. Bestätige kurz und committe/pushe.

## Regeln
- **Datum** immer aus dem aktuellen Kontext (currentDate) nehmen, nie raten.
- Obsidian-Konvention wahren: Frontmatter-Tags oben nicht anfassen, `_INDEX.md` nur ergänzen wenn eine **neü separate** Notiz-Datei entsteht (nicht bei Inbox-Einträgen).
- Wird eine einzelne Notiz sehr gross oder eigenständig, biete an, sie als eigene Datei
  `outputs/notizen/YYYY-MM-DD-<thema>.md` (mit Tags `[notiz, <thema>]`) auszulagern und im `_INDEX.md` zu verlinken.
- Patricia schreibt oft frei im Chat („Notiz: …", „merk dir…", „schreib auf…") — behandle das genauso wie `/notiz <text>`.
