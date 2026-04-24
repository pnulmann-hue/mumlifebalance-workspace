# private/bot-doterra/ — Patricias private doTERRA-Daten

> **🔒 PRIVAT — NICHT IN BOT-RAG.** Wird vom doTERRA-Bot bei Bedarf **direkt via Notion-API** gelesen (nicht via RAG-Embeddings).

## Scope

Patricias eigene, persönliche doTERRA-Daten:

- Rang-Plan (Premier → Gold)
- OV-Stand, Ziel-OV
- Leg-Struktur (Leg 1 Premier, Leg 2 ~Elite, Leg 3 sub-Elite)
- Direktkunden-Liste (Stand April 2026: 36 gesamt, 32 aktiv)
- Team-Aktivierungs-Plan (2 aktiv, 2 Potenzial, 1 ausgestiegen)
- Neukunden-Monatsziel und Ist-Stand
- doTERRA-Provisions-Umsatz pro Monat

## Primäre Datenqülle

Patricias bestehende doTERRA-Jahresplanung in Notion:
→ `https://www.notion.so/2ae7078e8b7e81d9b5e1c6bea76ac287` (Zugriff der Notion-Integration noch zu klären, aktuell 404)

**Sobald Zugriff steht:** Der Bot liest die Jahresplanung direkt via Notion-Tools (`get_current_quarter_focus()`, `get_week_tasks()` etc.) — diese Daten werden **nie in den RAG-Index aufgenommen**, sondern ad-hoc abgefragt. Damit bleiben die Zahlen strikt auf Patricias Bot-Kontext beschränkt, nicht auf den Team-RAG-Kontext.

## Was NICHT hier reinkommt

- Mentoring-Kurs-Umsatz → gehört nach `../leaderin-gesamt/`
- 1:1-Klient-Listen → gehört nach `../leaderin-gesamt/`
- Gesamt-40k-Ziel über alle Säulen → gehört nach `../leaderin-gesamt/`
- Instagram-Profil-1-Strategie (Mentoring) → gehört nach `../leaderin-gesamt/`

## Was NICHT im Team-RAG landen darf

- Diese Zahlen, Namen, konkrete Team-Metriken
- Patricias persönlicher Gold-Plan mit OV-Zielen
- Namen einzelner Direktkunden oder Team-Mitglieder

→ Der RAG-Ingest schliesst `private/` komplett aus. Bot-Zugriff nur via Notion-Tools mit Scope-Check auf Patricia als User.
