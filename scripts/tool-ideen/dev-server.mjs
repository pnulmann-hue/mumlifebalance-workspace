// Lokaler Testserver für den Tool-Ideen-Generator — ahmt Vercel nach (public/ + /api/ideen).
//   node dev-server.mjs   → http://localhost:4413
// Schlüssel: Claude aus startklar-service/.env, ActiveCampaign aus 04-projects/activecampaign-mcp/.env.
// Nichts davon wird ausgegeben.
import http from 'node:http';
import { readFileSync, existsSync } from 'node:fs';
import { join, extname, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import ideen from './api/ideen.js';

const HIER = dirname(fileURLToPath(import.meta.url));
process.chdir(HIER);
const WURZEL = join(HIER, '..', '..');
for (const pfad of [join(HIER, '..', 'startklar-service', '.env'), join(WURZEL, '04-projects', 'activecampaign-mcp', '.env')]) {
  for (const zeile of readFileSync(pfad, 'utf-8').split(/\r?\n/)) {
    const m = zeile.match(/^\s*(ANTHROPIC_API_KEY|ANTHROPIC_MODEL|AC_API_URL|AC_API_KEY)\s*=\s*"?([^"\s]+)"?/);
    if (m) process.env[m[1]] = m[2];
  }
}
const TYP = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.jpg': 'image/jpeg' };

http.createServer((req, res) => {
  const url = new URL(req.url, 'http://x');
  if (url.pathname === '/api/ideen') {
    let roh = '';
    req.on('data', (c) => { roh += c; });
    req.on('end', () => {
      req.body = roh ? JSON.parse(roh) : {};
      res.status = (c) => { res.statusCode = c; return res; };
      res.json = (d) => { res.setHeader('Content-Type', 'application/json'); res.end(JSON.stringify(d)); };
      ideen(req, res);
    });
    return;
  }
  const datei = join(HIER, 'public', url.pathname === '/' ? 'index.html' : url.pathname);
  if (!existsSync(datei)) { res.statusCode = 404; return res.end('nicht gefunden'); }
  res.setHeader('Content-Type', TYP[extname(datei)] || 'application/octet-stream');
  res.end(readFileSync(datei));
}).listen(4413, () => console.log('Tool-Ideen lokal: http://localhost:4413'));
