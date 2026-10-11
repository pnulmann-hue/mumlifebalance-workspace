# Archiv — die Chat-Version des Produkt-Ideen-Finders

Abgelöst am 14.09.2026 durch die Formular-Version (drei Schritte:
Dein Thema → Deine Ideen → Inhaltsverzeichnis).

| Datei hier | lag vorher unter |
|---|---|
| `api-chat.js` | `api/chat.js` — Claude-Proxy für den Chat-Verlauf |
| `public-chat.js` | `public/chat.js` — Frontend, 6-Schritte-Gespräch |
| `system-prompt.md` | `lib/system-prompt.md` — der Gesprächs-Prompt (418 Zeilen) |
| `lead.js` | `api/lead.js` — E-Mail an ActiveCampaign |
| `index.html` / `styles.css` | Stand vor dem Umbau, zum Nachschlagen |

**Warum weg:** Das Gespräch brauchte sechs Runden bis zur ersten Idee. Die
Formular-Version braucht ein Feld und einen Knopf.

**`lead.js` ist mit weg**, weil im Formular keine E-Mail mehr abgefragt wird —
die Leads kommen über das ManyChat-Keyword, bevor jemand den Link überhaupt
bekommt. Wer die E-Mail-Strecke zurückwill, holt die Datei von hier.
