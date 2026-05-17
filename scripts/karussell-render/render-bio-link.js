/**
 * Render Bio-Link-Tile (1080×1080) für Instagram Bio-Link-Page (Linktree/Linkin.bio).
 *
 * Variante A: Quadrat 1080×1080 (Linktree-Standard)
 * Variante B: Hochkant 1080×1920 (Story-Highlight-Cover)
 *
 * Nutzung:
 *   node render-bio-link.js               # rendert beide Varianten
 *   node render-bio-link.js --square      # nur 1080×1080
 *   node render-bio-link.js --story       # nur 1080×1920
 */

import puppeteer from 'puppeteer';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WORKSPACE_ROOT = path.resolve(__dirname, '..', '..');

const args = Object.fromEntries(
  process.argv.slice(2).map(a => {
    const [k, ...rest] = a.replace(/^--/, '').split('=');
    return [k, rest.join('=') || true];
  })
);

const RUN_SQUARE = !args.story || args.square;
const RUN_STORY = !args.square || args.story;

const COLORS = {
  creme: '#f1ecdd',
  petrol: '#12828c',
  dunkelblau: '#29556d',
  orange: '#dc822e',
  text: '#0c1c30',
  cremeSoft: 'rgba(241, 236, 221, 0.92)',
};

// Foto für Hintergrund — Patricia an Schreibtisch/Workspace
const PHOTOS_DIR = path.join(WORKSPACE_ROOT, 'context', 'Shootingbilder');
const PHOTO_INDEX = args.photo ? parseInt(args.photo, 10) : 400; // Default: Workspace/Morgen-Vibe (wie M8 Bademantel-Karussell)
const BRAND_ONLY = !!args['brand-only']; // wenn true: kein Foto, nur Petrol-Brand-Hintergrund

async function getPhotoPath(idx = PHOTO_INDEX) {
  const files = await fs.readdir(PHOTOS_DIR);
  const exact = files.find(f => f.startsWith(`${idx} -`));
  return exact ? path.join(PHOTOS_DIR, exact) : null;
}

function buildSquareHtml(photoUrl, brandOnly = false) {
  const bgLayer = brandOnly ? '' : `
    <img class="bg-photo" src="${photoUrl}" />
    <div class="bg-overlay"></div>`;
  const bgStyle = brandOnly
    ? `background: linear-gradient(135deg, ${COLORS.dunkelblau} 0%, ${COLORS.petrol} 60%, ${COLORS.petrol} 100%);`
    : `background: ${COLORS.petrol};`;
  return `
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  body { margin: 0; padding: 0; }
  .tile {
    width: 1080px;
    height: 1080px;
    position: relative;
    overflow: hidden;
    font-family: 'Source Sans 3', sans-serif;
    ${bgStyle}
  }
  .bg-photo {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center 25%;
    z-index: 1;
  }
  .bg-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(0,0,0,0.0) 0%, rgba(0,0,0,0.10) 40%, rgba(18,130,140,0.50) 60%, rgba(18,130,140,0.94) 82%);
    z-index: 2;
  }
  .tile > .tag, .tile > .micro, .tile > .content {
    position: absolute;
    z-index: 3;
  }
  .tag {
    position: absolute;
    top: 70px;
    left: 70px;
    background: ${COLORS.orange};
    color: ${COLORS.creme};
    font-family: 'Source Sans 3', sans-serif;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: 0.18em;
    padding: 12px 28px;
    border-radius: 4px;
    text-transform: uppercase;
  }
  .micro {
    position: absolute;
    top: 75px;
    right: 70px;
    color: ${COLORS.creme};
    font-family: 'Philosopher', serif;
    font-style: italic;
    font-size: 28px;
    opacity: 0.92;
    text-shadow: 0 1px 4px rgba(0,0,0,0.5);
  }
  .content {
    position: absolute;
    left: 0; right: 0; bottom: 0;
    padding: 80px 80px 90px;
    background: linear-gradient(180deg, rgba(18,130,140,0.0) 0%, ${COLORS.petrol} 38%);
  }
  .label {
    color: ${COLORS.cremeSoft};
    font-family: 'Source Sans 3', sans-serif;
    font-size: 30px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 24px;
  }
  h1 {
    font-family: 'Philosopher', serif;
    font-weight: 700;
    font-size: 82px;
    line-height: 1.12;
    color: ${COLORS.creme};
    margin: 0 0 32px 0;
    max-width: 880px;
  }
  .sub {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 36px;
    line-height: 1.35;
    color: ${COLORS.cremeSoft};
    margin: 0 0 36px 0;
    max-width: 820px;
  }
  .cta {
    display: inline-block;
    background: ${COLORS.orange};
    color: ${COLORS.creme};
    font-family: 'Source Sans 3', sans-serif;
    font-size: 32px;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 22px 44px;
    border-radius: 6px;
    text-transform: uppercase;
    box-shadow: 0 6px 24px rgba(0,0,0,0.25);
  }
</style></head><body>
<div class="tile">
  ${bgLayer}
  <div class="tag">KOSTENLOSES WEBINAR</div>
  <div class="micro">Mum Life Balance</div>
  <div class="content">
    <div class="label">Mai 2026 · Live mit Patricia</div>
    <h1>In 90 Min dein Mama-Leben mit KI-Assistenten umkrempeln.</h1>
    <p class="sub">Drei KI-Mitarbeiter. Live gezeigt. Bildschirm-Sharing. Keine Slides.</p>
    <div class="cta">Hier anmelden →</div>
  </div>
</div>
</body></html>`;
}

function buildStoryHtml(photoUrl) {
  return `
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  body { margin: 0; padding: 0; }
  .story {
    width: 1080px;
    height: 1920px;
    position: relative;
    overflow: hidden;
    font-family: 'Source Sans 3', sans-serif;
    background: ${COLORS.petrol};
  }
  .bg-photo {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center top;
    z-index: 1;
  }
  .bg-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(0,0,0,0.0) 0%, rgba(0,0,0,0.10) 40%, rgba(18,130,140,0.40) 60%, rgba(18,130,140,0.95) 82%);
    z-index: 2;
  }
  .story > .tag, .story > .micro, .story > .content {
    position: absolute;
    z-index: 3;
  }
  .tag {
    position: absolute;
    top: 140px;
    left: 70px;
    background: ${COLORS.orange};
    color: ${COLORS.creme};
    font-family: 'Source Sans 3', sans-serif;
    font-size: 28px;
    font-weight: 700;
    letter-spacing: 0.18em;
    padding: 14px 30px;
    border-radius: 4px;
    text-transform: uppercase;
  }
  .micro {
    position: absolute;
    top: 145px;
    right: 70px;
    color: ${COLORS.creme};
    font-family: 'Philosopher', serif;
    font-style: italic;
    font-size: 30px;
    opacity: 0.92;
    text-shadow: 0 1px 4px rgba(0,0,0,0.5);
  }
  .content {
    position: absolute;
    left: 0; right: 0; bottom: 0;
    padding: 100px 80px 160px;
    background: linear-gradient(180deg, rgba(18,130,140,0.0) 0%, ${COLORS.petrol} 35%);
  }
  .label {
    color: ${COLORS.cremeSoft};
    font-family: 'Source Sans 3', sans-serif;
    font-size: 32px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 28px;
  }
  h1 {
    font-family: 'Philosopher', serif;
    font-weight: 700;
    font-size: 96px;
    line-height: 1.1;
    color: ${COLORS.creme};
    margin: 0 0 40px 0;
    max-width: 900px;
  }
  .sub {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 42px;
    line-height: 1.35;
    color: ${COLORS.cremeSoft};
    margin: 0 0 50px 0;
    max-width: 880px;
  }
  .cta {
    display: inline-block;
    background: ${COLORS.orange};
    color: ${COLORS.creme};
    font-family: 'Source Sans 3', sans-serif;
    font-size: 36px;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 28px 52px;
    border-radius: 6px;
    text-transform: uppercase;
    box-shadow: 0 6px 24px rgba(0,0,0,0.25);
  }
</style></head><body>
<div class="story">
  <img class="bg-photo" src="${photoUrl}" />
  <div class="bg-overlay"></div>
  <div class="tag">KOSTENLOSES WEBINAR</div>
  <div class="micro">Mum Life Balance</div>
  <div class="content">
    <div class="label">Mai 2026 · Live mit Patricia</div>
    <h1>In 90 Min dein Mama-Leben mit KI-Assistenten umkrempeln.</h1>
    <p class="sub">Drei KI-Mitarbeiter. Live gezeigt. Bildschirm-Sharing. Keine Slides. Kein Tech-Background nötig.</p>
    <div class="cta">Hier anmelden →</div>
  </div>
</div>
</body></html>`;
}

async function renderTile({ html, width, height, outPath, browser }) {
  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: 1 });

  // HTML in tmp-Datei schreiben + via page.goto öffnen (lädt file://-Bilder zuverlässig)
  await fs.mkdir(path.dirname(outPath), { recursive: true });
  const tmpHtmlPath = outPath.replace(/\.png$/, '.html');
  await fs.writeFile(tmpHtmlPath, html, 'utf-8');
  await page.goto(pathToFileURL(tmpHtmlPath).href, { waitUntil: 'networkidle0', timeout: 60000 });

  // Fonts + Bilder warten
  await page.evaluate(async () => {
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
    const imgs = Array.from(document.images);
    await Promise.all(imgs.map(i => i.complete && i.naturalWidth > 0 ? null : new Promise(r => { i.onload = r; i.onerror = r; })));
  });

  await page.screenshot({ path: outPath, type: 'png', fullPage: false });
  await page.close();
  const stat = await fs.stat(outPath);
  console.log(`  ${path.basename(outPath)} (${(stat.size / 1024).toFixed(1)} KB)`);
}

async function main() {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--allow-file-access-from-files', '--disable-web-security', '--no-sandbox'],
  });

  const outDir = path.join(WORKSPACE_ROOT, 'outputs', 'sonstige', 'bio-link-webinar-mai-2026');

  // Wenn explizit --photo oder --brand-only gesetzt, nur EINE Variante rendern
  // Sonst: 4 Varianten parallel (3 Foto-Indices + 1 brand-only) zum Vergleichen
  const explicitMode = args.photo || args['brand-only'];

  try {
    if (explicitMode) {
      const photoPath = BRAND_ONLY ? null : await getPhotoPath(PHOTO_INDEX);
      const photoUrl = photoPath ? pathToFileURL(photoPath).href : null;
      const suffix = BRAND_ONLY ? 'brand-only' : `photo-${PHOTO_INDEX}`;
      console.log(`Modus: ${suffix}` + (photoPath ? ` (${path.basename(photoPath)})` : ''));

      if (RUN_SQUARE) {
        await renderTile({
          html: buildSquareHtml(photoUrl, BRAND_ONLY),
          width: 1080, height: 1080,
          outPath: path.join(outDir, `bio-link-square-${suffix}.png`),
          browser,
        });
      }
      if (RUN_STORY) {
        await renderTile({
          html: buildStoryHtml(photoUrl),
          width: 1080, height: 1920,
          outPath: path.join(outDir, `bio-link-story-${suffix}.png`),
          browser,
        });
      }
    } else {
      // 4-Varianten-Vergleich (nur Quadrat — Patricia pickt dann)
      const variants = [
        { label: 'photo-300', photo: 300 },
        { label: 'photo-500', photo: 500 },
        { label: 'photo-700', photo: 700 },
        { label: 'brand-only', brandOnly: true },
      ];
      console.log(`\n--- 4 Varianten zum Vergleich (alle 1080×1080) ---`);
      for (const v of variants) {
        const photoPath = v.brandOnly ? null : await getPhotoPath(v.photo);
        const photoUrl = photoPath ? pathToFileURL(photoPath).href : null;
        if (!v.brandOnly && !photoPath) {
          console.log(`  Skip ${v.label} — Foto nicht gefunden`);
          continue;
        }
        console.log(`\n  ${v.label}` + (photoPath ? ` → ${path.basename(photoPath)}` : ''));
        await renderTile({
          html: buildSquareHtml(photoUrl, v.brandOnly),
          width: 1080, height: 1080,
          outPath: path.join(outDir, `bio-link-square-${v.label}.png`),
          browser,
        });
      }
    }
  } finally {
    await browser.close();
  }

  console.log(`\nFertig. Output: ${outDir}`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
