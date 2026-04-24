# Blotato Setup — Instagram Auto-Posting

Stand: 2026-04-21
Blotato-API liefert Auto-Posting für Reels + Karussells. Wird von der **täglichen Posting-Queue** (Scheduled Task) und von **/reels + /karussell** im Freigabe-Flow genutzt.

---

## Credentials

**Alle Secrets liegen in `.env` im Workspace-Root.**

```
BLOTATO_API_KEY=<siehe .env>
BLOTATO_BASE_URL=https://backend.blotato.com/v2
BLOTATO_ACCOUNT_ID_MENTORING=<einmalig abrufen, dann hier eintragen>
BLOTATO_ACCOUNT_ID_DOTERRA=<einmalig abrufen, dann hier eintragen>
```

**Niemals API-Key in Commits, Chats, oder Outputs schreiben.** Wenn er je in Logs/Chats landet: sofort in Blotato rotieren (Dashboard → Settings → API Keys → Regenerate).

---

## API-Grundlagen

**Base URL:** `https://backend.blotato.com/v2`
**Auth-Header:** `blotato-api-key: <KEY>`
**Content-Type:** `application/json`
**Rate-Limit:** siehe Blotato-Doku (grob 60 req/min)

---

## Schritt 1 — Account-IDs einmalig abrufen

Bevor das erste Mal gepostet wird, brauchen wir die Blotato-Account-IDs für **beide** Instagram-Profile (Mentoring + doTERRA).

### Curl-Befehl

```bash
curl -X GET "https://backend.blotato.com/v2/users/me/accounts" \
  -H "blotato-api-key: $BLOTATO_API_KEY"
```

### Erwartete Antwort (Auszug)

```json
{
  "accounts": [
    {
      "id": "98432",
      "platform": "instagram",
      "username": "mumlifebalance_patricia_ulmann",
      "displayName": "Mum Life Balance Mentoring"
    },
    {
      "id": "98433",
      "platform": "instagram",
      "username": "<doterra-handle>",
      "displayName": "..."
    }
  ]
}
```

→ Die beiden `id`-Werte in `.env` eintragen:
- Mentoring-Profil → `BLOTATO_ACCOUNT_ID_MENTORING`
- doTERRA-Profil → `BLOTATO_ACCOUNT_ID_DOTERRA`

---

## Schritt 2 — Post schedulen (Instagram Reel)

### Endpoint
`POST https://backend.blotato.com/v2/posts`

### Headers
```
Content-Type: application/json
blotato-api-key: <KEY>
```

### JSON-Body (Reel)

```json
{
  "post": {
    "accountId": "<BLOTATO_ACCOUNT_ID_MENTORING oder _DOTERRA>",
    "content": {
      "text": "Hier kommt die Caption inkl. Hashtags und Keyword-CTA",
      "mediaUrls": ["https://public-url-zum-video.mp4"],
      "platform": "instagram"
    },
    "target": {
      "targetType": "instagram",
      "mediaType": "reel"
    }
  },
  "scheduledTime": "2026-04-23T19:00:00+02:00"
}
```

### JSON-Body (Karussell — Multi-Bild)

```json
{
  "post": {
    "accountId": "<ACCOUNT_ID>",
    "content": {
      "text": "Caption inkl. Hashtags + Keyword-CTA",
      "mediaUrls": [
        "https://public-url/slide-1.png",
        "https://public-url/slide-2.png",
        "https://public-url/slide-3.png",
        "https://public-url/slide-4.png"
      ],
      "platform": "instagram"
    },
    "target": {
      "targetType": "instagram",
      "mediaType": "image"
    }
  },
  "scheduledTime": "2026-04-23T19:00:00+02:00"
}
```

### Wichtig
- `scheduledTime` muss **root-level** sein (nicht in `post` eingebettet!)
- ISO 8601 mit Zeitzone (`+02:00` für Europe/Zurich im Sommer, `+01:00` im Winter)
- `mediaUrls` muss **öffentlich erreichbare** URLs enthalten (Canva-Export ggf. über S3 / Cloudinary hosten)
- Wenn kein `scheduledTime` → sofortiger Post

---

## Schritt 3 — Media-Upload für Canva-Designs

Canva-Export liefert oft keine persistent öffentliche URL. Zwei Optionen:

### Option A: Blotato Presigned Upload
```
POST https://backend.blotato.com/v2/media/presigned-upload
```
Blotato generiert eine Upload-URL. Wir laden das File hoch, bekommen eine persistente URL zurück.

### Option B: Externes Hosting
Das exportierte Canva-File lokal speichern → zu Cloudinary / S3 / Bunny uploaden → public URL nutzen.

**Empfehlung**: Option A (Blotato Presigned Upload) — eine Integration weniger.

---

## Posting-Queue-Flow (täglich 07:00)

1. Canva-Ordner „Posting Queue" prüfen (via Canva MCP, `list-folder-items`)
2. Pro Design: Status-Check (Freigabe-Marker)
3. Wenn freigegeben:
   - Canva-Export via `export-design` (PNG für Karussell, MP4 für Reel)
   - Upload via Blotato Presigned Upload
   - `POST /v2/posts` mit scheduledTime = nächste Zielgruppen-Zeit
   - Design verschieben nach Canva-Ordner „Gepostete Beiträge"
   - Notion Content-Management aktualisieren (Status → „Veröffentlicht", Posting-Datum, URL)
4. Wenn nicht freigegeben: Design bleibt, nächste Runde

---

## Error-Handling

| Status | Bedeutung | Aktion |
|--------|-----------|--------|
| 401 | API-Key ungültig | Key in .env prüfen, ggf. rotieren |
| 400 | Falsches JSON / fehlende Felder | Request-Body loggen, Schema abgleichen |
| 429 | Rate-Limit | 60 Sek. warten, erneut versuchen |
| 500 | Blotato-Fehler | 2 Min. warten, dann erneut |

Bei Fehler: Design in „Posting Queue" lassen + Error-Eintrag in `outputs/reels/errors.log`.

---

## Test-Call zum Start

Vor Produktiv-Nutzung einmal testen:

```bash
# 1) Accounts abfragen
curl -X GET "https://backend.blotato.com/v2/users/me/accounts" \
  -H "blotato-api-key: $(grep BLOTATO_API_KEY .env | cut -d= -f2)"

# 2) Test-Post (sofort, nicht scheduled, nur auf Mentoring)
curl -X POST "https://backend.blotato.com/v2/posts" \
  -H "Content-Type: application/json" \
  -H "blotato-api-key: $(grep BLOTATO_API_KEY .env | cut -d= -f2)" \
  -d '{
    "post": {
      "accountId": "<MENTORING_ID>",
      "content": {
        "text": "Testpost vom neuen Content-System 🚀",
        "mediaUrls": ["<public-image-url>"],
        "platform": "instagram"
      },
      "target": {
        "targetType": "instagram"
      }
    }
  }'
```

---

## Rotieren des Keys

Der aktuelle Key wurde am 2026-04-21 im Chat geteilt. Vor dem ersten Produktiv-Post:

1. https://app.blotato.com → Settings → API Keys
2. Auf „Regenerate" klicken
3. Neuen Key in `.env` ersetzen
4. Dokument hier **nicht** aktualisieren (der Key steht nur in .env)

---

## Quellen

- [Blotato API Quickstart](https://help.blotato.com/api/start)
- [Blotato Publish Post](https://help.blotato.com/api/publish-post)
- [Blotato API-Reference](https://help.blotato.com/api/api-reference)
