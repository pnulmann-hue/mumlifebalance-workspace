/**
 * Story-Render — HTML zu 10 Instagram-Story-PNGs (1080x1920, 9:16)
 *
 * Nutzung:
 *   node render-stories.js --input="<pfad-zur-html>" --output="<ziel-ordner>"
 *
 * Defaults:
 *   --input  → outputs/funnels/bio-check/launch/tag-0-stories-folien.html
 *   --output → outputs/funnels/bio-check/launch/stories-png/
 *
 * Was es macht:
 *   1. Oeffnet die HTML-Story-Folien-Datei in headless Chromium
 *   2. Wartet auf Google Fonts (Philosopher, Source Sans 3)
 *   3. Versteckt Preview-Chrome (Frame-Labels, Grid, Schatten)
 *   4. Setzt jede .slide auf exakt 1080x1920 px (Instagram-Story-Format)
 *   5. Macht pro Folie einen PNG-Screenshot → 01.png ... 10.png
 *
 * Die PNGs sind direkt Instagram-Story-tauglich.
 */

import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';

const args = Object.fromEntries(
  process.argv.slice(2).map(arg => {
    const [k, ...rest] = arg.replace(/^--/, '').split('=');
    return [k, rest.join('=') || true];
  })
);

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WORKSPACE_ROOT = path.resolve(__dirname, '..', '..');

const inputPath = args.input
  ? path.resolve(args.input)
  : path.join(WORKSPACE_ROOT, 'outputs', 'funnels', 'bio-check', 'launch', 'tag-0-stories-folien.html');

const outputDir = args.output
  ? path.resolve(args.output)
  : path.join(WORKSPACE_ROOT, 'outputs', 'funnels', 'bio-check', 'launch', 'stories-png');

console.log('Story-Render');
console.log(`  Input:  ${inputPath}`);
console.log(`  Output: ${outputDir}`);
console.log('');

await fs.mkdir(outputDir, { recursive: true });

try {
  await fs.access(inputPath);
} catch {
  console.error(`FEHLER: HTML-Datei nicht gefunden: ${inputPath}`);
  process.exit(1);
}

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
  // Viewport gross genug fuer 1080x1920-Slides
  await page.setViewport({ width: 1200, height: 2000, deviceScaleFactor: 1 });

  const fileUrl = pathToFileURL(inputPath).href;
  console.log(`Lade ${fileUrl} ...`);
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 60000 });

  await page.evaluate(() => document.fonts.ready);
  console.log('Fonts geladen.');

  // Preview-Chrome komplett wegnehmen + Slides auf Original-Groesse rendern.
  // Im Vorschau-HTML sind .stage-wrap mit overflow:hidden und .stage mit
  // transform:scale(0.32) — fuer Render muessen wir das aufheben.
  await page.addStyleTag({
    content: `
      html, body {
        padding: 0 !important;
        margin: 0 !important;
        background: #ffffff !important;
        overflow: visible !important;
      }
      .grid {
        display: block !important;
        gap: 0 !important;
        max-width: none !important;
        padding: 0 !important;
        margin: 0 !important;
      }
      .frame-label { display: none !important; }
      .stage-wrap {
        width: 1080px !important;
        height: 1920px !important;
        overflow: visible !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        margin: 0 !important;
      }
      .stage {
        transform: none !important;
        width: 1080px !important;
        height: 1920px !important;
      }
      .slide {
        width: 1080px !important;
        height: 1920px !important;
        border-radius: 0 !important;
      }
    `,
  });

  await new Promise(r => setTimeout(r, 800));

  const slides = await page.$$('.slide');
  if (slides.length === 0) {
    throw new Error('Keine .slide-Elemente gefunden in der HTML-Datei.');
  }
  console.log(`Gefunden: ${slides.length} Folien\n`);

  for (let i = 0; i < slides.length; i++) {
    const slide = slides[i];
    const n = String(i + 1).padStart(2, '0');
    const outPath = path.join(outputDir, `${n}.png`);

    await slide.scrollIntoView();
    await new Promise(r => setTimeout(r, 200));

    await slide.screenshot({
      path: outPath,
      type: 'png',
      omitBackground: false,
    });

    const stat = await fs.stat(outPath);
    const kb = (stat.size / 1024).toFixed(1);
    console.log(`  ${n}.png  (${kb} KB)`);
  }

  console.log(`\nFertig! ${slides.length} Story-Folien in:\n  ${outputDir}`);
} catch (err) {
  console.error('RENDER-FEHLER:', err);
  process.exitCode = 1;
} finally {
  await browser.close();
}
