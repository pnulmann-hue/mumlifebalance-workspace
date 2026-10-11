// Lokaler Test des Stimm-Checks ohne Vercel: ruft den Handler direkt auf.
// Schlüssel kommt aus einer vorhandenen .env (nie ausgeben, nie in den Code).
//   node test-lokal.mjs [pfad-zur-.env]
import { readFileSync, writeFileSync } from 'node:fs';
import handler from './api/generate.js';

const envPfad = process.argv[2] || '../startklar-service/.env';
for (const zeile of readFileSync(envPfad, 'utf-8').split(/\r?\n/)) {
  const m = zeile.match(/^\s*(ANTHROPIC_API_KEY|ANTHROPIC_MODEL)\s*=\s*"?([^"\s]+)"?/);
  if (m) process.env[m[1]] = m[2];
}
if (!process.env.ANTHROPIC_API_KEY) { console.error('Kein ANTHROPIC_API_KEY in', envPfad); process.exit(1); }

function rufe(body) {
  return new Promise((resolve) => {
    const res = { code: 200, status(c) { this.code = c; return this; }, json(d) { resolve({ code: this.code, d }); } };
    handler({ method: 'POST', body }, res);
  });
}

const angaben = JSON.parse(readFileSync(process.argv[3] || './test-angaben.json', 'utf-8'));
const t0 = Date.now();
const s1 = await rufe({ step: 1, angaben });
console.log(`Schritt 1: HTTP ${s1.code} nach ${((Date.now() - t0) / 1000).toFixed(1)} s`);
if (s1.code !== 200) { console.log(s1.d); process.exit(1); }

const t1 = Date.now();
const s2 = await rufe({ step: 2, brief: s1.d.brief, auftrag: { format: 'caption', thema: process.argv[4] || 'Warum ich abends nicht mehr alles im Kopf durchgehe' } });
console.log(`Schritt 2: HTTP ${s2.code} nach ${((Date.now() - t1) / 1000).toFixed(1)} s`);

writeFileSync('./test-ergebnis.json', JSON.stringify({ schritt1: s1.d, schritt2: s2.d }, null, 2));
console.log('→ test-ergebnis.json');
