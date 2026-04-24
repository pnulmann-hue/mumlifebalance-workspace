# Kurs-Transkription

Zwei Wege — wähle nach Situation:

## 🎯 Weg 1 — Vimeo-Transkripte direkt ziehen (empfohlen, kostenlos)

Wenn die Videos auf **Vimeo** gehostet sind (typisch für Julia-Trost-Kurse, Teachable etc.).

**Vorteile:**
- Kein Video-Download nötig (spart GB)
- Keine API-Kosten (Vimeo-Auto-Untertitel sind gratis)
- Funktioniert mit Chrome-Cookies für private Kurse

**Voraussetzungen:**
- `yt-dlp` installiert (`pip install yt-dlp` oder `winget install yt-dlp`)
- In Chrome auf der Kurs-Plattform eingeloggt (yt-dlp liest die Cookies)

**Schritte:**
1. **Vimeo-URLs sammeln** — Liste in `.txt`-Datei, eine pro Zeile:
   ```
   # Werbeanzeigen-Kurs Julia Trost
   https://vimeo.com/1234567890
   https://vimeo.com/1234567891
   ```
   Die Vimeo-URLs findest du in Chrome: F12 (DevTools) → Network-Tab → Video abspielen → Suche nach `player.vimeo.com/video/[id]`
2. **Script laufen lassen:**
   ```bash
   cd "scripts/transcribe"
   node fetch-vimeo-transcripts.js \
     vimeo-urls-werbeanzeigen.txt \
     "../../reference/julia-trost/Transkripte Videocalls/_sortiert/Werbeanzeigen"
   ```
3. **Transkripte prüfen** — landen als `.txt` im Zielordner.

---

## 🎯 Weg 2 — Lokale Videos mit Whisper transkribieren (wenn kein Vimeo)

Wenn du MP4-Files hast (z.B. weil der Anbieter nicht auf Vimeo hostet).

Videos aus Julia-Trost-Kursen (oder anderen) automatisch transkribieren.

## Einmalige Installation

1. **ffmpeg installieren** (einmal, systemweit)
   - Windows: `winget install ffmpeg`
   - Mac: `brew install ffmpeg`
   - Test: `ffmpeg -version` im Terminal
2. **OpenAI-API-Key** holen: https://platform.openai.com/api-keys → in `.env` eintragen

## Kurs transkribieren — 3 Schritte

### 1. Videos herunterladen (manuell, dauert je nach Kurs 10-30 Min)

- **Browser-Extension:** Video DownloadHelper oder FlixGrab
- Jedes Kurs-Video abspielen → Extension-Icon → MP4 speichern
- **Speicher-Ordner:** `reference/julia-trost/[Kursname]-Videos/`
- **Benennung:** `01-einleitung.mp4`, `02-...`, `03-...` etc. (Nummern vorne für Reihenfolge)

### 2. Script laufen lassen

```bash
cd "C:/Users/pnulm/Desktop/Mein Business/scripts/transcribe"

# Beispiel fuer den Werbeanzeigen-Kurs:
node --env-file=.env transcribe.js \
  "../../reference/julia-trost/Werbeanzeigen-Videos" \
  "../../reference/julia-trost/Transkripte Videocalls/_sortiert/Werbeanzeigen"
```

Das Script:
- Überspringt Videos die schon transkribiert sind
- Extrahiert Audio mit ffmpeg (kurze MP3s, 16kHz mono)
- Schickt zu OpenAI Whisper API
- Speichert Transkripte als `.txt` im Zielordner

### 3. Aufräumen

Nach erfolgreicher Transkription kannst du den Video-Ordner löschen (Videos sind gross, Transkripte sind klein).

## Kosten

Whisper API kostet **0.006 USD pro Audio-Minute**.

- Kurs mit 25 Videos × 10 Min = 250 Min = ~1.50 USD
- Kurs mit 50 Videos × 8 Min = 400 Min = ~2.40 USD

## Fehlerbehebung

**„ffmpeg nicht gefunden":**
- Windows: Pfad zu ffmpeg.exe in PATH eintragen, Terminal neu starten
- Test: `ffmpeg -version`

**„Whisper API 401":**
- Key stimmt nicht → neu kopieren aus https://platform.openai.com/api-keys

**„Whisper API 413 (file too large)":**
- Whisper-API-Limit: 25 MB pro File
- Audio wird bereits auf 32 kbps komprimiert → reicht für bis zu ~100 Min
- Falls längeres Video: manuell mit `ffmpeg -ss` teilen
