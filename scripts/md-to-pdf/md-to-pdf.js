/**
 * md-to-pdf.js — Markdown zu PDF via Puppeteer + marked
 *
 * Nutzung:
 *   node md-to-pdf.js --input=<pfad.md> [--output=<pfad.pdf>] [--title="Titel"]
 *
 * Default-Output: gleicher Pfad wie input aber mit .pdf statt .md
 */

import puppeteer from 'puppeteer';
import { marked } from 'marked';
import fs from 'node:fs/promises';
import path from 'node:path';

const args = Object.fromEntries(
  process.argv.slice(2).map(a => {
    const [k, ...rest] = a.replace(/^--/, '').split('=');
    return [k, rest.join('=') || true];
  })
);

if (!args.input) {
  console.error('FEHLER: --input=<pfad.md> fehlt');
  process.exit(1);
}

const inputPath = path.resolve(args.input);
const outputPath = args.output
  ? path.resolve(args.output)
  : inputPath.replace(/\.md$/, '.pdf');

const titleFromArg = args.title || path.basename(inputPath, '.md');

console.log(`Lese: ${inputPath}`);
const md = await fs.readFile(inputPath, 'utf-8');
const html = marked.parse(md);

const fullHtml = `<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>${titleFromArg}</title>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=Philosopher:wght@400;700&display=swap" rel="stylesheet">
<style>
  body {
    font-family: 'Source Sans 3', -apple-system, sans-serif;
    color: #0c1c30;
    line-height: 1.55;
    max-width: 700px;
    margin: 40px auto;
    padding: 0 20px 60px;
  }
  h1, h2, h3, h4 {
    font-family: 'Philosopher', serif;
    color: #12828c;
    margin-top: 1.8em;
    margin-bottom: 0.5em;
  }
  h1 { font-size: 28px; border-bottom: 2px solid #dc822e; padding-bottom: 6px; }
  h2 { font-size: 22px; border-left: 4px solid #12828c; padding-left: 12px; }
  h3 { font-size: 18px; color: #29556d; }
  h4 { font-size: 15px; color: #444; text-transform: uppercase; letter-spacing: 0.05em; }
  p { margin: 0.6em 0; }
  ul, ol { margin: 0.5em 0; padding-left: 22px; }
  li { margin: 0.25em 0; }
  table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 13px; }
  th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: left; vertical-align: top; }
  th { background: #f1ecdd; color: #0c1c30; font-weight: 700; }
  tr:nth-child(even) td { background: #fafafa; }
  code {
    background: #f1ecdd;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 13px;
    color: #29556d;
  }
  pre {
    background: #f1ecdd;
    padding: 12px;
    border-radius: 4px;
    overflow-x: auto;
    font-size: 12px;
  }
  blockquote {
    border-left: 4px solid #dc822e;
    padding-left: 14px;
    margin-left: 0;
    color: #555;
    font-style: italic;
  }
  hr { border: 0; border-top: 1px solid #ddd; margin: 2em 0; }
  a { color: #12828c; text-decoration: none; }
  strong { color: #0c1c30; }
  /* Print */
  @media print {
    body { margin: 20mm; }
    h2 { page-break-before: auto; }
  }
</style></head>
<body>
${html}
</body></html>`;

const browser = await puppeteer.launch({
  headless: 'new',
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});

const page = await browser.newPage();
await page.setContent(fullHtml, { waitUntil: 'networkidle0' });
await page.evaluate(async () => {
  if (document.fonts && document.fonts.ready) await document.fonts.ready;
});

await fs.mkdir(path.dirname(outputPath), { recursive: true });
await page.pdf({
  path: outputPath,
  format: 'A4',
  margin: { top: '15mm', bottom: '15mm', left: '15mm', right: '15mm' },
  printBackground: true,
});

await browser.close();

const stat = await fs.stat(outputPath);
console.log(`✅ PDF erstellt: ${outputPath} (${(stat.size / 1024).toFixed(1)} KB)`);
