---
tags: [content, montag-build]
---

# KW 19 Post-Plan · Karussells via Blotato + Reels manuell

**Stand:** 2026-05-06
**Plan:**

| Datum | Wochentag | Profil | Format | Slug | Status |
|---|---|---|---|---|---|
| **6.5.** | Mi 19:30 | doTERRA | Karussell D2 | hausarzt-wendepunkt | Heute Abend |
| **7.5.** | Do 19:30 | Mentoring | Karussell M9 | 3-uhr-liste | Morgen |
| **8.5.** | Fr 19:30 | doTERRA | Karussell D9 | echte-zeitlinie | |
| **9.5.** | Sa 19:30 | Mentoring | Karussell M7 | 3-jahre-nebenbei | |
| **10.5.** | So 19:30 | doTERRA | Karussell D8 | vor-wecker-auf | |
| **11.5.** | Mo 19:30 | Mentoring | Karussell M4 | 3-stunden-fokuszeit | |
| **12.5. / 13.5.** | Di | Beide | Reels R1 + R2 | (siehe Drehtag-Master) | |
| **14.5. / 15.5.** | Do | Beide | Reels R3 + R4 | (siehe Drehtag-Master) | |

---

## So planst du die 6 Karussells via Blotato

### Voraussetzungen (einmalig prüfen)

1. **`.env` im Workspace-Root** mit:
   ```
   BLOTATO_API_KEY=<dein Key>
   ```

2. **`scripts/wordpress/.env`** mit:
   ```
   WP_URL=https://mumlifebalance.ch
   WP_USER=patricia
   WP_APP_PASSWORD=<dein App-Password>
   ```

3. **Blotato Account-IDs** (sind in den Configs hardcoded):
   - Mentoring: `41414`
   - doTERRA: `41413`

> **Wichtig:** Web-Sandbox blockiert `mumlifebalance.ch` — also musst du das **lokal auf deinem PC** ausführen, nicht via Web-Claude.

### Befehl pro Tag (6×)

Aus deinem Terminal **lokal** im Workspace-Root:

**Mi 6.5. — D2 Hausarzt-Wendepunkt (heute Abend):**
```bash
cd scripts/blotato-post && node upload-and-schedule.js \
  --slides-dir="../../outputs/karussells/render-2026-05-04/doterra-monatsfokus-hausarzt-wendepunkt" \
  --config="post-configs/2026-05-06-mi-doterra-d2-hausarzt.json"
```

**Do 7.5. — M9 3-Uhr-Liste:**
```bash
cd scripts/blotato-post && node upload-and-schedule.js \
  --slides-dir="../../outputs/karussells/render-2026-05-04/mentoring-monatsfokus-3-uhr-liste" \
  --config="post-configs/2026-05-07-do-mentoring-m9-3-uhr-liste.json"
```

**Fr 8.5. — D9 Echte Zeitlinie:**
```bash
cd scripts/blotato-post && node upload-and-schedule.js \
  --slides-dir="../../outputs/karussells/render-2026-05-04/doterra-monatsfokus-echte-zeitlinie" \
  --config="post-configs/2026-05-08-fr-doterra-d9-echte-zeitlinie.json"
```

**Sa 9.5. — M7 3 Jahre Nebenbei:**
```bash
cd scripts/blotato-post && node upload-and-schedule.js \
  --slides-dir="../../outputs/karussells/render-2026-05-04/mentoring-monatsfokus-3-jahre-nebenbei" \
  --config="post-configs/2026-05-09-sa-mentoring-m7-3-jahre-nebenbei.json"
```

**So 10.5. — D8 Vor Wecker auf:**
```bash
cd scripts/blotato-post && node upload-and-schedule.js \
  --slides-dir="../../outputs/karussells/render-2026-05-04/doterra-monatsfokus-vor-wecker-auf" \
  --config="post-configs/2026-05-10-so-doterra-d8-vor-wecker-auf.json"
```

**Mo 11.5. — M4 3 Stunden Fokuszeit:**
```bash
cd scripts/blotato-post && node upload-and-schedule.js \
  --slides-dir="../../outputs/karussells/render-2026-05-04/mentoring-monatsfokus-3-stunden-fokuszeit" \
  --config="post-configs/2026-05-11-mo-mentoring-m4-3-stunden-fokuszeit.json"
```

### Was passiert pro Aufruf

1. Skript lädt alle `slide-01.png` … `slide-10.png` zu **deiner WordPress Media-Library** hoch (10 URLs)
2. Schreibt die WP-URLs in das Config-JSON zurück
3. Ruft Blotato `POST /v2/posts` mit `scheduledTime` auf
4. Blotato fetcht die Bilder von WP, hostet sie permanent, schedulet den Post

**Bei Erfolg:** Post-ID kommt zurück → Post ist eingeplant.
**Bei Fehler:** Skript bricht ab + zeigt Fehler. Häufige Ursachen: WP-Login falsch, Blotato-Key abgelaufen, `mediaUrls` schon gefüllt (Skript schreibt nur leeres Array).

---

## ManyChat-Keywords vorbereiten (vor dem ersten Post!)

| Keyword | Profil | DM-Inhalt |
|---|---|---|
| **WENDEPUNKT** | doTERRA | Wendepunkt-Story + Schritt-1-Hint / Link Energie-Kur |
| **MENTAL** | Mentoring | 3-Listen-Auslagern-Workbook oder kurzes Erklär-Video |
| **GETRENNT** | Mentoring | Kalender-Vorlage „3-Stunden-Fokuszeit schützen" |
| **WEBINAR** | Mentoring | Webinar-Anmeldelink „In 90 Min dein Mama-Leben mit KI-Assistenten umkrempeln" |
| **REALITÄT** | Mentoring | Mama-CEO-Setup-Video (für R2) |
| **KI** | Mentoring | KI-Stack-Übersichts-Video (für R4) |

→ **Pflicht-Check vor 19:30 heute:** WENDEPUNKT-Auto-DM funktioniert (für D2 Hausarzt heute Abend).

---

## Reels — separater Drehtag-Master

Siehe `outputs/reels/KW19-DREHTAG-MASTER.md` für:
- Sek-genaue Texte für alle 4 Reels (R1 D1, R2 M6, R3 D3, R4 M10)
- Setting-Tipps + Pausen-Markierungen
- Caption-Vorschläge
- Cover-PNG-Pfade
- ManyChat-Keyword-Liste

**Empfohlene Drehtag-Reihenfolge:** R1 → R2 → R3 (alle Talking-Head, eine Sitzung) · R4 separat (B-Roll mit Voiceover, Hausarbeit-tauglich).
