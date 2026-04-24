/**
 * Canva-Upload-Pipeline (Phase 2)
 *
 * Kombiniert die 11 Karussell-PNGs zu einem Multi-Page-PDF und servt es via
 * HTTPS-Tunnel (Localtunnel). Canva's `import-design-from-url` MCP-Tool kann
 * das PDF dann als editierbares Multi-Page-Design importieren.
 *
 * Nutzung:
 *   node serve.js --slug=<render-slug> [--port=3456]
 *
 * Defaults:
 *   --slug → neuester Ordner in outputs/karussells/renders/
 *   --port → 3456
 *
 * Was passiert:
 *   1. Liest die 11 PNGs aus outputs/karussells/renders/<slug>/
 *   2. Kombiniert sie zu einem Multi-Page-PDF (1080x1350 pro Seite)
 *   3. Speichert PDF nach outputs/karussells/pdfs/<slug>.pdf
 *   4. Startet Express-Server auf --port, servt das PDF unter /karussell.pdf
 *   5. Oeffnet Localtunnel → gibt HTTPS-URL aus
 *   6. Gibt fertige URL via stdout: CANVA_PDF_URL=https://xxx.loca.lt/karussell.pdf
 *   7. Haelt Prozess am Leben bis SIGTERM / Ctrl+C
 *
 * Danach nutzt der Canva MCP diese URL fuer import-design-from-url.
 * Sicherheit: Tunnel ist nur so lange aktiv wie das Skript laeuft (Sekunden).
 */

import express from 'express';
import localtunnel from 'localtunnel';
import { PDFDocument } from 'pdf-lib';
import path from 'node:path';
import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

// --- Pfade ---
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WORKSPACE_ROOT = path.resolve(__dirname, '..', '..');
const RENDERS_DIR = path.join(WORKSPACE_ROOT, 'outputs', 'karussells', 'renders');
const PDFS_DIR = path.join(WORKSPACE_ROOT, 'outputs', 'karussells', 'pdfs');

// --- Args parsen ---
const args = Object.fromEntries(
  process.argv.slice(2).map(a => {
    const [k, ...rest] = a.replace(/^--/, '').split('=');
    return [k, rest.join('=') || true];
  })
);

const PORT = parseInt(args.port || '3456', 10);

// --- Slug ermitteln (neuester Ordner wenn nicht explizit) ---
async function pickSlug() {
  if (args.slug) return args.slug;
  const entries = await fs.readdir(RENDERS_DIR, { withFileTypes: true });
  const dirs = entries
    .filter(e => e.isDirectory())
    .map(e => e.name)
    .sort()
    .reverse();
  if (dirs.length === 0) {
    throw new Error(`Keine Render-Ordner in ${RENDERS_DIR} gefunden.`);
  }
  return dirs[0];
}

const slug = await pickSlug();
const renderDir = path.join(RENDERS_DIR, slug);
console.log(`Slug:       ${slug}`);
console.log(`Render-Dir: ${renderDir}`);

// --- PNGs sammeln (01.png ... 11.png) ---
async function collectPngs(dir) {
  const files = await fs.readdir(dir);
  return files
    .filter(f => /^\d+\.png$/i.test(f))
    .sort((a, b) => parseInt(a) - parseInt(b))
    .map(f => path.join(dir, f));
}

const pngPaths = await collectPngs(renderDir);
if (pngPaths.length === 0) {
  throw new Error(`Keine PNG-Dateien in ${renderDir} gefunden.`);
}
console.log(`PNGs:       ${pngPaths.length} Dateien (${pngPaths.map(p => path.basename(p)).join(', ')})\n`);

// --- PDF bauen ---
console.log('Baue Multi-Page-PDF (1080x1350 pro Seite)...');
const pdfDoc = await PDFDocument.create();

for (const pngPath of pngPaths) {
  const pngBytes = await fs.readFile(pngPath);
  const pngImage = await pdfDoc.embedPng(pngBytes);
  const page = pdfDoc.addPage([1080, 1350]);
  page.drawImage(pngImage, {
    x: 0,
    y: 0,
    width: 1080,
    height: 1350,
  });
}

const pdfBytes = await pdfDoc.save();

await fs.mkdir(PDFS_DIR, { recursive: true });
const pdfPath = path.join(PDFS_DIR, `${slug}.pdf`);
await fs.writeFile(pdfPath, pdfBytes);
const pdfKb = (pdfBytes.length / 1024).toFixed(1);
console.log(`PDF:        ${pdfPath} (${pdfKb} KB)\n`);

// --- Express-Server starten ---
const app = express();
app.get('/karussell.pdf', (_req, res) => {
  res.setHeader('Content-Type', 'application/pdf');
  res.setHeader('Content-Disposition', `inline; filename="${slug}.pdf"`);
  res.send(Buffer.from(pdfBytes));
});
app.get('/', (_req, res) => {
  res.send(`<h1>Canva-Upload-Pipeline aktiv</h1><p><a href="/karussell.pdf">PDF herunterladen</a></p>`);
});

const server = app.listen(PORT, () => {
  console.log(`Server:     http://localhost:${PORT}`);
});

// --- Localtunnel oeffnen ---
console.log('Oeffne Localtunnel...');
let tunnel;
try {
  tunnel = await localtunnel({ port: PORT });
} catch (err) {
  console.error('FEHLER beim Oeffnen des Tunnels:', err.message);
  server.close();
  process.exit(1);
}

const pdfUrl = `${tunnel.url}/karussell.pdf`;
console.log(`Tunnel:     ${tunnel.url}`);
console.log('');
console.log('==========================================================');
console.log(`CANVA_PDF_URL=${pdfUrl}`);
console.log('==========================================================');
console.log('');
console.log('Der Tunnel ist aktiv. Claude kann jetzt via Canva MCP');
console.log('`import-design-from-url` mit obiger URL aufrufen.');
console.log('');
console.log('Druecke Ctrl+C um Tunnel + Server zu schliessen.');

// --- Cleanup bei SIGTERM/SIGINT ---
const cleanup = () => {
  console.log('\nSchliesse Tunnel + Server...');
  try { tunnel.close(); } catch {}
  try { server.close(); } catch {}
  process.exit(0);
};
process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);

tunnel.on('close', () => {
  console.log('Tunnel geschlossen.');
  cleanup();
});

tunnel.on('error', (err) => {
  console.error('Tunnel-Fehler:', err);
});
