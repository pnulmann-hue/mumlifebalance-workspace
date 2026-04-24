# Telegram Userbot — Business Monitor

Liest automatisch in allen Telegram-Gruppen mit denen Patricia Mitglied ist, klassifiziert wichtige Nachrichten (Ankündigungen, Strategien, Events, Learnings) und sendet DM-Benachrichtigungen mit Buttons zum Speichern.

## Setup

### 1. Dependencies installieren

```bash
cd scripts/telegram-userbot
npm install
```

### 2. Einmalig einloggen (lokal)

```bash
npm run login
```

- Gibt deine Handynummer ein (mit Ländercode, z.B. `+41...`)
- Kopiere den Code aus Telegram (der kommt auf ein anderes eingeloggtes Gerät)
- Die Session-String wird automatisch in `.env` gespeichert

### 3. Lokal testen

```bash
npm start
```

Schau ob Nachrichten in der Console auftauchen. Schicke dir selbst eine Nachricht in einer Gruppe — sollte klassifiziert werden.

### 4. Deploy auf Railway

1. Erstelle neuen Service auf Railway
2. Verlinke den Ordner `scripts/telegram-userbot` (via GitHub oder direkt Upload)
3. Setze alle Environment-Variablen aus `.env` in Railway ein
4. Deployment startet automatisch — check Logs ob alles läuft

## Commands (in DM mit deinem Notification-Bot)

- `/status` — Status prüfen
- `/list_chats` — Whitelist anzeigen
- `/add_chat` — Forward einer Nachricht aus der Gruppe fügt sie hinzu

## Architektur

```
┌─────────────────────┐
│ Telegram Account    │  ← Patricia ist Mitglied in Gruppen
│ (Patricia)          │
└──────────┬──────────┘
           │ User-Session
           ▼
┌─────────────────────┐      ┌─────────────────────┐
│ Userbot (Railway)   │─────▶│ Claude Haiku        │ Klassifikation
│ Node.js + GramJS    │◀─────│                     │
└──────────┬──────────┘      └─────────────────────┘
           │
           ▼
┌─────────────────────┐
│ Supabase            │ Tracking + Embeddings
│ telegram_messages   │
│ documents           │
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│ Normaler Bot        │ DM mit Inline-Buttons
│ (TELEGRAM_BOT_TOKEN)│ → Speichern/Skip
└──────────┬──────────┘
           │ Button-Klick
           ▼
┌─────────────────────┐
│ Vercel Webhook      │
│ /api/telegram/...   │
└─────────────────────┘
```
