/**
 * build-pdf.js — baut nur das PDF, ohne Tunnel/Server.
 *
 * Nimmt die 11 PNGs aus outputs/karussells/renders/<slug>/ und
 * kombiniert sie zu einem 1080x1350 multi-page PDF.
 *
 * Nutzung:
 *   node build-pdf.js --slug=<render-slug>
 *
 * Output:
 *   outputs/karussells/pdfs/<slug>.pdf
 */

import { PDFDocument } from 'pdf-lib';
import path from 'node:path';
import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WORKSPACE_ROOT = path.resolve(__dirname, '..', '..');
const RENDERS_DIR = path.join(WORKSPACE_ROOT, 'outputs', 'karussells', 'renders');
const PDFS_DIR = path.join(WORKSPACE_ROOT, 'outputs', 'karussells', 'pdfs');

const args = Object.fromEntries(
  process.argv.slice(2).map(a => {
    const [k, ...rest] = a.replace(/^--/, '').split('=');
    return [k, rest.join('=') || true];
  })
);

async function pickSlug() {
  if (args.slug) return args.slug;
  const entries = await fs.readdir(RENDERS_DIR, { withFileTypes: true });
  const dirs = entries.filter(e => e.isDirectory()).map(e => e.name).sort().reverse();
  if (dirs.length === 0) throw new Error(`Keine Render-Ordner in ${RENDERS_DIR}.`);
  return dirs[0];
}

const slug = await pickSlug();
const renderDir = path.join(RENDERS_DIR, slug);
console.log(`Slug:       ${slug}`);
console.log(`Render-Dir: ${renderDir}`);

const files = await fs.readdir(renderDir);
const pngPaths = files
  .filter(f => /^\d+\.png$/i.test(f))
  .sort((a, b) => parseInt(a) - parseInt(b))
  .map(f => path.join(renderDir, f));

if (pngPaths.length === 0) throw new Error(`Keine PNGs in ${renderDir}.`);
console.log(`PNGs:       ${pngPaths.length} Dateien\n`);

console.log('Baue Multi-Page-PDF (1080x1350 pro Seite)...');
const pdfDoc = await PDFDocument.create();

for (const pngPath of pngPaths) {
  const pngBytes = await fs.readFile(pngPath);
  const pngImage = await pdfDoc.embedPng(pngBytes);
  const page = pdfDoc.addPage([1080, 1350]);
  page.drawImage(pngImage, { x: 0, y: 0, width: 1080, height: 1350 });
}

const pdfBytes = await pdfDoc.save();
await fs.mkdir(PDFS_DIR, { recursive: true });
const pdfPath = path.join(PDFS_DIR, `${slug}.pdf`);
await fs.writeFile(pdfPath, pdfBytes);
const pdfKb = (pdfBytes.length / 1024).toFixed(1);

console.log(`\n\u2705 PDF fertig:`);
console.log(`   ${pdfPath}`);
console.log(`   ${pdfKb} KB, ${pngPaths.length} Seiten, 1080\u00d71350 px`);
console.log('');
console.log('Drag & Drop das PDF in Canva \u2192 wird automatisch Multi-Page-Design.');
