/**
 * Karussell-Render — HTML zu 11 Instagram-PNGs (1080x1350, 4:5)
 *
 * Nutzung:
 *   node render.js --input="<pfad-zur-html>" --output="<ziel-ordner>" [--slug="name"]
 *
 * Defaults:
 *   --input  → outputs/samples/karussell-v3-preview.html (relativ zum Workspace-Root)
 *   --output → outputs/karussells/renders/YYYY-MM-DD-<slug>/
 *   --slug   → "preview"
 *
 * Was es macht:
 *   1. Oeffnet die HTML-Preview in headless Chromium
 *   2. Wartet auf Google Fonts + Silver South Script @font-face
 *   3. Versteckt Preview-Chrome (Titel, Crop-Marker, Legende, Slide-Labels)
 *   4. Zwingt jede .slide auf exakt 1080x1350 px (Instagram-Karussell-Format)
 *   5. Macht pro Folie einen PNG-Screenshot → 01.png ... 11.png
 *
 * Die PNGs sind direkt Instagram-postbar (via Blotato API oder manuell).
 */

import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';

// --- Argumente parsen ---
const args = Object.fromEntries(
  process.argv.slice(2).map(arg => {
    const [k, ...rest] = arg.replace(/^--/, '').split('=');
    return [k, rest.join('=') || true];
  })
);

// Workspace-Root = 2 Ebenen ueber diesem Script (scripts/karussell-render/)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WORKSPACE_ROOT = path.resolve(__dirname, '..', '..');
const today = new Date().toISOString().slice(0, 10);
const slug = args.slug || 'preview';

const inputPath = args.input
  ? path.resolve(args.input)
  : path.join(WORKSPACE_ROOT, 'outputs', 'samples', 'karussell-v3-preview.html');

const outputDir = args.output
  ? path.resolve(args.output)
  : path.join(WORKSPACE_ROOT, 'outputs', 'karussells', 'renders', `${today}-${slug}`);

console.log('Karussell-Render');
console.log(`  Input:  ${inputPath}`);
console.log(`  Output: ${outputDir}`);
console.log('');

// --- Output-Ordner anlegen ---
await fs.mkdir(outputDir, { recursive: true });

// --- Eingabe pruefen ---
try {
  await fs.access(inputPath);
} catch {
  console.error(`FEHLER: HTML-Datei nicht gefunden: ${inputPath}`);
  process.exit(1);
}

// --- Puppeteer starten ---
const browser = await puppeteer.launch({
  headless: 'new',
  args: [
    '--allow-file-access-from-files',
    '--disable-web-security',
    '--no-sandbox',
  ],
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 1400, deviceScaleFactor: 1 });

  const fileUrl = pathToFileURL(inputPath).href;
  console.log(`Lade ${fileUrl} ...`);
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 60000 });

  // Auf alle Fonts warten (Philosopher, Source Sans Pro, Silver South Script)
  await page.evaluate(() => document.fonts.ready);
  console.log('Fonts geladen.');

  // Auf alle Bilder warten (file:// Bilder werden nicht von networkidle0 erfasst)
  await page.evaluate(() =>
    Promise.all(
      [...document.images].map(img =>
        img.complete && img.naturalWidth > 0
          ? Promise.resolve()
          : new Promise(res => {
              img.onload = img.onerror = res;
            })
      )
    )
  );
  const brokenImages = await page.evaluate(() =>
    [...document.images]
      .filter(img => !img.complete || img.naturalWidth === 0)
      .map(img => img.src)
  );
  if (brokenImages.length) {
    console.warn('WARNUNG: Folgende Bilder konnten nicht geladen werden:');
    brokenImages.forEach(src => console.warn(`  - ${src}`));
  } else {
    console.log('Alle Bilder geladen.');
  }

  // Preview-Chrome ausblenden + jede Slide proportional auf 1080x1350 skalieren.
  // Die HTML-Preview wurde fuer ~340px Grid-Darstellung designed. Wir lassen die
  // Slide auf 340x425 (die "Design-Basis") und nutzen CSS `zoom: 3.1765` damit
  // Chromium alles 3.18x vergroessert rendert -> bounding box = 1080x1350.
  // Vorteil: Alle Font-Sizes, Padding, Positions skalieren proportional mit.
  await page.addStyleTag({
    content: `
      html, body {
        padding: 0 !important;
        margin: 0 !important;
        background: #ffffff !important;
        overflow: visible !important;
      }
      h1, .subtitle, .legend, .slide-label { display: none !important; }
      .slide::before, .slide::after { display: none !important; }
      .slide .crop-label { display: none !important; }
      .slides-grid {
        display: block !important;
        max-width: none !important;
        margin: 0 !important;
        gap: 0 !important;
        padding: 0 !important;
      }
      .slide-wrapper {
        display: block !important;
        margin: 0 !important;
        padding: 0 !important;
      }
      .slide {
        width: 340px !important;
        height: 425px !important;
        aspect-ratio: unset !important;
        zoom: 3.1765 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        margin: 0 !important;
      }
    `,
  });

  // Kurz warten damit Layout sich neu berechnet
  await new Promise(r => setTimeout(r, 800));

  // Alle Folien finden
  const slides = await page.$$('.slide');
  if (slides.length === 0) {
    throw new Error('Keine .slide-Elemente gefunden in der HTML-Datei.');
  }
  console.log(`Gefunden: ${slides.length} Folien\n`);

  // Jede Folie screenshoten
  for (let i = 0; i < slides.length; i++) {
    const slide = slides[i];
    const n = String(i + 1).padStart(2, '0');
    const outPath = path.join(outputDir, `${n}.png`);

    // Sicherstellen dass Element sichtbar ist
    await slide.scrollIntoView();
    await new Promise(r => setTimeout(r, 150));

    await slide.screenshot({
      path: outPath,
      type: 'png',
      omitBackground: false,
    });

    const stat = await fs.stat(outPath);
    const kb = (stat.size / 1024).toFixed(1);
    console.log(`  ${n}.png  (${kb} KB)`);
  }

  console.log(`\nFertig! ${slides.length} Folien in:\n  ${outputDir}`);
} catch (err) {
  console.error('RENDER-FEHLER:', err);
  process.exitCode = 1;
} finally {
  await browser.close();
}
