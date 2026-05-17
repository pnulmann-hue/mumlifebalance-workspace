# Railway-Deploy — Story-Render-Bot

**Status:** Bot ist deploy-ready. Bundle gebaut (285 MB), nixpacks konfiguriert, Render-Pipeline self-contained.

**Was du machst:**
1. Bundle ist schon gebaut (`scripts/content-assistent/_bundle/`, 30 Shootingbilder + 652 Stock + .md)
2. Push zum GitHub
3. Railway-Service erstellen + verbinden
4. Env-Vars eintragen
5. Auto-Deploy startet

**Dauer:** ~10 Min Setup, ~5 Min Build.

---

## Schritt 1: Bundle aktualisieren (falls nötig)

Wenn du neue Shootingbilder dazugeben willst:

```powershell
cd "C:\Users\pnulm\Desktop\Mein Business\scripts\content-assistent"
python build_bundle.py --refresh
```

Das löscht das alte Bundle und baut neu (30 gleichverteilte Shootingbilder, alle Stock-Fotos, alle doTERRA-mds).

---

## Schritt 2: Git Push

```powershell
cd "C:\Users\pnulm\Desktop\Mein Business"
git add scripts/content-assistent/
git add .gitignore
git commit -m "Story-Render-Bot Railway-ready: Bundle + Sparring + Anti-Halluzination"
git push
```

**Wichtig:** Push wird ~285 MB hochladen — dauert je nach Internet 2-10 Min.

---

## Schritt 3: Railway-Service erstellen

### Option A — Web-UI (empfohlen)

1. https://railway.app → Login
2. **+ New Project** → **Deploy from GitHub repo**
3. Wähle `pnulmann-hue/mumlifebalance-workspace` (oder dein Hauptrepo)
4. **Configure** klicken
5. **Settings → Source**:
   - Root Directory: `scripts/content-assistent`
   - Build Command: leer lassen (nixpacks erkennt automatisch)
   - Start Command: leer lassen (Procfile sagt `python bot.py`)
6. **Settings → Variables** → folgende eintragen:

```
TELEGRAM_CONTENT_BOT_TOKEN=8690883253:AAH... (aus deiner .env)
TELEGRAM_CHAT_ID=5097782438
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-proj-...
NOTION_API_KEY=ntn_...
PEXELS_API_KEY=...
```

(Alle Werte aus deiner lokalen `.env` — kopier-paste)

7. **Deploy** klickt automatisch los

### Option B — CLI

```powershell
# Railway-CLI installieren (einmalig)
winget install Railway.CLI

cd "C:\Users\pnulm\Desktop\Mein Business\scripts\content-assistent"
railway login
railway link            # → wähle dein Projekt + erstelle Service
python deploy_to_railway.py
```

---

## Schritt 4: Build beobachten

In Railway → dein Service → **Deployments** → Logs ansehen.

**Erwartete Ausgabe:**
```
[BUNDLE-SETUP] context/ ist leer — entpacke _bundle/ nach context/
[BUNDLE-SETUP]   symlink Shootingbilder
[BUNDLE-SETUP]   symlink stock-fotos
[BUNDLE-SETUP]   symlink doTERRA
[BUNDLE-SETUP]   18 context-Dateien kopiert
[BUNDLE-SETUP] Fertig.
[INFO] Setup OK — Bot startet.
[INFO] Scheduler aktiv: Mo-So 06:30 Europe/Zurich
[INFO] Telegram-Polling aktiv. Bot ist online.
```

---

## Schritt 5: Erster Test

Sobald „Bot ist online" in den Logs:

1. Telegram → Bot → `/status`
   → sollte Bot-Info zeigen
2. `/run` (Sparring-Modus)
   → Bot stellt 5 Fragen
3. Per Sprachnotiz antworten
4. `/generieren`
   → Bot baut Story + sendet 8 Slides

---

## Schritt 6: Lokalen Bot stoppen

Du brauchst den lokalen `start_bot.bat` nicht mehr — Railway läuft 24/7. Stop alle lokalen Bot-Instanzen.

---

## Troubleshooting

### Build-Fehler „chromium not found"

→ nixpacks.toml prüfen, `chromium` muss in `nixPkgs` stehen.

### Bot crasht beim Start

→ Logs lesen. Häufigste Ursachen:
- Env-Var fehlt → check Railway-Variables
- `_bundle/` fehlt → erneut `python build_bundle.py` lokal + git push

### Telegram-Bot reagiert nicht

→ Logs zeigen ob Polling aktiv. Wenn nicht: Token falsch oder Patricia-Chat-ID falsch.

### Foto-Pfade in HTML brechen

→ `_setup_bundle_if_needed()` sollte `context/Shootingbilder/` erzeugen. Wenn nicht:
- Auf Railway: Volume-Permission-Issue → `permanently mountierte` `context/` als Volume?
- Or: Symlinks deaktiviert → Container nutzt copytree (langsamer aber funktioniert)

### Build dauert ewig

→ Erste Build = ~5 Min (Chromium-Download + npm install). Folgebuilds = ~1 Min (cached).

---

## Kosten-Übersicht (Railway)

| Plan | Preis | Was Du kriegst |
|---|---|---|
| **Hobby** | $5/Mo | 500h Compute, $5 Usage-Credit, 1 GB RAM, 100 GB Outbound |
| **Pro** | $20/Mo | unbegrenzte Compute, Volumes, Teams |

**Für Story-Bot reicht Hobby** — er läuft 24/7, braucht aber nur kurz CPU bei Trigger (06:30 + manuelle /run). Erwartete Compute-Kosten: ~$2-3/Mo. **Effektive Hosting = $5/Mo** (Hobby-Base-Fee).

---

## Update deployen

Bei Code-Änderungen:

```powershell
cd "C:\Users\pnulm\Desktop\Mein Business"
git add scripts/content-assistent/
git commit -m "Update: <was hast du geaendert>"
git push
```

Railway baut + deployed automatisch (~1 Min).

---

## Alte lokale Setup deaktivieren

Sobald Railway läuft:

1. Beende `start_bot.bat` falls offen
2. Lösche Windows-Aufgabenplanung-Eintrag (falls eingerichtet)
3. Falls `bot.py` als Startup-Item: `shell:startup` → Verknüpfung löschen
