---
tags: [kochen, rezept, eingang]
---

# Kochbot-Eingang

Hier landen **Rezepte, die der Mail-Assistent aus E-Mails extrahiert hat** — automatisch als `.md`-Datei mit sauber herausgelöstem Rezept (ohne Werbe-Ballast).

## Woher kommt das?

Der Mail-Sweep (`scripts/telegram-userbot`) erkennt Mails mit einem **vollständigen, nachkochbaren Rezept** (Zutaten + Zubereitung) und legt sie hier ab. Reine Rezept-Werbung ohne echtes Rezept wird **nicht** gestaged.

## Wie kommen die ins Kochbot-RAG?

- **Wenn** die Kochbot-Supabase-Zugangsdaten in der Userbot-`.env` stehen
  (`KOCHBOT_SUPABASE_URL` + `KOCHBOT_SUPABASE_KEY`), werden Rezepte beim Sweep
  **sofort live** in den Kochbot-RAG embeddet — zusätzlich zur Datei hier.
- **Ohne** diese Zugangsdaten bleiben die Rezepte hier als Eingangskorb liegen,
  bis sie eingespielt werden. Sie gehen nicht verloren.

## Aktivierung des Live-Ingests

In `scripts/telegram-userbot/.env` ergänzen (Werte aus dem Kochbot-Supabase-Projekt,
*nicht* dem doTERRA-Projekt):

```
KOCHBOT_SUPABASE_URL=https://<projekt>.supabase.co
KOCHBOT_SUPABASE_KEY=<service-role-key>
```

Danach speist jeder Sweep neue Rezepte direkt ein. Bereits hier liegende Dateien
können per erweitertem `scripts/kochbot-rag`-Ingest nachgezogen werden.
