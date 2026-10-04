// Einmaliger Tiefen-Abruf: die letzten N Beiträge ausgewählter Konten.
//
// Der tägliche Scrape (scrape-competitors.js) holt je Konto nur die 12 neuesten
// Beiträge. Für die Nischen-Analyse der Hook-Maschine (plans/2026-10-04-hook-maschine.md)
// braucht es die Geschichte: rund 200 Beiträge je Konto. Patricia hat den Abruf am
// 04.10.2026 freigegeben (etwa 2–3 Franken Apify-Guthaben).
//
// Läuft als GitHub Action (.github/workflows/apify-tiefe.yml), weil der Apify-Schlüssel
// nur dort als Secret liegt. Ergebnis: outputs/apify-runs/tiefe-JJJJ-MM-TT.json
//
// Asynchron (Run starten → warten → Datensatz holen): 600+ Beiträge sprengen das
// 300-Sekunden-Limit von run-sync.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..', '..');
const ACTOR = 'apify~instagram-scraper';
const token = process.env.APIFY_API_TOKEN;
if (!token) {
  console.error('APIFY_API_TOKEN fehlt');
  process.exit(1);
}

const handles = (process.env.HANDLES || '').split(',').map((h) => h.trim().replace(/^@/, '')).filter(Boolean);
const limit = parseInt(process.env.LIMIT || '200', 10);
if (handles.length === 0) {
  console.error('Keine Handles angegeben (HANDLES)');
  process.exit(1);
}
console.log(`Tiefen-Abruf: ${handles.join(', ')} · je ${limit} Beiträge`);

const api = (p) => `https://api.apify.com/v2${p}${p.includes('?') ? '&' : '?'}token=${token}`;

const start = await fetch(api(`/acts/${ACTOR}/runs`), {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    directUrls: handles.map((h) => `https://www.instagram.com/${h}/`),
    resultsType: 'posts',
    resultsLimit: limit,
    addParentData: false,
  }),
});
if (!start.ok) {
  console.error(`Start fehlgeschlagen: HTTP ${start.status} ${(await start.text()).slice(0, 400)}`);
  process.exit(1);
}
const run = (await start.json()).data;
console.log(`Run ${run.id} gestartet`);

let status = run.status;
const bis = Date.now() + 50 * 60 * 1000;
while (!['SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT'].includes(status)) {
  if (Date.now() > bis) {
    console.error('Zeitlimit erreicht, Run läuft noch');
    process.exit(1);
  }
  await new Promise((r) => setTimeout(r, 15000));
  const r = await fetch(api(`/actor-runs/${run.id}`));
  status = (await r.json()).data.status;
  console.log(`  Status: ${status}`);
}
if (status !== 'SUCCEEDED') {
  console.error(`Run endete mit ${status}`);
  process.exit(1);
}

const items = await (await fetch(api(`/datasets/${run.defaultDatasetId}/items?clean=true&format=json`))).json();
const posts = items.filter((p) => p.shortCode);
const je = {};
for (const p of posts) je[p.ownerUsername] = (je[p.ownerUsername] || 0) + 1;
console.log(`Beiträge: ${posts.length}`, je);

const date = new Date().toISOString().slice(0, 10);
const ziel = path.join(REPO_ROOT, 'outputs', 'apify-runs', `tiefe-${date}.json`);
fs.writeFileSync(ziel, JSON.stringify({ date, handles, limit, je_konto: je, posts }, null, 1));
console.log(`→ ${path.relative(REPO_ROOT, ziel)}`);
