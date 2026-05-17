/**
 * Render-KW20 — Schlanker Karussell-Renderer für KW 20
 *
 * Liest eine HTML-Datei mit .slide-Elementen (jedes 1080x1350) und
 * macht pro Slide einen PNG-Screenshot in den Output-Ordner.
 *
 * Nutzung:
 *   node render-kw20.js --input=<html-pfad> --output=<ziel-ordner>
 *
 * Output: slide-01.png .. slide-NN.png (1080x1350)
 */

import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';

const args = Object.fromEntries(
  process.argv.slice(2).map(a => {
    const [k, ...rest] = a.replace(/^--/, '').split('=');
    return [k, rest.join('=') || true];
  })
);

if (!args.input || !args.output) {
  console.error('Nutzung: node render-kw20.js --input=<html> --output=<dir>');
  process.exit(1);
}

const inputPath = path.resolve(args.input);
const outputDir = path.resolve(args.output);
await fs.mkdir(outputDir, { recursive: true });

console.log(`Render: ${inputPath} -> ${outputDir}`);

const browser = await puppeteer.launch({
  headless: 'new',
  args: ['--allow-file-access-from-files', '--disable-web-security', '--no-sandbox'],
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1350, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(inputPath).href, { waitUntil: 'networkidle0', timeout: 60000 });
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

  const slides = await page.$$('.slide');
  if (slides.length === 0) throw new Error('Keine .slide-Elemente gefunden');
  console.log(`${slides.length} Slides gefunden`);

  for (let i = 0; i < slides.length; i++) {
    const n = String(i + 1).padStart(2, '0');
    const outPath = path.join(outputDir, `slide-${n}.png`);
    await slides[i].screenshot({ path: outPath, type: 'png' });
    const stat = await fs.stat(outPath);
    console.log(`  slide-${n}.png (${(stat.size / 1024).toFixed(1)} KB)`);
  }

  console.log(`\nFertig: ${slides.length} PNGs in ${outputDir}`);
} catch (err) {
  console.error('FEHLER:', err);
  process.exitCode = 1;
} finally {
  await browser.close();
}
