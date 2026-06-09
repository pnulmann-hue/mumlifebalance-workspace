/**
 * Render-Viral — direktes 1:1 Rendering ohne Zoom-Trick.
 * Voraussetzung: HTML-Slides sind bereits in echten 1080×1350 px-Werten designed.
 *
 * Nutzung:
 *   node render-viral.js --input="<pfad-zur-html>" --output="<ziel-ordner>"
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
  : path.join(WORKSPACE_ROOT, 'outputs', 'samples', 'karussell-v3-preview.html');

const outputDir = args.output
  ? path.resolve(args.output)
  : path.join(WORKSPACE_ROOT, 'outputs', 'karussells', 'renders', 'viral');

const SLIDE_W = 1080;
const SLIDE_H = 1350;

console.log('Render-Viral (no zoom)');
console.log(`  Input:  ${inputPath}`);
console.log(`  Output: ${outputDir}`);
console.log(`  Slide:  ${SLIDE_W}x${SLIDE_H}`);
console.log('');

await fs.mkdir(outputDir, { recursive: true });
await fs.access(inputPath);

const browser = await puppeteer.launch({
  headless: 'new',
  defaultViewport: null,
});
const page = await browser.newPage();
await page.setViewport({ width: SLIDE_W + 200, height: SLIDE_H + 200, deviceScaleFactor: 1 });

const fileUrl = pathToFileURL(inputPath).href;
console.log(`Lade ${fileUrl} ...`);
await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 30000 });

// Wait for fonts to be ready
await page.evaluate(() => document.fonts.ready);
console.log('Fonts geladen.');

// Wait for images
await page.evaluate(async () => {
  const imgs = Array.from(document.images);
  await Promise.all(imgs.map(img => img.complete ? Promise.resolve() : new Promise(r => img.onload = img.onerror = r)));
});
console.log('Alle Bilder geladen.');

// Strip body padding/margins so each slide screenshots cleanly
await page.evaluate(() => {
  document.body.style.padding = '0';
  document.body.style.margin = '0';
  document.body.style.background = '#fff';
  document.querySelectorAll('.slide').forEach(s => {
    s.style.margin = '0';
  });
});

// Find slides
const slideCount = await page.evaluate(() => document.querySelectorAll('.slide').length);
console.log(`Gefunden: ${slideCount} Folien`);
console.log('');

// Force every slide to exact dimensions first
await page.evaluate((w, h) => {
  document.querySelectorAll('.slide').forEach(s => {
    s.style.width = `${w}px`;
    s.style.height = `${h}px`;
  });
}, SLIDE_W, SLIDE_H);

const slides = await page.$$('.slide');
for (let i = 0; i < slides.length; i++) {
  const filename = `${String(i + 1).padStart(2, '0')}.png`;
  const filepath = path.join(outputDir, filename);

  // Direct element screenshot — no scrolling/clipping math needed
  await slides[i].screenshot({ path: filepath, omitBackground: false });

  const stat = await fs.stat(filepath);
  console.log(`  ${filename}  (${(stat.size / 1024).toFixed(1)} KB)`);
}

await browser.close();
console.log('');
console.log(`Fertig! ${slideCount} Folien in:`);
console.log(`  ${outputDir}`);
