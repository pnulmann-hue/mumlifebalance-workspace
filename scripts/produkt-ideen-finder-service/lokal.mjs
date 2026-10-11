/* =============================================================
   Der Produkt-Ideen-Finder lokal
   =============================================================
   Startet die echte Seite mit der echten API auf dem eigenen
   Rechner — ohne Vercel, ohne Deploy.

     node scripts/produkt-ideen-finder-service/lokal.mjs
     -> http://localhost:4390

   Der ANTHROPIC_API_KEY kommt aus der .env im Wurzelverzeichnis
   und wird nirgends ausgegeben. Es ist derselbe Code, der spaeter
   auf Vercel laeuft — api/finder.js wird direkt aufgerufen.

   Zum Ansehen und Ausprobieren gedacht, nicht zum Veroeffentlichen:
   die Seite haengt hier an niemandem und niemand kommt von aussen
   daran.
   ============================================================= */

import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { join, extname, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HIER = dirname(fileURLToPath(import.meta.url));
const OEFFENTLICH = join(HIER, 'public');
const PORT = Number(process.env.PORT || 4390);

const TYPEN = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
  '.svg': 'image/svg+xml', '.ico': 'image/x-icon',
};

/* --- Schluessel aus der .env holen, ohne ihn anzuzeigen --- */
if (!process.env.ANTHROPIC_API_KEY) {
  try {
    const env = await readFile(join(HIER, '..', '..', '.env'), 'utf-8');
    for (const zeile of env.split(/\r?\n/)) {
      const m = zeile.match(/^\s*ANTHROPIC_API_KEY\s*=\s*(.+)$/);
      if (m) process.env.ANTHROPIC_API_KEY = m[1].trim().replace(/^["']|["']$/g, '');
    }
  } catch {
    /* keine .env — der Hinweis kommt gleich */
  }
}
if (!process.env.ANTHROPIC_API_KEY) {
  console.error('Kein ANTHROPIC_API_KEY gefunden — weder in der Umgebung noch in der .env im');
  console.error('Wurzelverzeichnis. Ohne den Schluessel kann die Seite keine Ideen holen.');
  process.exit(1);
}

/* Vercel setzt das Arbeitsverzeichnis auf den Projektordner — api/finder.js
   sucht seine Prompts danach. Hier genauso. */
process.chdir(HIER);
const { default: finder } = await import(pathToFileURL(join(HIER, 'api', 'finder.js')).href);

createServer(async (req, res) => {
  try {
    if (req.url.split('?')[0] === '/api/finder') {
      if (req.method !== 'POST') {
        res.writeHead(405).end('Nur POST.');
        return;
      }
      let roh = '';
      for await (const stueck of req) roh += stueck;

      /* Die Antwort so nachbauen, wie Vercel sie der Route reicht. */
      const antwort = {
        status(code) { this._code = code; return this; },
        json(daten) {
          res.writeHead(this._code || 200, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify(daten));
          return this;
        },
      };
      let koerper = {};
      try { koerper = roh ? JSON.parse(roh) : {}; } catch { /* leer lassen */ }
      await finder({ method: 'POST', body: koerper }, antwort);
      return;
    }

    const pfad = join(OEFFENTLICH, req.url === '/' ? 'index.html' : req.url.split('?')[0]);
    if (!pfad.startsWith(OEFFENTLICH)) { res.writeHead(403).end('Nein.'); return; }

    const inhalt = await readFile(pfad);
    res.writeHead(200, {
      'Content-Type': TYPEN[extname(pfad).toLowerCase()] || 'application/octet-stream',
      'Cache-Control': 'no-store',
    });
    res.end(inhalt);
  } catch (err) {
    if (err.code === 'ENOENT') { res.writeHead(404).end('Nicht gefunden.'); return; }
    console.error(err);
    if (!res.headersSent) res.writeHead(500);
    res.end('Fehler.');
  }
}).listen(PORT, () => {
  console.log(`Produkt-Ideen-Finder laeuft: http://localhost:${PORT}`);
  console.log('Beenden mit Strg+C.');
});
