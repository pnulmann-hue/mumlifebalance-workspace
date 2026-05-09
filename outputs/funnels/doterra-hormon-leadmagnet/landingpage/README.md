# Hormon-Typ Quiz Landingpage

**Status:** Code-fertig, ready für Netlify-Deploy
**Erstellt:** 2026-05-08
**Erwartete URL:** mumlifebalance.ch/hormon (oder Subdomain — siehe „Deploy-Optionen")

## Was das ist

Eine vollständige Static-Site für den doTERRA-Lead-Magnet-Funnel. 5 HTMLs + 1 CSS + 1 JS + Config — keine externen Quiz-Tools, keine iframes, keine Tally-Integration.

```
landingpage/
├── index.html                       ← Hero + Video + Quiz-Start
├── quiz.html                        ← 5-Fragen-Quiz mit Email-Form
├── result-energie-raeuberin.html    ← Ergebnis Typ 1 (Stress dominant)
├── result-mineral-maengelin.html    ← Ergebnis Typ 2 (Nährstoff-Mangel)
├── result-darm-detektivin.html      ← Ergebnis Typ 3 (Mikrobiom)
├── style.css                        ← Brand-System (Petrol/Creme/Orange/Dunkelblau)
├── quiz.js                          ← Quiz-Logik + Form-Submit
├── netlify.toml                     ← Auto-Deploy-Config
└── README.md                        ← (diese Datei)
```

## Deploy-Optionen

### Option A: Subdomain via Netlify (am einfachsten)
1. Netlify-Site mit GitHub-Repo verbinden, **Base directory: `outputs/funnels/doterra-hormon-leadmagnet/landingpage`**
2. Custom domain: `hormon.mumlifebalance.ch` in Netlify konfigurieren
3. DNS: CNAME `hormon` → `[your-netlify-app].netlify.app`
4. SSL läuft auto via Let's Encrypt
5. Live in 5 Min.

### Option B: mumlifebalance.ch/hormon via Netlify-Edge-Routing
Patricias Wunsch-URL. Komplexer, weil mumlifebalance.ch auf WordPress läuft.
1. WordPress muss mumlifebalance.ch/hormon NICHT serven (in WP keine Page mit slug `hormon` anlegen)
2. Netlify-Site deployen wie Option A
3. Reverse-Proxy via Netlify Edge oder Cloudflare Workers, der mumlifebalance.ch/hormon → Netlify-Site routet
4. Alternativ: WP-Plugin „Redirection" mit 302-Redirect von /hormon → hormon.mumlifebalance.ch (einfachste Variante)

**Empfehlung Patricia:** Subdomain (`hormon.mumlifebalance.ch`) — 0 DNS-Drama, funktioniert sofort.

### Option C: Direkt in bestehendes Netlify-Projekt
Falls du schon ein Netlify-Projekt für mumlifebalance hast: Files in den jeweiligen Repo-Pfad legen, deployen, Pfad-Routing in netlify.toml anpassen.

## ⚠️ Bevor du deployst — TODOs

### 1. Video einsetzen
In `index.html` unter `<!-- TODO Patricia: ... -->` deinen Video-Block einfügen:
- **Lokal hochgeladen:** `<video controls preload="metadata"><source src="patricia-intro.mp4"></video>` und MP4-File in den landingpage-Ordner legen
- **Vimeo-Hosted (empfohlen für 30-60s):** `<iframe src="https://player.vimeo.com/video/DEINE_VIDEO_ID" allowfullscreen></iframe>`
- **YouTube unlisted:** `<iframe src="https://www.youtube.com/embed/DEINE_VIDEO_ID?rel=0" allowfullscreen></iframe>`

### 2. PDF-Download verlinken
Das fertige PDF (`4-erkenntnisse-hormonchaos.pdf`) muss irgendwo öffentlich verfügbar sein:
- **Option 1 (einfach):** PDF in den landingpage/ Ordner legen — Netlify serviert es. URL: `/4-erkenntnisse-hormonchaos.pdf`
- **Option 2:** PDF in WordPress hochladen und Link in der Welcome-Mail (nicht auf der Result-Page nötig)

Aktuell wird das PDF NICHT auf der Result-Page direkt angeboten — sondern über die Welcome-Mail in AC. Wenn du das ändern willst: `<a href="/4-erkenntnisse-hormonchaos.pdf">PDF jetzt herunterladen</a>` in den 3 result-*.html ergänzen.

### 3. Email-Backend wählen

**Option A: Netlify Forms (einfachster Weg, sofort fertig)**
- Funktioniert out-of-the-box. Die Submissions landen in deinem Netlify-Dashboard unter „Forms"
- Du kannst Zapier/Make zu ActiveCampaign anbinden (~10 Min Setup)
- Nachteil: 1-Stunden-Delay zwischen Submit und AC-Eintragung möglich

**Option B: Direct AC-API via Netlify Function**
Wenn du echte Real-Time-Integration zu AC willst:
1. Erstelle Netlify Function `netlify/functions/submit-to-ac.js` (Beispiel-Code unten)
2. Setze `AC_API_ENDPOINT = '/.netlify/functions/submit-to-ac'` in `quiz.js` (Zeile 22)
3. AC-API-Key als Netlify-Env-Variable: `ACTIVECAMPAIGN_API_TOKEN` und `ACTIVECAMPAIGN_API_URL`

**Beispiel Netlify Function (für Option B):**

```javascript
// netlify/functions/submit-to-ac.js
exports.handler = async function (event) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }
  const data = JSON.parse(event.body);
  const acUrl = process.env.ACTIVECAMPAIGN_API_URL;
  const acToken = process.env.ACTIVECAMPAIGN_API_TOKEN;

  const contactPayload = {
    contact: {
      email: data.email,
      firstName: data.firstName,
      fieldValues: [
        { field: 'HORMON_TYPE', value: data.type },
        { field: 'HORMON_TYPE_LABEL', value: data.typeLabel }
      ]
    }
  };

  const response = await fetch(`${acUrl}/api/3/contacts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Api-Token': acToken
    },
    body: JSON.stringify(contactPayload)
  });

  // Tagging via separate endpoint:
  // POST /api/3/contactTags mit { contactTag: { contact: ID, tag: TAG_ID } }

  return {
    statusCode: response.ok ? 200 : 500,
    body: JSON.stringify({ success: response.ok })
  };
};
```

### 4. ManyChat-Trigger anpassen
Wenn die Site live ist, in ManyChat den HORMON-Trigger aktualisieren:

```
DM-Text:
Hey [first_name] 💜

Hier ist dein Quiz — sag mir wer du bist und ich schick dir dein
personalisiertes Ergebnis + 12-Seiten-Mini-Buch:

👉 https://hormon.mumlifebalance.ch (oder deine finale URL)

Patricia
```

### 5. AC-Drip-Sequenzen anlegen
Pro Hormon-Typ (Energie-Räuberin / Mineral-Mängelin / Darm-Detektivin) eine 3-Tages-Drip-Sequenz, getriggert durch das Tag `hormon-typ-[id]`. Drip-Texte sind in `outputs/funnels/doterra-hormon-leadmagnet/leadmagnet-komplett.md` Section 2 — du kannst sie als Vorlage nehmen und pro Typ anpassen (1-2 Sätze typ-spezifisch oben).

## Tests vor Go-Live

1. ☐ **Lokal-Test:** `cd landingpage && python3 -m http.server 8000` → http://localhost:8000 → Quiz durchspielen, Form-Submit prüft sessionStorage
2. ☐ **Netlify-Preview:** Pull Request öffnen → Netlify gibt Preview-URL → Quiz testen
3. ☐ **Mobile-Test:** Quiz auf iPhone + Android öffnen — alle Buttons tappable, Progress-Bar smooth
4. ☐ **Email-Test:** Selbst Quiz machen mit eigener Email → prüfen ob Lead in Netlify Forms / AC ankommt
5. ☐ **Result-Pages:** Alle 3 result-*.html direkt aufrufen — Layout, Texte, CTAs prüfen
6. ☐ **Spam-Test:** Honey-Pot-Field „bot-field" funktioniert? Bot-Submission ablehnen?

## Quiz-Logik kurz erklärt

**5 Fragen × 4 Optionen × Punkte für 3 Typen:**
- Energie-Räuberin (er): Stress + Schlaflosigkeit dominant
- Mineral-Mängelin (mm): Nährstoffmangel + Müdigkeit
- Darm-Detektivin (dd): Mikrobiom + Hormon-Recycling

Jede Option vergibt 0-3 Punkte pro Typ. Höchste Summe = Result.

Code: `quiz.js`, Funktion `computeType()`. Punkte stehen in der Konstante `QUESTIONS` als `weights: { er, mm, dd }`. Wenn du Texte oder Wertungen ändern willst — direkt im `QUESTIONS`-Array.

## Brand-Specs

| Element | Wert |
|---------|------|
| Petrol (primary) | `#12828c` |
| Dunkelblau (text) | `#29556d` |
| Creme (background) | `#f1ecdd` |
| Orange (accent) | `#dc822e` |
| Headlines | Philosopher (Google Fonts) |
| Body | Source Sans 3 (Google Fonts) |
| Max-Width Content | 720px (für Lesbarkeit) |

## Anpassungen ohne Code

Texte ändern: in den HTMLs direkt. Die Files sind kommentar-arm und gut lesbar.
Quiz-Fragen ändern: `quiz.js` Zeilen 24-94 (Konstante `QUESTIONS`).
Result-Page-Texte ändern: `result-*.html` direkt.
Branding ändern: `style.css` Zeilen 6-10 (CSS-Custom-Properties).

## Re-Deploy

Bei Code-Änderung: einfach committen + pushen. Netlify deployt automatisch.
