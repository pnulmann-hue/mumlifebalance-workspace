# IKM-Companion

Chat-Companion zum Kurs **Instagram-Kundenmaschine** von Patricia Ulmann
(Mum Life Balance). Zwilling von `bio-check-bot` / `freischaufeln` /
`produktwelt-companion`.

Live unter: `companion-ikm.mumlifebalance.ch`

## Was er tut

Setzt das Kurswissen der Instagram-Kundenmaschine auf das konkrete Profil
der Nutzerin um — Story-Ideen, Beitragsthemen, fertige Hooks, nächster
Schritt für die Woche. Optional Vision-Upload (Profil-Screenshot) für
konkretes Feedback.

## Aufbau

```
lib/system-prompt.md   Der komplette Brain: Persona + Kurswissen +
                       ZUSATZ-WERKZEUGKASTEN (Hook-Formeln, Caption-Formeln,
                       Kaufpsychologie, Floskel-Blackliste)
api/chat.js            Claude-Proxy — laedt nur lib/system-prompt.md
api/tag.js             ActiveCampaign-Tagging bei Pitch-Klick (optional)
api/health.js          Health-Check
public/                Chat-UI (index.html + styles.css + chat.js)
                       inkl. Vision-Upload + localStorage + Pitch-Marker
```

## Deployment (Vercel)

- **Root Directory:** `scripts/ikm-companion`
- **Production Branch:** `main`
- **Env-Variablen:**
  - `ANTHROPIC_API_KEY` (Pflicht) — Claude-API-Key
  - `AC_API_URL`, `AC_API_KEY`, `AC_TAG_*` (optional) — nur fuer
    ActiveCampaign-Tagging

Kein Key gehoert ins Repo. `.gitignore` blockt `API_KEY.txt`.

## Lokal testen

```bash
cd scripts/ikm-companion
npm install
cp .env.example .env   # ANTHROPIC_API_KEY eintragen
vercel dev
```
