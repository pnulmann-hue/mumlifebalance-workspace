# Scheduled Task: Instagram Posting-Queue

**Name:** `instagram-posting-queue`
**Schedule:** Täglich 07:00 Europe/Zurich (Cron: `0 7 * * *`)
**Modell:** Sonnet
**Zweck:** Canva-Ordner „Posting Queue" prüfen, freigegebene Designs exportieren, via Blotato posten, Notion aktualisieren.

---

## Voraussetzungen

- Blotato-MCP ist verbunden ODER API-Calls via Bash/HTTP (aktuell: API-Key in `.env`, Calls via curl)
- Patricia hat `BLOTATO_ACCOUNT_ID_MENTORING` + `BLOTATO_ACCOUNT_ID_DOTERRA` in `.env` eingetragen
- Canva-Ordner `FAHG7yBZfpE` (Posting Queue) + `FAHG7-zV3Cw` (Gepostete Beiträge) existieren
- Notion Content-Management-DB (`collection://2ae7078e-8b7e-811a-ad14-000ba5820c09`) ist erreichbar

---

## Freigabe-Marker-Konvention

Ein Design in „Posting Queue" gilt als freigegeben, wenn:
- **Im Titel** das Kürzel `[OK]` enthalten ist (z.B. „Reel Mittwochs Hot-Take #12 [OK]")
- ODER **im Kommentar** das Wort „FREIGEGEBEN" steht
- ODER der **Notion-Status** bereits auf „Erstellung abgeschlossen" steht

Patricia markiert manüll. Nicht freigegebene Designs bleiben in der Queue.

---

## Prompt

```
Du bist die tägliche Posting-Queue-Automatisierung für Patricias Instagram (Mentoring + doTERRA).

## Schritt 1: Kontext laden
- `context/reels-framework.md` — Posting-Zeiten, Engagement-Routine
- `context/caption-formeln.md` — Caption-Struktur
- `context/manychat-keywords.md` — Keyword pro Pillar
- `context/brand-voice.md`
- `.env` — BLOTATO_API_KEY, BLOTATO_ACCOUNT_ID_MENTORING, BLOTATO_ACCOUNT_ID_DOTERRA

## Schritt 2: Posting Queue prüfen
Canva MCP: `list-folder-items` mit folder_id `FAHG7yBZfpE` (Posting Queue).

Wenn leer: Session beenden, nichts tun.

## Schritt 3: Pro Design

### 3.1 Freigabe-Check
Design ist freigegeben wenn:
- Titel enthält `[OK]`
- ODER Kommentar enthält „FREIGEGEBEN"
- ODER Notion-Eintrag Status = „Erstellung abgeschlossen"

**Nicht freigegebene Designs überspringen.** Am Ende Notification: „X Designs warten auf Freigabe".

### 3.2 Metadaten aus Notion holen
Suche in Content-Management-DB (`collection://2ae7078e-8b7e-811a-ad14-000ba5820c09`) nach Eintrag mit passendem Titel oder Canva-Link. Hole:
- Profil (Relation Content-Plattformen: Instagram Mentoring oder Instagram doTERRA)
- Pillar
- Content-Typ (Reel / Karussell)
- Caption (falls schon hinterlegt)
- ManyChat-Keyword

### 3.3 Caption generieren (falls nicht vorhanden)
Wenn Caption-Feld leer:
- Design-Inhalt lesen via Canva MCP `get-design-content`
- Caption generieren nach HVC-Formel (`caption-formeln.md`)
- Julia-Trost-Prinzipien: Transformation statt Features, Ziel statt Problem
- 1 CTA mit ManyChat-Keyword (aus `manychat-keywords.md` passend zur Pillar)
- 5 Hashtags (aus `reels-framework.md`)
- Erste 125 Zeichen müssen catchen (davor wird abgeschnitten)

### 3.4 Export via Canva MCP
- Reel: MP4-Video via `export-design` (Format: `mp4`, Qualität: `hd`)
- Karussell: Eine PNG pro Folie (Format: `png`)

### 3.5 Upload zu Blotato (Media-URL generieren)
Via Blotato Presigned Upload API:
```
POST https://backend.blotato.com/v2/media/presigned-upload
Header: blotato-api-key: <KEY>
```
Dann File hochladen, öffentliche URL zurück.

### 3.6 Post schedulen
Zielgruppen-Zeit bestimmen:
- Mentoring: nächster Di/Mi/Fr 21:00 (Swiss Time)
- doTERRA: nächster Mo/Mi/Sa 21:30 (Swiss Time)

API-Call:
```
POST https://backend.blotato.com/v2/posts
Header: Content-Type: application/json
Header: blotato-api-key: <KEY>

Body:
{
  "post": {
    "accountId": "<BLOTATO_ACCOUNT_ID_MENTORING oder _DOTERRA>",
    "content": {
      "text": "<Caption + Hashtags>",
      "mediaUrls": ["<public-url-aus-presigned-upload>"],
      "platform": "instagram"
    },
    "target": {
      "targetType": "instagram",
      "mediaType": "reel" (für Reels) oder "image" (für Karussell)
    }
  },
  "scheduledTime": "<ISO 8601 mit Zeitzone>"
}
```

### 3.7 Design verschieben (Canva)
Via `move-item-to-folder`: Design von Posting Queue nach „Gepostete Beiträge" (`FAHG7-zV3Cw`).

### 3.8 Notion aktualisieren
Content-Management-Eintrag:
- Status: „Veröffentlicht"
- Veröffentlichung: Posting-Datum + Zeit
- Caption (falls neu generiert): eintragen
- URL veröffentlicht: leer lassen (wird nach tatsächlichem Posten von Patricia gefüllt ODER via Instagram Graph API nachgetragen)

## Schritt 4: Max-Limit
Max 3 Posts pro Tag (Algorithmus-Rate-Limit). Wenn mehr freigegeben, die ältesten 3 zürst, Rest bleibt in Queue.

## Schritt 5: Fehler-Handling
Bei Fehler:
- Design in Posting Queue lassen
- Fehler-Eintrag in `outputs/posting-queue-errors.log` (Zeitstempel + Design-ID + Error)
- Notification an Patricia in Zusammenfassung

## Schritt 6: Zusammenfassung ausgeben

Am Ende der Session:
- Welche Designs wurden gepostet (Liste mit Posting-Zeit)?
- Welche Designs warten auf Freigabe (Liste)?
- Fehler aufgetreten?

Speichern als `outputs/posting-queue-log-YYYY-MM-DD.md`.

## Engagement-Reminder
Füge der Zusammenfassung folgenden Block hinzu (Patricia soll das manüll machen):

```
## Nach dem Posten — Deine Checkliste (erste Stunde!)
- [ ] Min. 30 Min am Handy bleiben
- [ ] Jeden Kommentar beantworten
- [ ] Reel/Karussell in Story teilen mit Frage-Sticker
- [ ] ManyChat-Automation checken (ist DM rausgegangen?)
- [ ] Bei >10 Views in 1. Minute: Screenshot für Archiv
```
```

---

## Modus „Halb-Automatik" (bis Blotato-IDs eingetragen sind)

Wenn `BLOTATO_ACCOUNT_ID_MENTORING` oder `_DOTERRA` in `.env` leer sind:
- Post-Schritte 3.5 + 3.6 UEBERSPRINGEN
- Statt dessen: Export-URL + Caption + Posting-Zeit in `outputs/posting-queue-pending-YYYY-MM-DD.md` schreiben
- Notification an Patricia: „X Posts sind bereit — bitte manüll in Instagram hochladen oder Blotato einrichten"

---

_Zuletzt aktualisiert: 2026-04-21_
