// Lokaler Testserver für den Story-Generator — ahmt Vercel nach (public/ + /api/story).
//   node dev-server.mjs [pfad-zur-.env]     → http://localhost:4415   (Zugangscode lokal: TEST)
// Der Schlüssel kommt aus einer vorhandenen .env und wird nie ausgegeben.
import http from 'node:http';
import { readFileSync, existsSync } from 'node:fs';
import { join, extname, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import story from './api/story.js';

const HIER = dirname(fileURLToPath(import.meta.url));
process.chdir(HIER);
const envPfad = process.argv[2] || join(HIER, '..', 'startklar-service', '.env');
for (const zeile of readFileSync(envPfad, 'utf-8').split(/\r?\n/)) {
  const m = zeile.match(/^\s*(ANTHROPIC_API_KEY|ANTHROPIC_MODEL)\s*=\s*"?([^"\s]+)"?/);
  if (m) process.env[m[1]] = m[2];
}
process.env.ZUGANGSCODES = process.env.ZUGANGSCODES || 'TEST';
const TYP = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.jpg': 'image/jpeg', '.png': 'image/png' };

http.createServer((req, res) => {
  const url = new URL(req.url, 'http://x');
  if (url.pathname === '/api/story') {
    let roh = '';
    req.on('data', (c) => { roh += c; });
    req.on('end', () => {
      req.body = roh ? JSON.parse(roh) : {};
      res.status = (c) => { res.statusCode = c; return res; };
      res.json = (d) => { res.setHeader('Content-Type', 'application/json'); res.end(JSON.stringify(d)); };
      story(req, res);
    });
    return;
  }
  const datei = join(HIER, 'public', url.pathname === '/' ? 'index.html' : url.pathname);
  if (!existsSync(datei)) { res.statusCode = 404; return res.end('nicht gefunden'); }
  res.setHeader('Content-Type', TYP[extname(datei)] || 'application/octet-stream');
  res.end(readFileSync(datei));
}).listen(4415, () => console.log('Story-Generator lokal: http://localhost:4415'));
