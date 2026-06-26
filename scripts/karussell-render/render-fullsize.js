/**
 * Full-Size-Slide-Render — screenshotet jede .slide in ihrer nativen Groesse.
 *
 * Fuer Single-Image-/Slide-HTMLs, deren .slide bereits 1080x1350 (oder andere
 * Zielgroesse) direkt definiert ist — also OHNE den 340px-Grid-Zoom-Trick aus
 * render.js. Schreibt 01.png, 02.png, ... in den Output-Ordner.
 *
 * Nutzung:
 *   node render-fullsize.js --input="<pfad.html>" --output="<ordner>"
 */

import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';
import { pathToFileURL } from 'node:url';

const args = Object.fromEntries(
  process.argv.slice(2).map(a => {
    const [k, ...rest] = a.replace(/^--/, '').split('=');
    return [k, rest.join('=') || true];
  })
);

if (!args.input || !args.output) {
  console.error('FEHLER: --input und --output sind erforderlich.');
  process.exit(1);
}

const inputPath = path.resolve(args.input);
const outputDir = path.resolve(args.output);
await fs.mkdir(outputDir, { recursive: true });

const browser = await puppeteer.launch({
  headless: 'new',
  args: ['--allow-file-access-from-files', '--disable-web-security', '--no-sandbox'],
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 1500, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(inputPath).href, { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() =>
    Promise.all([...document.images].map(img =>
      img.complete && img.naturalWidth > 0 ? Promise.resolve()
        : new Promise(res => { img.onload = img.onerror = res; })))
  );

  // Preview-Rahmen weg, Slides ohne Aussenrand — native Groesse beibehalten.
  await page.addStyleTag({
    content: `html,body{padding:0!important;margin:0!important;background:#fff!important;overflow:visible!important;}
              .slide{margin:0!important;box-shadow:none!important;}`,
  });
  await new Promise(r => setTimeout(r, 600));

  const slides = await page.$$('.slide');
  if (!slides.length) throw new Error('Keine .slide-Elemente gefunden.');
  console.log(`Gefunden: ${slides.length} Slides`);

  for (let i = 0; i < slides.length; i++) {
    const n = String(i + 1).padStart(2, '0');
    const outPath = path.join(outputDir, `${n}.png`);
    await slides[i].scrollIntoView();
    await new Promise(r => setTimeout(r, 120));
    await slides[i].screenshot({ path: outPath, type: 'png', omitBackground: false });
    const kb = ((await fs.stat(outPath)).size / 1024).toFixed(1);
    console.log(`  ${n}.png (${kb} KB)`);
  }
  console.log(`Fertig -> ${outputDir}`);
} catch (err) {
  console.error('RENDER-FEHLER:', err);
  process.exitCode = 1;
} finally {
  await browser.close();
}
