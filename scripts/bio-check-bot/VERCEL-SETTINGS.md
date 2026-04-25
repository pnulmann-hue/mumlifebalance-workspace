# Vercel-Settings für Bio-Check-Bot

> **Single Source of Truth** für alle Vercel-Projekt-Settings.
> Wenn der Bot kaputt geht → zuerst hier abgleichen.

Diese Settings sind **NICHT im Code** gespeichert (Vercel-Cloud-Setting), nur im Vercel-Dashboard. Wenn sie verloren gehen (Repo-Reconnect, manuelles Reset, neues Projekt) → Bot kaputt mit 404.

---

## Pflicht-Settings im Vercel-Dashboard

**Pfad:** vercel.com → Bio-Check-Bot → Einstellungen → Allgemein (oder Build & Deployment)

| Setting | Wert | Was passiert wenn falsch |
|---|---|---|
| **Stammverzeichnis (Root Directory)** | `scripts/bio-check-bot` | 404 auf allen URLs (Vercel findet kein `index.html`) |
| **Framework Preset** | `Other` | Build-Fehler (Vercel versucht falsches Framework) |
| **Build Command** | (leer / Standard) | Optional |
| **Output Directory** | (leer / Standard) | Vercel erkennt `public/` automatisch |
| **Install Command** | `npm install` | Dependencies fehlen → Function-Errors |
| **Node.js Version** | `24.x` | Aktuelle Empfehlung |
| **Production Branch** | `main` | Nur Pushes auf main triggern Production-Deploy |

---

## Pflicht-Environment-Variables

**Pfad:** vercel.com → Bio-Check-Bot → Einstellungen → Umgebungsvariablen

Alle für **Production + Preview + Development** anhaken.

| Variable | Wert / Quelle |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic Console → API Keys (eigener Key, nicht doTERRA-Bot-Key wiederverwenden) |
| `BLOB_READ_WRITE_TOKEN` | Wird automatisch gesetzt durch `vercel blob create` |
| `AC_API_URL` | `https://mumlifebalance.api-us1.com` |
| `AC_API_KEY` | ActiveCampaign → Settings → Developer |
| `AC_TAG_LEAD` | `59` |
| `AC_TAG_COMPLETED` | `60` |
| `AC_TAG_THEMA` | `61` |
| `AC_TAG_EXPERTIN` | `62` |
| `AC_TAG_KUNDENMASCHINE` | `63` |
| `AC_TAG_INSTA_DM` | `64` |
| `AC_FIELD_PDF_URL` | (leer bis Phase 2 — Custom Field für PDF-URL) |

**Health-Check:** Wenn eine ENV fehlt, antwortet `/api/health` mit HTTP 503. UptimeRobot triggert dann Alarm.

---

## Custom Domains (optional)

| Domain | Status | DNS-Setup |
|---|---|---|
| `bio-check-bot.vercel.app` | Aktiv (Default Vercel) | — |
| `bio-check.mumlifebalance.ch` | Geplant Phase 3 | CNAME `bio-check` → `cname.vercel-dns.com` |

---

## Recovery-Steps wenn Bot 404 zeigt

1. **Health-Check pingen:** `https://bio-check-bot.vercel.app/api/health`
   - 200 OK → Bot lebt, Problem ist woanders (Mail-Link? Browser-Cache?)
   - 503 → Welche Checks fehlschlagen? Antwort lesen
   - 404 → Stammverzeichnis-Setting fehlt (siehe oben)
   - Timeout / DNS-Error → Vercel selbst down (rare)

2. **Vercel-Dashboard checken:**
   - Status der letzten Bereitstellung (grün = Bereit, rot = Fehler)
   - Bei Fehler → Build-Logs öffnen → Fehlermeldung lesen

3. **Stammverzeichnis prüfen:**
   - Einstellungen → finden / suchen nach „Stammverzeichnis"
   - Muss `scripts/bio-check-bot` sein
   - Falls leer oder falsch → korrigieren → speichern → „Wiederverlegen" mit deaktiviertem Build-Cache

4. **ENV-Variables prüfen:**
   - Einstellungen → Umgebungsvariablen
   - Liste aus `.env.example` durchgehen — alle gesetzt?

---

_Letztes Update: 2026-04-25_
