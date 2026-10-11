// Lokaler Testserver für den Stimm-Check — ahmt Vercel nach (public/ + /api/*).
//   node dev-server.mjs [pfad-zur-.env]     → http://localhost:4397
// Der Schlüssel kommt aus einer vorhandenen .env und wird nie ausgegeben.
import http from 'node:http';
import { readFileSync, existsSync } from 'node:fs';
import { join, extname, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import generate from './api/generate.js';
import tag from './api/tag.js';

const HIER = dirname(fileURLToPath(import.meta.url));
process.chdir(HIER); // api/generate.js sucht lib/ relativ zum Arbeitsordner
const envPfad = process.argv[2] || join(HIER, '..', 'startklar-service', '.env');
for (const zeile of readFileSync(envPfad, 'utf-8').split(/\r?\n/)) {
  const m = zeile.match(/^\s*(ANTHROPIC_API_KEY|ANTHROPIC_MODEL)\s*=\s*"?([^"\s]+)"?/);
  if (m) process.env[m[1]] = m[2];
}
const TYP = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css' };

http.createServer((req, res) => {
  const url = new URL(req.url, 'http://x');
  const api = { '/api/generate': generate, '/api/tag': tag }[url.pathname];
  if (api) {
    let roh = '';
    req.on('data', (c) => { roh += c; });
    req.on('end', () => {
      req.body = roh ? JSON.parse(roh) : {};
      res.status = (c) => { res.statusCode = c; return res; };
      res.json = (d) => { res.setHeader('Content-Type', 'application/json'); res.end(JSON.stringify(d)); };
      api(req, res);
    });
    return;
  }
  const datei = join(HIER, 'public', url.pathname === '/' ? 'index.html' : url.pathname);
  if (!existsSync(datei)) { res.statusCode = 404; return res.end('nicht gefunden'); }
  res.setHeader('Content-Type', TYP[extname(datei)] || 'application/octet-stream');
  res.end(readFileSync(datei));
}).listen(4397, () => console.log('Stimm-Check lokal: http://localhost:4397'));
