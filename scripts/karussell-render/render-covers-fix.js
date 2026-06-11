/**
 * Rendert NUR Slide 1 für die 4 ABAB-Fix-Cover (11.6.2026).
 * Output: outputs/{karussells,single-image}/<slug>/png/01.png
 */
import puppeteer from 'puppeteer';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs/promises';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WORKSPACE = path.resolve(__dirname, '..', '..');

const JOBS = [
  { type: 'single-image', slug: '2026-06-sonntag-21-uhr' },
  { type: 'karussells', slug: '2026-06-echt1-teamcall-anfrage' },
  { type: 'karussells', slug: '2026-06-network-standbein' },
  { type: 'single-image', slug: '2026-06-5-mamas-zusammen' },
];

async function renderSlide1(slidesPath, outPath) {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1350, deviceScaleFactor: 1 });
  await page.goto(`file:///${slidesPath.replace(/\\/g, '/')}`, { waitUntil: 'networkidle0' });
  await page.evaluate(() => Promise.all(
    Array.from(document.images).filter(i => !i.complete).map(i =>
      new Promise(r => { i.onload = r; i.onerror = r; })
    )
  ));
  await page.evaluate(() => {
    document.body.style.padding = '0';
    document.body.style.background = '#000';
  });
  const slide = await page.$('.slide');
  if (!slide) throw new Error('No .slide found');
  await slide.screenshot({ path: outPath, type: 'png' });
  await browser.close();
}

for (const job of JOBS) {
  const slidesPath = path.join(WORKSPACE, 'outputs', job.type, job.slug, 'slides.html');
  const outDir = path.join(WORKSPACE, 'outputs', job.type, job.slug, 'png');
  await fs.mkdir(outDir, { recursive: true });
  const outPath = path.join(outDir, '01.png');
  console.log(`Rendering ${job.slug} → ${outPath}`);
  await renderSlide1(slidesPath, outPath);
  console.log(`  ✓ Done`);
}

console.log('\n=== Alle 4 Slide-1-Covers gerendert ===');
