/**
 * Rendert das MBA-Webinar-Deck (HTML) zu 16:9-Folien-PNGs + dumpt Folientext.
 * node render-webinar-deck.mjs
 */
import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';
import { pathToFileURL } from 'node:url';

const DECK = 'C:/Users/pnulm/Desktop/Mein Business/outputs/produkte/mba-launch/webinar-deck.html';
const OUT = 'C:/Users/pnulm/AppData/Local/Temp/claude/C--Users-pnulm-Desktop-Mein-Business/f670d40c-dca6-44a9-b036-328baeedd727/scratchpad/webslides';

await fs.mkdir(OUT, { recursive: true });

const browser = await puppeteer.launch({
  headless: 'new',
  args: ['--allow-file-access-from-files', '--disable-web-security', '--no-sandbox'],
});
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(DECK).href, { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.all([...document.images].map(img =>
    img.complete && img.naturalWidth > 0 ? Promise.resolve()
      : new Promise(res => { img.onload = img.onerror = res; }))));

  // Scroll-Container statisch machen, damit jede .slide als eigenes 1920x1080-Element rendert
  await page.addStyleTag({ content: `
    html,body{margin:0!important;padding:0!important;}
    .deck{height:auto!important;overflow:visible!important;scroll-snap-type:none!important;}
    .slide{height:1080px!important;}
    .progress,.counter,.nav,.hint{display:none!important;}
  `});
  await new Promise(r => setTimeout(r, 600));

  const texts = await page.$$eval('.slide', els => els.map(e => e.innerText.replace(/\s+/g, ' ').trim()));
  const slides = await page.$$('.slide');
  console.log('Folien:', slides.length);
  for (let i = 0; i < slides.length; i++) {
    const n = String(i + 1).padStart(2, '0');
    await slides[i].scrollIntoView();
    await new Promise(r => setTimeout(r, 120));
    await slides[i].screenshot({ path: path.join(OUT, `${n}.png`), type: 'png' });
    console.log(`  ${n}.png  |  ${texts[i].slice(0, 70)}`);
  }
  await fs.writeFile(path.join(OUT, 'slides-text.json'), JSON.stringify(texts, null, 2));
  console.log('OK ->', OUT);
} catch (e) { console.error('FEHLER:', e); process.exitCode = 1; }
finally { await browser.close(); }
