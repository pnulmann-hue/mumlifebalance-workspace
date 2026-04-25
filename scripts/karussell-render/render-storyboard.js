/**
 * Storyboard-Render — HTML zu 1080x2400-PNG (Reel-Storyboard)
 *
 * Default:
 *   --input  → outputs/funnels/bio-check/launch/tag-0-reel-storyboard.html
 *   --output → outputs/funnels/bio-check/launch/tag-0-reel-storyboard.png
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
  : path.join(WORKSPACE_ROOT, 'outputs', 'funnels', 'bio-check', 'launch', 'tag-0-reel-storyboard.html');

const outputPath = args.output
  ? path.resolve(args.output)
  : path.join(WORKSPACE_ROOT, 'outputs', 'funnels', 'bio-check', 'launch', 'tag-0-reel-storyboard.png');

const W = parseInt(args.w || 1080, 10);
const H = parseInt(args.h || 2400, 10);

console.log(`Storyboard-Render (${W}×${H})`);
console.log(`  Input:  ${inputPath}`);
console.log(`  Output: ${outputPath}\n`);

await fs.mkdir(path.dirname(outputPath), { recursive: true });
try { await fs.access(inputPath); }
catch { console.error(`FEHLER: HTML nicht gefunden: ${inputPath}`); process.exit(1); }

const browser = await puppeteer.launch({
  headless: 'new',
  args: ['--allow-file-access-from-files', '--disable-web-security', '--no-sandbox'],
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: H + 100, deviceScaleFactor: 1 });

  const fileUrl = pathToFileURL(inputPath).href;
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);

  await page.addStyleTag({
    content: `
      html, body { padding: 0 !important; margin: 0 !important; background: #fff !important; }
      .stage-wrap { width: ${W}px !important; height: ${H}px !important; overflow: visible !important; border-radius: 0 !important; box-shadow: none !important; }
      .stage { transform: none !important; width: ${W}px !important; height: ${H}px !important; }
      .slide { width: ${W}px !important; height: ${H}px !important; border-radius: 0 !important; }
    `,
  });

  await new Promise(r => setTimeout(r, 600));

  const slide = await page.$('.slide');
  if (!slide) throw new Error('Keine .slide gefunden.');

  await slide.screenshot({ path: outputPath, type: 'png', omitBackground: false });
  const stat = await fs.stat(outputPath);
  console.log(`  PNG: ${(stat.size / 1024).toFixed(1)} KB`);
  console.log(`\nFertig:\n  ${outputPath}`);
} catch (err) {
  console.error('RENDER-FEHLER:', err);
  process.exitCode = 1;
} finally {
  await browser.close();
}
