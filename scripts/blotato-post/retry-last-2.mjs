/**
 * Retry-Schedule für die 2 Karussells die vom Rate-Limit erwischt wurden.
 * 60s initial-wait, dann 8s Throttle zwischen Media-Uploads.
 */
import fs from 'node:fs/promises';

const envContent = await fs.readFile(new URL('./.env', import.meta.url), 'utf8');
const key = envContent.match(/BLOTATO_API_KEY=(.+)/)[1].trim().replace(/^["']|["']$/g, '');
const HEADERS = { 'Content-Type': 'application/json', 'blotato-api-key': key };
const BASE = 'https://backend.blotato.com';
const GH = 'https://raw.githubusercontent.com/pnulmann-hue/mumlifebalance-workspace/main';

const POSTS = [
  { config: '2026-06-29-mo-mentoring-100-follower-anfragen.json', slidesDir: 'outputs/karussells/2026-06-100-follower-anfragen/png' },
  { config: '2026-07-01-mi-mentoring-network-standbein.json',     slidesDir: 'outputs/karussells/2026-06-network-standbein/png' },
];

const sleep = ms => new Promise(r => setTimeout(r, ms));

console.log('Initial-Wait 60s für Rate-Limit-Reset ...');
await sleep(60000);
console.log('Go.');

for (const p of POSTS) {
  const cfgPath = new URL(`./post-configs/${p.config}`, import.meta.url);
  const cfg = JSON.parse(await fs.readFile(cfgPath, 'utf8'));
  console.log(`\n=== ${p.config} ===`);
  const hosted = [];
  for (let i = 1; i <= 7; i++) {
    const num = String(i).padStart(2, '0');
    const url = `${GH}/${p.slidesDir}/slide-${num}.png`;
    let retries = 4;
    while (retries > 0) {
      const r = await fetch(`${BASE}/v2/media`, { method: 'POST', headers: HEADERS, body: JSON.stringify({ url }) });
      const t = await r.text();
      if (r.ok) {
        const j = JSON.parse(t);
        hosted.push(j.url || j.mediaUrl || j.publicUrl);
        console.log(`  [${i}/7] uploaded`);
        break;
      }
      if (r.status === 429) {
        console.log(`  [${i}/7] rate-limited (try ${5 - retries}/4), wait 50s ...`);
        await sleep(50000);
        retries--;
      } else {
        console.error(`  [${i}/7] FEHLER: HTTP ${r.status} ${t.slice(0, 200)}`);
        throw new Error('upload failed');
      }
    }
    if (retries === 0) throw new Error(`Retry erschöpft für slide ${num}`);
    await sleep(8000);
  }
  const body = {
    post: {
      accountId: cfg.accountId,
      content: { text: cfg.text, mediaUrls: hosted, platform: cfg.platform },
      target: { targetType: cfg.platform },
    },
    scheduledTime: cfg.scheduledTime,
  };
  const r = await fetch(`${BASE}/v2/posts`, { method: 'POST', headers: HEADERS, body: JSON.stringify(body) });
  const t = await r.text();
  const j = JSON.parse(t);
  console.log(`  ✅ Submission: ${j.id || j.postSubmissionId || JSON.stringify(j)}`);
  cfg.mediaUrls = hosted;
  cfg._submissionId = j.id || j.postSubmissionId;
  cfg._scheduledAt = new Date().toISOString();
  await fs.writeFile(cfgPath, JSON.stringify(cfg, null, 2));
  await sleep(10000);
}
console.log('\nFertig.');
