---
description: WordPress-Helfer für mumlifebalance.ch — Seiten erstellen, aktualisieren, Medien hochladen, Menüs pflegen
---

# /wp — WordPress-Helfer

Du hast über die WordPress REST API vollen Admin-Zugriff auf **mumlifebalance.ch**. Credentials stehen in `scripts/wordpress/.env` (wird nie committed).

## Aufgabe verstehen

Der User gibt dir natürlich-sprachliche WordPress-Aufgaben:

- „Erstelle eine Angebotsseite für [Produkt]"
- „Aktualisiere die Über-mich-Seite mit [Text]"
- „Lade [Foto] hoch und nutze es auf [Seite]"
- „Liste alle Seiten auf"
- „Welche Seiten enthalten das Wort 'Newsletter'?"
- „Veröffentliche die Seite [slug]"
- „Zeig mir die Bio-Check-Seite"
- „Erstelle einen neuen Blog-Beitrag über [Thema]"

## Tools die du nutzt

**1. CLI-Helper (`scripts/wordpress/wp-api.js`):**
```bash
cd scripts/wordpress
node --env-file=.env wp-api.js <command> [args]
```

Commands:
- `whoami` — prüft Login
- `list-pages [search]` — alle Seiten
- `get-page <id-or-slug>` — Details einer Seite
- `set-status <id> <publish|draft|private|trash>`
- `delete-page <id>`
- `upload-media <pfad> [titel]` — Datei hochladen
- `list-media [search]`
- `list-menus`

**2. Für komplexe Ops (Seiten mit HTML-Content, Medien + Seiten kombiniert):** JavaScript-Script in `scripts/wordpress/` anlegen und als Module auf `wp-api.js` zugreifen.

Beispiel-Script:
```js
import { createOrUpdatePage, uploadMedia } from './wp-api.js';

const media = await uploadMedia('./bild.jpg', { title: 'Hero Foto' });
const page = await createOrUpdatePage({
  title: 'Meine Angebotsseite',
  slug: 'mein-angebot',
  content: `<!-- wp:html -->\n<div>Dein HTML mit ${media.source_url}</div>\n<!-- /wp:html -->`,
  status: 'draft',  // erst als Entwurf, User publiziert selbst
});
```

## Ausführen

```bash
cd scripts/wordpress && node --env-file=.env mein-script.js
```

## Wichtige Regeln

1. **Neue Seiten immer als `status: draft`** — User prüft Vorschau, publiziert selbst (es sei denn User sagt explizit „veröffentlichen")

2. **Schaufenster-Metapher + Patricia-Voice bei Content-Generierung:** Sieh `~/.claude/projects/.../memory/feedback_brand-metaphern-patricia.md`, `context/brand-voice.md`, `context/brand-identity.md` — für alle Landingpages/Angebotsseiten nutze Creme-Hintergrund (#f1ecdd), Philosopher (Heading) + Source Sans 3 (Body), Schaufenster-Metapher ("violettes Kleid + Schuhladen") und **Transformation statt Features**.

3. **HTML-Block-Template** (wrap deinen Content in diesen Gutenberg-Block, damit WP das HTML durchreicht):
```
<!-- wp:html -->
[DEIN HTML]
<!-- /wp:html -->
```

4. **Fotos aus `context/Shootingbilder/`** nutzen wenn passend — 100+ authentische Patricia-Shootingbilder sind dort.

5. **Existierende Seiten prüfen** bevor du neue anlegst:
```bash
node --env-file=.env wp-api.js list-pages
```
→ Dann `createOrUpdatePage()` — findet via Slug und updatet, falls da.

6. **Brand-Farben (Hex):**
- Petrol `#12828c`
- Dunkelblau `#29556d`
- Creme `#f1ecdd`
- Orange `#dc822e`
- Text `#0c1c30`

7. **Nach jeder Seite: kurz zusammenfassen** was gemacht wurde und Vorschau-URL geben.

## Beispiele

### Beispiel 1 — Liste holen
User: „Welche Seiten hab ich auf WP?"
Du: Führst `node --env-file=.env wp-api.js list-pages` aus und antwortest mit der Liste.

### Beispiel 2 — Seite veröffentlichen
User: „Setz die Bio-Check-Seite live"
Du: `node --env-file=.env wp-api.js list-pages bio-check` → finde ID → `node --env-file=.env wp-api.js set-status <id> publish`

### Beispiel 3 — Neue Angebotsseite
User: „Bau mir eine Angebotsseite für Expertin statt Verkäuferin, Preis 97 CHF, Thrivecart-Link https://..."

Du:
1. Schreibst ein neues Script `deploy-expertin-angebot.js` mit HTML-Template in Patricia-Voice (Schaufenster-Metapher, Transformation-Sprache)
2. Lädst ggf. Foto hoch
3. Erstellst Seite als Draft
4. Gibst User die Vorschau-URL
5. Fragst: „Wenn's passt, soll ich veröffentlichen?"

## Troubleshooting

- **401/403 Error** → App Password rotiert? → User bitten neues zu erstellen, `.env` updaten
- **404 bei Seiten-URL** → Status ist draft, erst publishen
- **Styles zerschossen** → Theme wraper stört? → Template `elementor_canvas` probieren oder volle Breite aktivieren
- **Foto zu gross** → Compression mit Sharp vor Upload (optional)
