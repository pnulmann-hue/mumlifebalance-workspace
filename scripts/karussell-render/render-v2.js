/**
 * Karussell-Render V2 — Multi-Layout-Renderer für KW 19 (2026-05-04)
 *
 * Was es macht:
 *   1. Liest alle 6 Karussell-Briefings aus outputs/karussells/2026-05-04-*.md
 *   2. Liest alle 4 Reel-Briefings aus outputs/reels/2026-05-04-*-briefing.md
 *   3. Generiert HTML pro Karussell (Layout-Variante laut Pick-V2-File)
 *   4. Rendert PNG je Slide mit Puppeteer
 *
 * Layouts:
 *   V1 = Sauber-Statement (Petrol-Solid bzw. Orange-Solid für doTERRA)
 *        Kleiner Strich oben + Hero (Philosopher Bold) + Sub + Italic-Akzent
 *   V2 = Foto-Sticker (Hintergrund-Foto + Petrol-Sticker-Box am unteren Rand)
 *        Mit Top-Tag (MENTORING / VORMENOPAUSE)
 *   V3 = Magazin-Style (Creme + Top-Tag links + Slide-Nr-Kreis rechts + Hero + Italic-Quote)
 *
 * Brand-Akzente:
 *   Mentoring → Petrol (#12828c)
 *   doTERRA  → Orange (#dc822e)
 *
 * Output: outputs/karussells/render-2026-05-04/[profil]-[slug]/slide-XX.png
 *         outputs/reels/render-2026-05-04/[profil]-[slug]/cover.png
 *
 * Nutzung:
 *   node render-v2.js              → rendert ALLE Karussells + Reel-Cover
 *   node render-v2.js --batch      → wie oben (Alias)
 *   node render-v2.js --karussells → nur Karussells
 *   node render-v2.js --reels      → nur Reel-Cover
 *   node render-v2.js --slug=mentoring-monatsfokus-3-uhr-liste → ein einzelnes
 */

import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WORKSPACE_ROOT = path.resolve(__dirname, '..', '..');

const args = Object.fromEntries(
  process.argv.slice(2).map(arg => {
    const [k, ...rest] = arg.replace(/^--/, '').split('=');
    return [k, rest.join('=') || true];
  })
);

const RUN_KARUSSELLS = !args.reels || args.batch || args.karussells;
const RUN_REELS = !args.karussells || args.batch || args.reels;
const ONLY_SLUG = typeof args.slug === 'string' ? args.slug : null;

// ====================================================================
// FARBEN + LAYOUT-DEFINITIONEN
// ====================================================================

const COLORS = {
  creme: '#f1ecdd',
  petrol: '#12828c',
  dunkelblau: '#29556d',
  orange: '#dc822e',
  text: '#0c1c30',
  textSoft: 'rgba(12, 28, 48, 0.78)',
  cremeSoft: 'rgba(241, 236, 221, 0.85)',
};

// Welches Karussell hat welches Layout
// briefingDate-Property: erlaubt Briefings mit anderen Datums-Prefixes (KW20 = 2026-05-11)
// Default-briefingDate = '2026-05-04' (KW19)
const KARUSSELL_LAYOUTS = {
  // KW19 (2026-05-04)
  'mentoring-monatsfokus-3-uhr-liste':       { layout: 'V1', profil: 'mentoring' },                            // M9
  'mentoring-monatsfokus-3-jahre-nebenbei':  { layout: 'V3', profil: 'mentoring' },                            // M7
  'mentoring-monatsfokus-3-stunden-fokuszeit':{ layout: 'V2', profil: 'mentoring' },                           // M4
  'doterra-monatsfokus-hausarzt-wendepunkt': { layout: 'V3', profil: 'doterra' },                              // D2
  'doterra-monatsfokus-echte-zeitlinie':     { layout: 'V2', profil: 'doterra', stickerStyle: 'creme' },       // D9 — Creme-Sticker
  'doterra-monatsfokus-vor-wecker-auf':      { layout: 'V2', profil: 'doterra' },                              // D8 — Orange-Sticker

  // KW20 (2026-05-11) — Webinar-Aufwärmphase 2 + doTERRA Daily-Anwendung
  'mentoring-webinar-90min':                 { layout: 'V3', profil: 'mentoring', briefingDate: '2026-05-11' },                            // M3 — Webinar-Pitch direkt
  'mentoring-bademantel-ki':                 { layout: 'V2', profil: 'mentoring', briefingDate: '2026-05-11' },                            // M8 — Foto-Sticker (Bademantel-Vibe)
  'doterra-11-monate-schlaf':                { layout: 'V2', profil: 'doterra',   briefingDate: '2026-05-11', stickerStyle: 'creme' },     // D3 — Creme-Sticker
  'doterra-6-saeulen':                       { layout: 'V1', profil: 'doterra',   briefingDate: '2026-05-11' },                            // D9 — Sauber-Statement

  // KW21 (2026-05-18) — Bio-Klarheit + doTERRA „alles richtig"-Reframe
  // Variation-Update 2026-05-15: M5 von V3 auf V2-Creme (nach Patricia-Feedback Feed-Wiederholungs-Check)
  'mentoring-bio-produktkatalog':            { layout: 'V2', profil: 'mentoring', briefingDate: '2026-05-18', stickerStyle: 'creme' },     // M5 — Foto+Creme-Sticker
  'mentoring-instagram-eine-regel':          { layout: 'V1', profil: 'mentoring', briefingDate: '2026-05-18' },                            // M8 — Sauber-Statement
  'doterra-alles-richtig-trotzdem':          { layout: 'V2', profil: 'doterra',   briefingDate: '2026-05-18', stickerStyle: 'creme' },     // D5 — Creme-Sticker
  'doterra-brain-fog-47-tabs':               { layout: 'V3', profil: 'doterra',   briefingDate: '2026-05-18' },                            // D3 — Magazin
};

// Reel-Cover-Layouts
const REEL_LAYOUTS = {
  // KW19
  'mentoring-monatsfokus-bali-linie':        { layout: 'V2', profil: 'mentoring' }, // M6
  'mentoring-monatsfokus-ki-mitarbeiter':    { layout: 'V2', profil: 'mentoring' }, // M10
  'doterra-monatsfokus-3-uhr-symptome':      { layout: 'V1', profil: 'doterra' },   // D1
  'doterra-monatsfokus-koerper-ueberhoert':  { layout: 'V3', profil: 'doterra' },   // D3
};

// Profil-Akzent-Farbe
function accentForProfil(profil) {
  return profil === 'doterra' ? COLORS.orange : COLORS.petrol;
}

// Top-Tag pro Profil
function tagForProfil(profil) {
  return profil === 'doterra' ? 'VORMENOPAUSE' : 'MENTORING';
}

// ====================================================================
// MARKDOWN-PARSER für Karussell-Briefings
// ====================================================================

/**
 * Parst ein Karussell-Briefing-MD und gibt Slides zurück:
 *   { coverHook: { hero, sub }, slides: [{ hero, sub }, ...] }
 *
 * Format-Annahme:
 *   ## Cover (Slide 1) — Hook
 *   > **„HERO-TEXT"**
 *   > Untertitel: *„SUB-TEXT"*
 *
 *   ## Slide 2 — ...
 *   **Hero:** „TEXT"
 *   **Sub:** „TEXT"
 */
async function parseKarussellBriefing(filePath) {
  const md = await fs.readFile(filePath, 'utf-8');

  // Cover-Slide
  const coverMatch = md.match(/##\s+Cover\s+\(Slide 1\)[\s\S]*?\n>\s+\*\*[„"](.*?)["“]\*\*[\s\S]*?\n>\s+(?:Untertitel:|Subtitel:)?\s*\*[„"](.*?)["“]\*/);
  if (!coverMatch) {
    throw new Error(`Cover nicht gefunden in ${filePath}`);
  }
  const coverHook = {
    hero: coverMatch[1].trim(),
    sub: coverMatch[2].trim(),
  };

  // Slides 2-10
  const slides = [];
  for (let i = 2; i <= 10; i++) {
    // Match: ## Slide N — TITLE  ...  **Hero:** „...” \n**Sub:** „...”
    const sectionRe = new RegExp(
      `##\\s+Slide\\s+${i}\\b[\\s\\S]*?\\*\\*Hero:\\*\\*\\s*[„"](.*?)["“][\\s\\S]*?\\*\\*Sub:\\*\\*\\s*[„"](.*?)["“]`,
      'm'
    );
    const m = md.match(sectionRe);
    if (!m) {
      throw new Error(`Slide ${i} nicht gefunden in ${path.basename(filePath)}`);
    }
    slides.push({
      hero: m[1].trim(),
      sub: m[2].trim(),
    });
  }

  return { coverHook, slides };
}

/**
 * Parst ein Reel-Briefing-MD und extrahiert den Hook (Cover-Text):
 *   ## Hook (Cover-Text)
 *   > **„HERO"**
 *   > Untertitel: *„SUB"*
 */
async function parseReelHook(filePath) {
  const md = await fs.readFile(filePath, 'utf-8');
  // Nimm den gesamten Bereich zwischen ## Hook (Cover-Text) und der naechsten ## Section
  const sectionMatch = md.match(/##\s+Hook\s+\(Cover-Text\)\s*\n([\s\S]*?)(?=\n##\s)/);
  if (!sectionMatch) {
    throw new Error(`Section "## Hook (Cover-Text)" nicht gefunden in ${filePath}`);
  }
  const section = sectionMatch[1];

  // Extrahiere Hero (erste Bold-Quote-Sequenz, die ueber mehrere Zeilen gehen kann)
  // Pattern: > **„...**  oder  > **„... „**  oder mehrzeilig
  // Wir kombinieren alle > ** ... ** bis wir ein Untertitel: finden oder ein *„...*
  const lines = section.split('\n');
  let heroParts = [];
  let subParts = [];
  let mode = 'hero';
  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line.startsWith('>')) continue;
    const inner = line.replace(/^>\s*/, '').trim();
    if (!inner) continue;
    if (mode === 'hero') {
      // Wechsel zu sub bei Untertitel: oder italic-Quote
      if (/^Untertitel:/i.test(inner) || /^\*[„"]/.test(inner) || /^Subtitel:/i.test(inner)) {
        mode = 'sub';
      }
    }
    if (mode === 'hero') {
      // Strip ** und „ "
      let clean = inner.replace(/\*\*/g, '').replace(/^[„"]|["“]$/g, '');
      heroParts.push(clean);
    } else {
      // Strip Untertitel: + ** + * + „ "
      let clean = inner
        .replace(/^(?:Untertitel:|Subtitel:)\s*/i, '')
        .replace(/\*\*/g, '')
        .replace(/\*/g, '')
        .replace(/^[„"]|["“]$/g, '');
      subParts.push(clean);
    }
  }
  const hero = heroParts.join(' ').trim();
  const sub = subParts.join(' ').trim();
  if (!hero || !sub) {
    throw new Error(`Hook/Sub konnte nicht geparst werden in ${filePath}\n  hero="${hero}"\n  sub="${sub}"`);
  }
  return { hero, sub };
}

// ====================================================================
// HTML-TEMPLATES
// ====================================================================

const FONT_LINKS = `
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Philosopher:ital,wght@0,400;0,700;1,400;1,700&family=Source+Sans+3:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
`;

const SHARED_CSS = `
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: 1080px; }
  body { font-family: 'Source Sans 3', sans-serif; color: ${COLORS.text}; }
  .slide {
    width: 1080px;
    height: 1350px;
    position: relative;
    overflow: hidden;
  }
  .footer-brand {
    position: absolute;
    left: 60px;
    bottom: 60px;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 22px;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
  }
  .footer-meta {
    position: absolute;
    right: 60px;
    bottom: 60px;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 22px;
    font-weight: 500;
    letter-spacing: 0.05em;
  }
  .top-tag {
    position: absolute;
    top: 60px;
    left: 60px;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 0.16em;
  }
  .slide-num-circle {
    position: absolute;
    top: 60px;
    right: 60px;
    width: 64px;
    height: 64px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: ${COLORS.creme};
    font-family: 'Source Sans 3', sans-serif;
    font-weight: 700;
    font-size: 22px;
  }
`;

/**
 * V1 — Sauber-Statement (Petrol-Solid bzw. Orange-Solid)
 * - Solider Brand-Hintergrund (Akzent-Farbe)
 * - Kleiner horizontaler Strich oben (gold/creme)
 * - Hero (Philosopher Bold) zentriert
 * - Sub (Source Sans, soft creme)
 * - Italic-Akzent (Philosopher Italic, Akzent-Farbe-Tint)
 * - Footer: MUM LIFE BALANCE links + Slide-Nr rechts
 */
function renderV1Slide({ hero, sub, accent, slideNum, totalSlides, isCover, italicAccent }) {
  const accentBg = accent;
  // Italic-Akzent: für sub-text in soft Tone
  const italicQuote = italicAccent || extractItalicAccent(sub);
  const subClean = italicAccent ? sub : sub;
  const heroSize = isCover ? 104 : 96;

  return `
    <div class="slide v1" style="
      background: ${accentBg};
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 200px 100px 200px;
    ">
      <div style="
        width: 60px;
        height: 3px;
        background: ${COLORS.cremeSoft};
        margin-bottom: 80px;
        border-radius: 2px;
      "></div>

      <h1 style="
        font-family: 'Philosopher', serif;
        font-weight: 700;
        font-size: ${heroSize}px;
        line-height: 1.18;
        color: ${COLORS.creme};
        text-align: center;
        max-width: 880px;
        margin-bottom: 40px;
      ">${escapeHtml(hero)}</h1>

      <p style="
        font-family: 'Source Sans 3', sans-serif;
        font-size: 42px;
        line-height: 1.45;
        color: ${COLORS.cremeSoft};
        text-align: center;
        max-width: 880px;
        margin-bottom: ${italicQuote ? '50px' : '0'};
      ">${escapeHtml(subClean)}</p>

      ${italicQuote ? `
        <p style="
          font-family: 'Philosopher', serif;
          font-style: italic;
          font-size: 42px;
          line-height: 1.4;
          color: ${COLORS.creme};
          text-align: center;
          max-width: 860px;
          opacity: 0.92;
        ">${escapeHtml(italicQuote)}</p>
      ` : ''}

      <div class="footer-brand" style="color: ${COLORS.cremeSoft};">MUM LIFE BALANCE</div>
      <div class="footer-meta" style="color: ${COLORS.cremeSoft};">${slideNum} / ${totalSlides}</div>
    </div>
  `;
}

/**
 * V2 — Foto-Sticker
 * - Hintergrund-Foto (file://)
 * - Brand-Overlay-Sticker-Box am unteren Drittel mit Hero + Sub
 * - Top-Tag (MENTORING / VORMENOPAUSE)
 * - Slide-Nr oben rechts (klein)
 */
function renderV2Slide({ hero, sub, accent, slideNum, totalSlides, profil, photoPath, stickerStyle }) {
  const tag = tagForProfil(profil);
  const photoUrl = photoPath ? pathToFileURL(photoPath).href : null;
  const heroSize = 78;

  // stickerStyle: 'accent' (default — Akzentfarbe-Gradient) | 'creme' (heller Creme-Block, dunkle Schrift)
  const isCreme = stickerStyle === 'creme';

  // RGB-Werte des Akzents für Gradient
  const accentRGB = accent === COLORS.orange ? '220, 130, 46' : '18, 130, 140';

  // Hintergrund-Overlay (Foto + Bottom-Gradient damit Sticker sich absetzt)
  const photoOverlay = isCreme
    ? `linear-gradient(180deg, rgba(0,0,0,0.0) 0%, rgba(0,0,0,0.05) 40%, rgba(0,0,0,0.25) 75%, rgba(0,0,0,0.35) 100%), url('${photoUrl}') center/cover no-repeat`
    : `linear-gradient(180deg, rgba(0,0,0,0.05) 0%, rgba(0,0,0,0.15) 50%, rgba(${accentRGB}, 0.55) 75%, rgba(${accentRGB}, 0.85) 100%), url('${photoUrl}') center/cover no-repeat`;

  // Sticker-Block-Style (Creme-Karte vs Akzent-Gradient)
  const stickerBg = isCreme
    ? COLORS.creme
    : `linear-gradient(180deg, rgba(${accentRGB},0.0) 0%, ${accent} 28%)`;

  const heroColor = isCreme ? COLORS.text : COLORS.creme;
  const subColor = isCreme ? COLORS.textSoft : COLORS.cremeSoft;

  return `
    <div class="slide v2" style="
      background: ${photoUrl ? photoOverlay : accent};
    ">
      <div class="top-tag" style="
        background: ${accent};
        color: ${COLORS.creme};
        padding: 10px 22px;
        border-radius: 4px;
      ">${tag}</div>

      <div style="
        position: absolute;
        top: 70px;
        right: 60px;
        color: ${COLORS.creme};
        font-family: 'Source Sans 3', sans-serif;
        font-size: 24px;
        font-weight: 600;
        opacity: 0.9;
        text-shadow: 0 1px 4px rgba(0,0,0,0.4);
      ">${slideNum} / ${totalSlides}</div>

      <div style="
        position: absolute;
        left: ${isCreme ? '60px' : '0'};
        right: ${isCreme ? '60px' : '0'};
        bottom: ${isCreme ? '80px' : '0'};
        padding: ${isCreme ? '60px 60px 60px' : '80px 80px 100px'};
        background: ${stickerBg};
        ${isCreme ? `border-radius: 8px; box-shadow: 0 8px 32px rgba(0,0,0,0.18);` : ''}
        ${isCreme ? `border-left: 6px solid ${accent};` : ''}
      ">
        <h1 style="
          font-family: 'Philosopher', serif;
          font-weight: 700;
          font-size: ${heroSize}px;
          line-height: 1.16;
          color: ${heroColor};
          margin-bottom: 28px;
          max-width: ${isCreme ? '780px' : '920px'};
        ">${escapeHtml(hero)}</h1>
        <p style="
          font-family: 'Source Sans 3', sans-serif;
          font-size: 34px;
          line-height: 1.42;
          color: ${subColor};
          max-width: ${isCreme ? '760px' : '880px'};
        ">${escapeHtml(sub)}</p>
      </div>
    </div>
  `;
}

/**
 * V3 — Magazin-Style (Creme-Hintergrund)
 * - Top-Tag-Caps links (Akzent-Farbe)
 * - Slide-Nr-Kreis rechts (Akzent-Farbe)
 * - Kleiner Strich + Hero (Philosopher Bold)
 * - Sub (Source Sans)
 * - Italic-Akzent mit Akzent-Linie links
 * - Footer „Mum Life Balance" links + „Mentoring · KW 19" rechts
 */
function renderV3Slide({ hero, sub, accent, slideNum, totalSlides, profil, italicAccent, kwLabel }) {
  const tag = tagForProfil(profil);
  const profilLabel = profil === 'doterra' ? 'Vormenopause' : 'Mentoring';
  const italicQuote = italicAccent || extractItalicAccent(sub);
  const subClean = italicAccent ? sub : sub;
  const heroSize = 92;

  return `
    <div class="slide v3" style="
      background: ${COLORS.creme};
      padding: 60px;
    ">
      <div style="
        position: absolute;
        top: 60px;
        left: 60px;
        font-family: 'Source Sans 3', sans-serif;
        font-size: 22px;
        font-weight: 700;
        letter-spacing: 0.16em;
        color: ${accent};
      ">${tag}</div>

      <div class="slide-num-circle" style="background: ${accent};">
        ${String(slideNum).padStart(2, '0')}
      </div>

      <div style="
        position: absolute;
        left: 80px;
        right: 80px;
        top: 50%;
        transform: translateY(-50%);
      ">
        <div style="
          width: 80px;
          height: 4px;
          background: ${accent};
          margin-bottom: 50px;
          border-radius: 2px;
        "></div>

        <h1 style="
          font-family: 'Philosopher', serif;
          font-weight: 700;
          font-size: ${heroSize}px;
          line-height: 1.14;
          color: ${COLORS.text};
          margin-bottom: 36px;
        ">${escapeHtml(hero)}</h1>

        <p style="
          font-family: 'Source Sans 3', sans-serif;
          font-size: 36px;
          line-height: 1.45;
          color: ${COLORS.textSoft};
          margin-bottom: ${italicQuote ? '40px' : '0'};
        ">${escapeHtml(subClean)}</p>

        ${italicQuote ? `
          <div style="
            display: flex;
            gap: 18px;
            align-items: flex-start;
            margin-top: 30px;
          ">
            <div style="
              width: 4px;
              align-self: stretch;
              background: ${accent};
              border-radius: 2px;
              min-height: 50px;
            "></div>
            <p style="
              font-family: 'Philosopher', serif;
              font-style: italic;
              font-size: 36px;
              line-height: 1.4;
              color: ${accent};
            ">${escapeHtml(italicQuote)}</p>
          </div>
        ` : ''}
      </div>

      <div class="footer-brand" style="
        font-family: 'Philosopher', serif;
        font-style: italic;
        font-weight: 400;
        font-size: 22px;
        letter-spacing: 0.04em;
        text-transform: none;
        color: ${COLORS.textSoft};
      ">Mum Life Balance</div>
    </div>
  `;
}

/**
 * Reel-Cover (1080x1920, Story-Format, ähnlich Layout aber höher)
 */
function renderReelCover({ hero, sub, accent, profil, layout, photoPath }) {
  const tag = tagForProfil(profil);
  const photoUrl = photoPath ? pathToFileURL(photoPath).href : null;

  if (layout === 'V1') {
    // Sauber-Statement, Solid-Hintergrund
    return `
      <div class="slide reel-cover v1" style="
        width: 1080px;
        height: 1920px;
        background: ${accent};
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 280px 100px;
        position: relative;
        overflow: hidden;
      ">
        <div style="
          width: 60px;
          height: 3px;
          background: ${COLORS.cremeSoft};
          margin-bottom: 100px;
          border-radius: 2px;
        "></div>

        <h1 style="
          font-family: 'Philosopher', serif;
          font-weight: 700;
          font-size: 86px;
          line-height: 1.16;
          color: ${COLORS.creme};
          text-align: center;
          max-width: 880px;
          margin-bottom: 50px;
        ">${escapeHtml(hero)}</h1>

        <p style="
          font-family: 'Philosopher', serif;
          font-style: italic;
          font-size: 38px;
          line-height: 1.42;
          color: ${COLORS.cremeSoft};
          text-align: center;
          max-width: 820px;
        ">${escapeHtml(sub)}</p>

        <div style="
          position: absolute;
          left: 60px;
          bottom: 100px;
          color: ${COLORS.cremeSoft};
          font-family: 'Source Sans 3', sans-serif;
          font-size: 26px;
          font-weight: 500;
          letter-spacing: 0.18em;
          text-transform: uppercase;
        ">MUM LIFE BALANCE · REEL</div>
      </div>
    `;
  }

  if (layout === 'V2') {
    // Foto-Sticker
    return `
      <div class="slide reel-cover v2" style="
        width: 1080px;
        height: 1920px;
        background: ${photoUrl
          ? `linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.2) 50%, rgba(18, 130, 140, 0.55) 70%, rgba(18, 130, 140, 0.9) 100%), url('${photoUrl}') center/cover no-repeat`
          : accent};
        position: relative;
        overflow: hidden;
      ">
        <div style="
          position: absolute;
          top: 100px;
          left: 60px;
          background: ${accent};
          color: ${COLORS.creme};
          padding: 14px 28px;
          border-radius: 4px;
          font-family: 'Source Sans 3', sans-serif;
          font-size: 26px;
          font-weight: 700;
          letter-spacing: 0.16em;
        ">${tag}</div>

        <div style="
          position: absolute;
          top: 110px;
          right: 60px;
          color: ${COLORS.creme};
          font-family: 'Source Sans 3', sans-serif;
          font-size: 26px;
          font-weight: 600;
          opacity: 0.9;
        ">REEL</div>

        <div style="
          position: absolute;
          left: 0;
          right: 0;
          bottom: 0;
          padding: 100px 80px 140px;
          background: linear-gradient(180deg, rgba(18,130,140,0) 0%, ${accent} 28%);
        ">
          <h1 style="
            font-family: 'Philosopher', serif;
            font-weight: 700;
            font-size: 80px;
            line-height: 1.14;
            color: ${COLORS.creme};
            margin-bottom: 36px;
            max-width: 920px;
          ">${escapeHtml(hero)}</h1>
          <p style="
            font-family: 'Source Sans 3', sans-serif;
            font-size: 36px;
            line-height: 1.42;
            color: ${COLORS.cremeSoft};
            max-width: 880px;
          ">${escapeHtml(sub)}</p>
        </div>
      </div>
    `;
  }

  if (layout === 'V3') {
    // Magazin-Style
    const profilLabel = profil === 'doterra' ? 'Vormenopause' : 'Mentoring';
    return `
      <div class="slide reel-cover v3" style="
        width: 1080px;
        height: 1920px;
        background: ${COLORS.creme};
        position: relative;
        overflow: hidden;
        padding: 100px 80px;
      ">
        <div style="
          position: absolute;
          top: 100px;
          left: 80px;
          font-family: 'Source Sans 3', sans-serif;
          font-size: 26px;
          font-weight: 700;
          letter-spacing: 0.16em;
          color: ${accent};
        ">${tag}</div>

        <div style="
          position: absolute;
          top: 90px;
          right: 80px;
          width: 80px;
          height: 80px;
          border-radius: 50%;
          background: ${accent};
          display: flex;
          align-items: center;
          justify-content: center;
          color: ${COLORS.creme};
          font-family: 'Source Sans 3', sans-serif;
          font-weight: 700;
          font-size: 24px;
        ">REEL</div>

        <div style="
          position: absolute;
          left: 100px;
          right: 100px;
          top: 50%;
          transform: translateY(-50%);
        ">
          <div style="
            width: 100px;
            height: 5px;
            background: ${accent};
            margin-bottom: 60px;
            border-radius: 2px;
          "></div>

          <h1 style="
            font-family: 'Philosopher', serif;
            font-weight: 700;
            font-size: 88px;
            line-height: 1.13;
            color: ${COLORS.text};
            margin-bottom: 50px;
          ">${escapeHtml(hero)}</h1>

          <div style="
            display: flex;
            gap: 22px;
            align-items: flex-start;
          ">
            <div style="
              width: 5px;
              align-self: stretch;
              background: ${accent};
              border-radius: 2px;
              min-height: 70px;
            "></div>
            <p style="
              font-family: 'Philosopher', serif;
              font-style: italic;
              font-size: 38px;
              line-height: 1.42;
              color: ${accent};
            ">${escapeHtml(sub)}</p>
          </div>
        </div>

        <div style="
          position: absolute;
          left: 80px;
          bottom: 100px;
          font-family: 'Philosopher', serif;
          font-style: italic;
          font-weight: 400;
          font-size: 26px;
          color: ${COLORS.textSoft};
        ">Mum Life Balance</div>
      </div>
    `;
  }

  throw new Error(`Unbekanntes Reel-Cover-Layout: ${layout}`);
}

// ====================================================================
// HELPERS
// ====================================================================

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/**
 * Wenn der Sub mit „Das nennt sich..." oder ähnlich endet, kann er als italic-Quote behandelt werden.
 * Hier konservativ: gibt null zurück = kein extra italic-Akzent (sub bleibt wie er ist).
 * Italic-Akzente kommen explizit aus dem Briefing wenn nötig.
 */
function extractItalicAccent(sub) {
  return null;
}

function buildHtmlPage(slidesHtml) {
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Karussell-Render</title>
  ${FONT_LINKS}
  <style>${SHARED_CSS}</style>
</head>
<body>
${slidesHtml}
</body>
</html>`;
}

// ====================================================================
// PHOTO-AUSWAHL für V2
// ====================================================================

const PHOTOS_DIR = path.join(WORKSPACE_ROOT, 'context', 'Shootingbilder');

// Spezifisches Foto pro V2-Slug (nur V2-Layouts haben Foto-Hintergrund!)
// V1+V3 nutzen Solid-Color/Creme-Hintergründe — kein Foto.
// Indices weit auseinander gewählt fürs visuell unterschiedliche Set.
const PHOTO_INDEX = {
  // KW19 — Mentoring V2
  'mentoring-monatsfokus-3-stunden-fokuszeit': 150,  // M4 Karussell — Fokuszeit/Schreibtisch
  'mentoring-monatsfokus-bali-linie':           50,  // M6 Reel-Cover — Statement/Anti-Bali
  'mentoring-monatsfokus-ki-mitarbeiter':      450,  // M10 Reel-Cover — KI/Phone/Telegram
  // KW19 — doTERRA V2
  'doterra-monatsfokus-echte-zeitlinie':       700,  // D9 Karussell — Wendepunkt/ruhig
  'doterra-monatsfokus-vor-wecker-auf':        200,  // D8 Karussell — Morgen/Erwachen

  // KW20 — V2 Karussells
  'mentoring-bademantel-ki':                   400,  // M8 — Morgen/Bademantel-Vibe
  'doterra-11-monate-schlaf':                  650,  // D3 — Patricia ruhig morgens

  // KW21 — V2 Karussells
  'mentoring-bio-produktkatalog':              250,  // M5 — Patricia casual (anders als M8-KW20 #400)
  'doterra-alles-richtig-trotzdem':            550,  // D5 — Patricia nachdenklich
};

async function getPhotoPathForSlug(slug) {
  const idx = PHOTO_INDEX[slug];
  if (idx !== undefined) {
    // Nach exakter Datei suchen
    try {
      const files = await fs.readdir(PHOTOS_DIR);
      const exact = files.find(f => f.startsWith(`${idx} -`));
      if (exact) return path.join(PHOTOS_DIR, exact);
    } catch (e) {
      console.warn(`Konnte ${PHOTOS_DIR} nicht lesen:`, e.message);
    }
  }
  // Fallback: erstes Foto
  try {
    const files = await fs.readdir(PHOTOS_DIR);
    const jpgs = files.filter(f => /\.jpe?g$/i.test(f)).sort();
    if (jpgs.length) return path.join(PHOTOS_DIR, jpgs[0]);
  } catch (e) {
    // ignore
  }
  return null;
}

// ====================================================================
// MAIN
// ====================================================================

async function renderKarussell({ slug, layout, profil, briefingPath, browser, stickerStyle, renderDate }) {
  console.log(`\n--- Karussell: ${slug} (Layout ${layout}, Profil ${profil}${stickerStyle ? ', Sticker ' + stickerStyle : ''}) ---`);
  const { coverHook, slides } = await parseKarussellBriefing(briefingPath);

  const accent = accentForProfil(profil);
  const totalSlides = 10;
  const photoPath = layout === 'V2' ? await getPhotoPathForSlug(slug) : null;
  if (layout === 'V2' && photoPath) console.log(`  V2-Foto: ${path.basename(photoPath)}`);

  // Alle 10 Slides bauen (Cover + 9 Inhalts-Slides)
  const allSlides = [coverHook, ...slides];

  let slidesHtml = '';
  for (let i = 0; i < allSlides.length; i++) {
    const s = allSlides[i];
    const slideNum = i + 1;
    const isCover = i === 0;
    const opts = {
      hero: s.hero,
      sub: s.sub,
      accent,
      slideNum,
      totalSlides,
      isCover,
      profil,
      photoPath,
      stickerStyle,
    };
    if (layout === 'V1') slidesHtml += renderV1Slide(opts);
    else if (layout === 'V2') slidesHtml += renderV2Slide(opts);
    else if (layout === 'V3') slidesHtml += renderV3Slide(opts);
    else throw new Error(`Unbekanntes Layout: ${layout}`);
  }

  const html = buildHtmlPage(slidesHtml);
  const dateForDir = renderDate || '2026-05-04';
  const outDir = path.join(
    WORKSPACE_ROOT,
    'outputs', 'karussells', `render-${dateForDir}`,
    `${profil}-${slug.replace(`${profil}-`, '')}`
  );
  await fs.mkdir(outDir, { recursive: true });

  // HTML-Debug-Datei
  const htmlPath = path.join(outDir, '_debug.html');
  await fs.writeFile(htmlPath, html, 'utf-8');

  // Render
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1350, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() =>
    Promise.all(
      [...document.images].map(img =>
        img.complete && img.naturalWidth > 0
          ? Promise.resolve()
          : new Promise(res => { img.onload = img.onerror = res; })
      )
    )
  );
  await new Promise(r => setTimeout(r, 400));

  const slideEls = await page.$$('.slide');
  const outPaths = [];
  for (let i = 0; i < slideEls.length; i++) {
    const num = String(i + 1).padStart(2, '0');
    const outPath = path.join(outDir, `slide-${num}.png`);
    await slideEls[i].screenshot({ path: outPath, type: 'png' });
    const stat = await fs.stat(outPath);
    console.log(`  slide-${num}.png  (${(stat.size / 1024).toFixed(1)} KB)`);
    outPaths.push(outPath);
  }
  await page.close();

  return outPaths;
}

async function renderReel({ slug, layout, profil, briefingPath, browser }) {
  console.log(`\n--- Reel-Cover: ${slug} (Layout ${layout}, Profil ${profil}) ---`);
  const hook = await parseReelHook(briefingPath);

  const accent = accentForProfil(profil);
  const photoPath = layout === 'V2' ? await getPhotoPathForSlug(slug) : null;
  if (layout === 'V2' && photoPath) console.log(`  V2-Foto: ${path.basename(photoPath)}`);

  const slideHtml = renderReelCover({
    hero: hook.hero,
    sub: hook.sub,
    accent,
    profil,
    layout,
    photoPath,
  });
  const html = buildHtmlPage(slideHtml);

  const outDir = path.join(
    WORKSPACE_ROOT,
    'outputs', 'reels', 'render-2026-05-04',
    `${profil}-${slug.replace(`${profil}-`, '')}`
  );
  await fs.mkdir(outDir, { recursive: true });

  const htmlPath = path.join(outDir, '_debug.html');
  await fs.writeFile(htmlPath, html, 'utf-8');

  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() =>
    Promise.all(
      [...document.images].map(img =>
        img.complete && img.naturalWidth > 0
          ? Promise.resolve()
          : new Promise(res => { img.onload = img.onerror = res; })
      )
    )
  );
  await new Promise(r => setTimeout(r, 400));

  const slideEl = await page.$('.slide');
  if (!slideEl) throw new Error(`Keine .slide gefunden für ${slug}`);

  const outPath = path.join(outDir, 'cover.png');
  await slideEl.screenshot({ path: outPath, type: 'png' });
  const stat = await fs.stat(outPath);
  console.log(`  cover.png  (${(stat.size / 1024).toFixed(1)} KB)`);
  await page.close();

  return [outPath];
}

async function main() {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--allow-file-access-from-files', '--disable-web-security', '--no-sandbox'],
  });

  const allOutputs = { karussells: [], reels: [] };

  try {
    if (RUN_KARUSSELLS) {
      console.log('\n=== KARUSSELL-RENDER ===');
      for (const [slug, info] of Object.entries(KARUSSELL_LAYOUTS)) {
        if (ONLY_SLUG && ONLY_SLUG !== slug) continue;
        const briefingDate = info.briefingDate || '2026-05-04';
        const briefingPath = path.join(
          WORKSPACE_ROOT, 'outputs', 'karussells', `${briefingDate}-${slug}.md`
        );
        try {
          const paths = await renderKarussell({
            slug, layout: info.layout, profil: info.profil, briefingPath, browser,
            stickerStyle: info.stickerStyle,
            renderDate: briefingDate,
          });
          allOutputs.karussells.push(...paths);
        } catch (err) {
          console.error(`  FEHLER bei ${slug}:`, err.message);
        }
      }
    }

    if (RUN_REELS) {
      console.log('\n=== REEL-COVER-RENDER ===');
      for (const [slug, info] of Object.entries(REEL_LAYOUTS)) {
        if (ONLY_SLUG && ONLY_SLUG !== slug) continue;
        const briefingPath = path.join(
          WORKSPACE_ROOT, 'outputs', 'reels', `2026-05-04-${slug}-briefing.md`
        );
        try {
          const paths = await renderReel({
            slug, layout: info.layout, profil: info.profil, briefingPath, browser,
          });
          allOutputs.reels.push(...paths);
        } catch (err) {
          console.error(`  FEHLER bei ${slug}:`, err.message);
        }
      }
    }
  } finally {
    await browser.close();
  }

  console.log('\n=== FERTIG ===');
  console.log(`  Karussell-PNGs: ${allOutputs.karussells.length}`);
  console.log(`  Reel-Cover-PNGs: ${allOutputs.reels.length}`);
}

main().catch(err => {
  console.error('FATAL:', err);
  process.exit(1);
});
