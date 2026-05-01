# Setup-Anleitung: 3 fehlende API-Keys für Story-Render-Bot

**Stand:** 2026-05-01
**Zeit:** ca. 15 Min Gesamt-Setup
**Was Patricia tun muss:** drei Keys holen und in `.env` einfügen

---

## Übersicht

Die `.env` im Workspace-Root hat bereits leere Slots vorbereitet:

```
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
NOTION_API_KEY=
```

Du musst nur in jede Zeile **deinen Key nach dem `=` einfügen**, OHNE Anführungszeichen.

Beispiel — so soll's am Ende aussehen:
```
ANTHROPIC_API_KEY=sk-ant-api03-abcXYZ123...
OPENAI_API_KEY=sk-proj-abcXYZ...
NOTION_API_KEY=secret_abcXYZ...
```

---

## 🔑 Key 1: Anthropic (Claude API)

**Wofür:** Der Bot ruft Claude API für Story-Generierung auf (Voice-Check, Julia-Templates, Slide-Texte schreiben)

**Kosten:**
- Input: ~$3 pro 1 Million Token (= ca. 750'000 Wörter)
- Output: ~$15 pro 1 Million Token
- Pro Story-Lauf: ca. $0.05–0.15 (Cent-Bereich)
- Bei 1× pro Tag = ca. **$3–5 pro Monat**

**Setup (5 Min):**

1. Gehe auf [console.anthropic.com](https://console.anthropic.com)
2. Account erstellen (E-Mail + Passwort)
3. **WICHTIG:** Bei „Plans" musst du **Pay-as-you-go** aktivieren — es gibt keinen Free-Tier
   - Mindesteinzahlung: $5 (reicht für ca. 2-3 Monate Story-Bot)
   - Kreditkarte hinterlegen
4. Linke Seitenleiste → **API Keys** → **Create Key**
5. Name: „Patricia Story-Render-Bot"
6. **Kopiere den Key** (wird nur EINMAL angezeigt!)
7. In `.env` einfügen:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-DEIN-KEY-HIER
   ```
8. Speichern

**Sicherheit:** Niemals den Key in Code/Git/Chat teilen. `.env` ist gitignored.

---

## 🔑 Key 2: OpenAI (Whisper für Sprachnotizen)

**Wofür:** Wenn du dem Bot eine Sprachnotiz schickst, transkribiert Whisper sie zu Text.

**Kosten:**
- $0.006 pro Minute Audio
- Pro Story-Lauf eine 1-Minuten-Sprachnotiz = $0.006
- Bei 1× pro Tag = **$0.20 pro Monat**

**Alternative:** Wenn du keine Sprachnotizen nutzen willst → kannst du diesen Key **auch leer lassen**. Bot funktioniert dann nur mit Text-Antworten.

**Setup (3 Min):**

1. Gehe auf [platform.openai.com](https://platform.openai.com)
2. Account erstellen (oder einloggen wenn schon vorhanden)
3. **Pay-as-you-go aktivieren** (Mindesteinzahlung $5)
4. Linke Seitenleiste → **API keys** → **Create new secret key**
5. Name: „Patricia Story-Bot Whisper"
6. **Kopiere den Key** (wird nur EINMAL angezeigt!)
7. In `.env` einfügen:
   ```
   OPENAI_API_KEY=sk-proj-DEIN-KEY-HIER
   ```
8. Speichern

---

## 🔑 Key 3: Notion (Wochenplan + Monatsplan)

**Wofür:** Bot liest deinen Notion-Wochenplan + Monatsplan + Themenplanung um zu wissen welche Säule + welches Produkt heute beworben wird.

**Kosten:** Kostenlos (Notion-API ist gratis)

**Setup (5-7 Min — etwas mehr Klick-Arbeit):**

### Schritt 1: Integration erstellen

1. Gehe auf [notion.so/profile/integrations](https://www.notion.so/profile/integrations)
2. Klick **„New integration"**
3. Felder:
   - **Name:** „Patricia Story-Bot"
   - **Workspace:** dein Workspace wählen (Mum Life Balance)
   - **Type:** „Internal" (NICHT Public)
4. Klick **„Save"**
5. Auf der nächsten Seite siehst du den **Internal Integration Secret** (das ist der Key)
6. **Kopiere den Key** (beginnt mit `secret_` oder `ntn_`)
7. In `.env` einfügen:
   ```
   NOTION_API_KEY=secret_DEIN-KEY-HIER
   ```
8. Speichern

### Schritt 2: Integration Zugriff geben

**WICHTIG:** Die Integration weiss zwar dass sie existiert, aber sieht noch keine Pages. Du musst sie EINZELN zu jeder Notion-Seite hinzufügen die der Bot lesen soll.

Folgende Pages/DBs braucht der Bot:

| DB | Notion-URL (geöffnet auf Page) |
|---|---|
| **Wochenplanung-DB** | suche „Wochenplanung" in Notion |
| **Monatsplanung-DB** | suche „Monatsplanung" in Notion |
| **Content-Themenplanung-DB** | suche „Content-Themenplanung" |
| **Content-Management-DB** | suche „Content-Management" |
| **Produkte-DB** (optional) | suche „Produkte" |

Pro DB:

1. Öffne die DB in Notion
2. Oben rechts „•••" Menü
3. **„Add connections"** klicken
4. Suche „Patricia Story-Bot"
5. Klick um Zugriff zu geben

**Tipp Patricia-spezifisch:** Du kannst auch der **Top-Level-Page** Zugriff geben („Online Business Brain" oder ähnlich) — dann erbt jede Sub-Page/DB den Zugriff automatisch. Das geht schneller als pro DB einzeln.

### Schritt 3: Verifizieren

Nach dem Hinzufügen kannst du testen ob die Integration funktioniert:

```bash
cd "C:/Users/pnulm/Desktop/Mein Business/scripts/story-render-bot"
python -c "from notion_client import Client; import os; from dotenv import load_dotenv; load_dotenv('../../.env'); c = Client(auth=os.getenv('NOTION_API_KEY')); r = c.search(query='Wochenplanung'); print(f'✅ {len(r[\"results\"])} Treffer für Wochenplanung')"
```

Wenn das `✅ X Treffer` zeigt = Setup erfolgreich.

---

## ✅ Setup-Check (alle Keys testen)

Sobald alle 3 Keys in `.env` sind:

```bash
cd "C:/Users/pnulm/Desktop/Mein Business/scripts/story-render-bot"
python config.py
```

**Erfolgreich:**
```
✅ Setup OK
   Workspace: C:\Users\pnulm\Desktop\Mein Business
   Telegram-Bot: ...EwOv1RA
   Claude-Model: claude-sonnet-4-5-20250929
   Schedule: Mo-So 06:30 Europe/Zurich
```

**Bei Fehler:**
```
❌ Setup unvollständig — fehlt:
   - ANTHROPIC_API_KEY
```

→ Key prüfen, Tippfehler in `.env`?

---

## 🔒 Sicherheits-Hinweise

### .env ist privat
- `.env` ist in `.gitignore` → wird NIE auf GitHub hochgeladen
- Niemals `.env`-Inhalt in Chats / Slack / E-Mails teilen
- Bei Verdacht auf Leak: API-Keys SOFORT widerrufen + neu generieren

### Pro Service:
- **Anthropic:** API-Keys können in console.anthropic.com → API Keys → Disable
- **OpenAI:** platform.openai.com → API keys → Revoke
- **Notion:** notion.so/profile/integrations → Integration löschen

### Railway-Deploy:
Wenn der Bot auf Railway läuft, müssen die Keys auch in **Railway Environment Variables** gesetzt sein (nicht in der `.env` im Repo).

→ siehe `deploy_to_railway.py` und `README.md`.

---

## 💰 Kosten-Übersicht (geschätzt)

Bei 1× Story-Lauf pro Tag (Mo-So):

| Service | Pro Lauf | Pro Monat |
|---|---|---|
| Anthropic Claude | $0.05 - 0.15 | **$2 - 5** |
| OpenAI Whisper | $0.006 | **$0.20** |
| Notion | gratis | **$0** |
| Pexels | gratis | **$0** |
| Railway Hosting | — | **$5** (Hobby-Plan) |
| **GESAMT** | | **~$8 - 12 / Monat** |

→ Eine Story-Konversion (1× Bio-Check-Anmeldung → später 1× Säule-3-Käufer = CHF 333) deckt 30+ Monate Bot-Kosten.

---

## ⏭️ Nächste Schritte nach Setup

Sobald alle Keys in `.env` sind:

1. **Setup-Check:** `python config.py` → `✅ Setup OK`
2. **Bot lokal testen:** `python bot.py` (läuft im Vordergrund)
3. **Railway-Deploy:** `python deploy_to_railway.py`
4. **24/7-Betrieb:** Bot läuft auf Railway, unabhängig von deinem PC

Plus: Du sagst mir Bescheid wenn alle 3 Keys da sind, dann starte ich die nächste Implementations-Stage (notion_reader + claude_caller + render_caller + transcribe + task_daily_story).

---

## ❓ FAQ

**Brauche ich eine Kreditkarte?**
Anthropic + OpenAI: ja, mindestens für initiale $5-Einzahlung.
Notion + Pexels: nein, gratis.

**Was wenn ich keine Sprachnotizen nutzen will?**
Dann lass `OPENAI_API_KEY` leer. Bot funktioniert mit Text-Antworten.

**Was wenn der Bot Notion-DB-Zugriff verliert?**
In notion.so/profile/integrations checken ob Integration noch existiert. Plus prüfen ob die DB die Connection noch hat (kann nach Notion-Updates wegfallen).

**Wie viel Token verbraucht eine Story?**
Eine 8-Slide-Story-Generierung braucht ca. 5'000 Input-Token + 2'000 Output-Token = ca. $0.05.
