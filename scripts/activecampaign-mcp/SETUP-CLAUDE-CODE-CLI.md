# Claude Code CLI lokal mit AC-MCP einrichten

**Zweck:** Claude Code lokal auf dem Mac so einrichten, dass er **direkt mit ActiveCampaign reden kann** — Campaigns erstellen, Tags setzen, Automations bauen, ohne Copy-Paste.

**Zeitaufwand:** 30-60 Min (einmalig)
**Ergebnis:** Patricia sagt „Erstelle Campaign mit Subject XYZ" → Claude legt sie direkt in AC an.

---

## Voraussetzungen

- Mac mit macOS (oder Windows/Linux)
- Terminal (auf Mac: Programme → Dienstprogramme → Terminal)
- Node.js 18+ installiert (Test: `node --version` im Terminal — wenn Fehler: https://nodejs.org)
- ActiveCampaign-Account mit API-Zugang (hast du)

---

## Schritt 1 — Claude Code CLI installieren (5 Min)

Im Terminal eingeben:
```bash
npm install -g @anthropic-ai/claude-code
```

Test:
```bash
claude --version
```
Sollte eine Version zeigen.

**Erste Anmeldung:**
```bash
claude
```
→ Browser öffnet sich → Login mit Anthropic-Account (gleicher wie deine Web-Claude-Anmeldung).

---

## Schritt 2 — Workspace lokal klonen (5 Min)

Du brauchst den Workspace-Code lokal damit Claude Code darin arbeiten kann:

```bash
cd ~
git clone https://github.com/pnulmann-hue/mumlifebalance-workspace.git
cd mumlifebalance-workspace
```

(Falls SSH-Key benötigt: GitHub → Settings → SSH-Keys einrichten, oder HTTPS mit Personal Access Token.)

---

## Schritt 3 — AC-API-Token besorgen (3 Min)

1. Login bei **mumlifebalance.activehosted.com**
2. Oben rechts: dein Profil-Icon → **„Mein Account"**
3. Links: **„Entwickler"** (oder „Developer")
4. Du siehst:
   - **API URL:** z.B. `https://mumlifebalance.api-us1.com`
   - **API Key:** lange Zahlen-Buchstaben-Kombination
5. Beide kopieren

---

## Schritt 4 — AC-MCP-Server konfigurieren (5 Min)

Im Workspace-Ordner:
```bash
cd scripts/activecampaign-mcp
npm install
```

`.env`-Datei erstellen:
```bash
nano .env
```

Eintragen:
```
AC_API_URL=https://mumlifebalance.api-us1.com
AC_API_KEY=DEIN-TOKEN-VON-OBEN
```

Speichern (Ctrl+O, Enter, Ctrl+X bei nano).

**Test:**
```bash
node --env-file=.env index.js
```
Sollte Server starten ohne Fehler. Wenn ja: Ctrl+C zum Stoppen.

---

## Schritt 5 — MCP in Claude Code registrieren (5 Min)

Öffne `~/.claude/mcp.json` (oder erstelle wenn nicht vorhanden):
```bash
nano ~/.claude/mcp.json
```

Eintragen (oder zu bestehender Config hinzufügen):
```json
{
  "mcpServers": {
    "activecampaign": {
      "command": "node",
      "args": [
        "--env-file=/Users/DEIN-USERNAME/mumlifebalance-workspace/scripts/activecampaign-mcp/.env",
        "/Users/DEIN-USERNAME/mumlifebalance-workspace/scripts/activecampaign-mcp/index.js"
      ]
    }
  }
}
```

⚠️ Ersetze `/Users/DEIN-USERNAME/` mit deinem tatsächlichen Pfad. Test mit:
```bash
echo $HOME
```

---

## Schritt 6 — Test (5 Min)

```bash
cd ~/mumlifebalance-workspace
claude
```

In der Claude-Code-Session tippen:
```
Liste mir alle ActiveCampaign-Listen
```

→ Wenn Claude Listen aus AC zeigt: ✅ es funktioniert!

Dann kannst du Sachen fragen wie:
- „Erstelle eine Campaign mit Subject XYZ und Body aus Datei `webinar-mails/01-bestaetigung.html`"
- „Setze Tag `mama-ceo-webinar-anmeldung` auf Kontakt mit E-Mail xyz@example.com"
- „Liste alle Automations"
- „Erstelle eine neue Automation die bei Tag XYZ getriggert wird"

---

## Was AC-MCP aktuell kann (Stand `index.js`)

Schau in `scripts/activecampaign-mcp/index.js` für die volle Liste der unterstützten Operationen. Typischerweise:
- Lists abrufen + erstellen
- Contacts abrufen + erstellen + tagging
- Campaigns abrufen + erstellen
- Automations abrufen
- Tags abrufen + setzen

Wenn was fehlt: AC-API-Doku auf https://developers.activecampaign.com/reference/overview — Funktion in `index.js` ergänzen.

---

## Troubleshooting

❌ **„Permission denied" bei npm install -g**
→ `sudo npm install -g @anthropic-ai/claude-code`

❌ **„Cannot find module @modelcontextprotocol/sdk"**
→ Im `scripts/activecampaign-mcp/` Ordner: `npm install` nochmal

❌ **„AC API 401: Authentication failed"**
→ AC-Token oder URL falsch in `.env`

❌ **Claude Code findet MCP-Server nicht**
→ Pfade in `~/.claude/mcp.json` sind absolute Pfade (mit /Users/DEIN-USERNAME/...), nicht relative

❌ **MCP startet aber Tools tauchen nicht auf**
→ Claude Code beenden (Ctrl+C) und neu starten — MCP-Server werden beim Start gelesen

---

## Alternative für später: API-Token via Web-Claude

Wenn du in Web-Claude (Browser) bleiben willst und doch AC nutzen, gibt's einen Workaround:
1. Du installierst einen lokalen MCP-Server bei dir auf dem Mac
2. Verbindest ihn mit Claude über einen Tunnel (ngrok oder ähnlich)
3. Claude.ai Settings → MCP-Connectors → URL eintragen

Aber das ist komplizierter und nicht so stabil. CLI lokal ist der saubere Weg.

---

## Zusammenfassung

**1× Setup (30-60 Min):** CLI installieren + Workspace klonen + Token einrichten + MCP registrieren
**Danach:** Claude Code kann AC direkt bedienen, jedes Mal wenn du `claude` startest

**Mein Tipp:** Mach das am Wochenende oder Abend wo du Ruhe hast. Nicht jetzt während Mai-Launch-Vorbereitung — Mails copy-paste in AC ist für jetzt schneller.

---

**Bei Problemen:** Sag mir wo's hängt + Screenshot/Fehlermeldung — wir lösen's.
