---
tags: [misc]
---

# Scheduled Task — Kommentare einarbeiten

**Läuft:** täglich **19:30**, also eine halbe Stunde vor `freigaben-einplanen-2000`.
Damit ist alles, was Patricia tagsüber angemerkt hat, eingearbeitet, **bevor** der
Einplan-Task die Freigaben abholt.

**Wozu:** Patricia tippt auf der Wochenkarte in die Zeile „Was soll ich ändern?" —
*„Caption neu schreiben"*, *„Video passt nicht"*, *„Hook zu brav"*. Ohne diesen Task
bliebe das liegen, bis sie im Chat davon erzählt. Ihr Wunsch vom 16.09.2026: *„das
automatisch siehst anpasst und mir wieder aktualisierst und auf telegram schreibst, dass
der beitrag aktualisiert wurde und zur freigabe steht"*.

---

## Der Auftrag

Lies mit `ArtifactData` aus dem Cockpit
(`https://claude.ai/code/artifact/eeee48d5-3e50-4cff-8047-1ec5eccbb074`) die Sammlungen
**`reels`**, **`karussells`** und **`storys`**.

**Offen ist ein Beitrag, wenn** `kommentar` gefüllt ist **und** `kommentarErledigt`
fehlt **oder älter ist als** `kommentarStand`.

🚨 **Über die Zeitstempel vergleichen, nie über ein Häkchen.** Sonst bleibt ein zweiter
Kommentar zum selben Beitrag unbemerkt, weil der erste schon als erledigt gilt.

Gibt es keinen offenen Kommentar: **nichts tun, keine Telegram-Nachricht.** Eine
Nachricht „heute nichts" jeden Abend ist Lärm, und Lärm wird weggewischt.

### Je offenem Kommentar

1. **Lies den Beitrag ganz** — Hook, Caption, Skript, Folien, Datum, Profil.
2. **Lies die Regeln, bevor du schreibst.** Für Hooks `.claude/skills/hooks/SKILL.md`,
   für Reels `context/reels-framework.md`, für Karussells
   `context/karussell-framework.md`, für Storys `context/story-framework.md`, dazu
   `context/brand-voice.md` und `context/ki-phrasen-blackliste.md`.
   🚨 **Nicht aus dem Gedächtnis schreiben.** Die Regeln ändern sich, und eine Caption,
   die gestern durchging, fällt heute durch.
3. **Arbeite genau das ein, was dasteht** — nicht mehr. Steht „Caption neu", wird die
   Caption neu geschrieben und der Hook bleibt. Sonst ändert sich unter der Hand etwas,
   das sie schon abgenommen hatte.
4. **Prüfe das Ergebnis** gegen den Beitrags-Check (vier Fragen) und den letzten
   Hook-Check, bevor du es zurückschreibst.
5. **Schreib zurück** mit `ArtifactData update`, mit `if_version` aus dem Lesen:
   - das geänderte Feld (`caption`, `hook`, `skript`, `slides` …)
   - `kommentarErledigt` = jetzt, als ISO-Zeitstempel
   - `kommentarAntwort` = **ein Satz, was tatsächlich geändert wurde**, nicht „erledigt".
     Sie soll auf der Karte lesen können, was passiert ist, ohne den Text zu vergleichen.
   - `kommentar` bleibt stehen — das ist der Verlauf.

### Was nicht geht

Manches lässt sich nicht per Text lösen. **Sag das, statt etwas anderes zu ändern:**

| Kommentar | Antwort |
|---|---|
| „Video passt nicht" | Es gibt kein Ersatzvideo. `kommentarAntwort`: was am Video stört, und dass ein neuer Dreh nötig ist — mit dem Sprechtext, den sie dafür braucht. |
| „anderes Foto" | Fotos liegen im Bild-Editor, nicht hier. Sag, welches passen würde und wo. |
| Unklar, was gemeint ist | **Nichts ändern.** `kommentarAntwort`: die Rückfrage. Lieber nachfragen als raten — eine falsch geratene Änderung kostet mehr als eine Nachfrage. |

---

## Telegram

**Eine** Nachricht für alle Änderungen zusammen, nicht eine pro Beitrag.

```
✏️ 3 Beiträge aktualisiert und bereit zur Freigabe

• Mi · Drei Wege ohne Namensliste
  „Caption neu schreiben" → Caption neu, Einstieg jetzt als Frage

• Do · Die Phase, über die keiner redet
  „Hook zu brav" → Hook geschärft, Szene statt Zusammenfassung

⚠️ Do · doTERRA · Zwei Arten von müde
  „Video passt nicht" → braucht einen neuen Dreh, Sprechtext steht in der Karte

→ Wochen-Vorschau öffnen und freigeben
```

Zugang: `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`. **Nie den Token in den Task-Text
schreiben** — er kommt aus der Umgebung.

---

## Grenzen

- **Nichts freigeben.** Der Task ändert Texte, er setzt nie `textfrei`. Die Freigabe
  bleibt Patricias Klick — siehe die Regel „Freigabe IST das Go".
- **Nichts einplanen.** Das macht `freigaben-einplanen-2000` um 20:00.
- **Nichts löschen.** Auch einen Beitrag nicht, zu dem „taugt nichts" steht — dann
  `kommentarAntwort` mit dem Vorschlag, ihn zu ersetzen, und sie entscheidet.
- **Storys nie an Blotato.** Die postet Patricia selbst.
