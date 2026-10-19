// Rendert jede <section class="slide"> aus slides.html als 1080x1920-PNG.
//   node scripts/story-render/bogo-2026-10-render.mjs [ordner]
import { createRequire } from 'module';
import { resolve, join } from 'path';
import { mkdirSync } from 'fs';
import { pathToFileURL } from 'url';
// playwright lokal oder global (NODE_PATH)
const { chromium } = createRequire(import.meta.url)('playwright');

const ordner = resolve(process.argv[2] || 'outputs/stories/2026-10-20-bogo-doterra');
const aus = join(ordner, 'slides-png');
mkdirSync(aus, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 2000 } });
await page.goto(pathToFileURL(join(ordner, 'slides.html')).href, { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
const ids = await page.$$eval('section.slide', els => els.map(e => e.id));
for (const id of ids) {
  await page.locator('#' + id).screenshot({ path: join(aus, id.replace('s', '') + '.png') });
}
await browser.close();
console.log(`${ids.length} PNGs -> ${aus}`);
