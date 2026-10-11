/**
 * HTML → A4-PDF (einseitiger Flyer/Freebie).
 * Nutzung:
 *   node render-pdf.mjs --input="<pfad.html>" --output="<pfad.pdf>"
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
  console.error('FEHLER: --input und --output sind Pflicht.');
  process.exit(1);
}

const inputPath = path.resolve(args.input);
const outputPath = path.resolve(args.output);
await fs.mkdir(path.dirname(outputPath), { recursive: true });

const browser = await puppeteer.launch({
  headless: 'new',
  args: ['--allow-file-access-from-files', '--disable-web-security', '--no-sandbox'],
});

try {
  const page = await browser.newPage();
  const fileUrl = pathToFileURL(inputPath).href;
  console.log(`Lade ${fileUrl} ...`);
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  console.log('Fonts geladen. Erzeuge PDF ...');
  await page.pdf({
    path: outputPath,
    format: 'A4',
    printBackground: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
    preferCSSPageSize: true,
  });
  const stat = await fs.stat(outputPath);
  console.log(`Fertig: ${outputPath} (${(stat.size / 1024).toFixed(1)} KB)`);
} catch (err) {
  console.error('PDF-FEHLER:', err);
  process.exitCode = 1;
} finally {
  await browser.close();
}
