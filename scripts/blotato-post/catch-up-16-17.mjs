/**
 * CATCH-UP: Posts die nicht raus gingen
 *  - Echt1-Leadmagnet (war für Di 16.6. 18:30): JETZT + 3 Min nachposten
 *  - Sponsorin-Reel (Mi 17.6. 18:30): neu schedulen (Datei auf GitHub)
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WORKSPACE = path.resolve(__dirname, '..', '..');

const envContent = await fs.readFile(path.join(__dirname, '.env'), 'utf8');
const envMap = Object.fromEntries(
  envContent.split('\n').filter(l => l.includes('=') && !l.startsWith('#')).map(l => {
    const [k, ...rest] = l.split('=');
    return [k.trim(), rest.join('=').trim().replace(/^["']|["']$/g, '')];
  })
);
const BLOTATO_API_KEY = envMap.BLOTATO_API_KEY;
const BLOTATO_BASE = 'https://backend.blotato.com';
const HEADERS = { 'blotato-api-key': BLOTATO_API_KEY, 'Content-Type': 'application/json' };
const GH_RAW_BASE = 'https://raw.githubusercontent.com/pnulmann-hue/mumlifebalance-workspace/main';
const ACCOUNT_ID = '41414';

async function uploadMedia(url) {
  console.log(`  Upload: ${url.split('/').pop()}`);
  const res = await fetch(`${BLOTATO_BASE}/v2/media`, {
    method: 'POST', headers: HEADERS, body: JSON.stringify({ url }),
  });
  if (!res.ok) throw new Error(`Upload failed: ${res.status} ${await res.text()}`);
  return (await res.json()).url;
}

async function scheduleNow(accountId, mediaUrls, text, scheduledTime) {
  const body = {
    post: {
      accountId,
      content: { text, mediaUrls, platform: 'instagram' },
      target: { targetType: 'instagram' },
    },
    scheduledTime,
  };
  const res = await fetch(`${BLOTATO_BASE}/v2/posts`, {
    method: 'POST', headers: HEADERS, body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Schedule failed: ${res.status} ${await res.text()}`);
  return await res.json();
}

// === JOB 1: Echt1-Leadmagnet ASAP nachposten ===
console.log('\n[JOB 1] Echt1-Leadmagnet — sofort (für gestern Di 16.6.) nachposten');
const cfg = JSON.parse(await fs.readFile(
  path.join(__dirname, 'post-configs/2026-06-16-di-mentoring-echt1-leadmagnet.json'),
  'utf8'
));

// Re-upload alle 7 PNGs frisch zu Blotato (alte URLs könnten stale sein)
const echtMediaUrls = [];
for (let i = 1; i <= 7; i++) {
  const png = String(i).padStart(2, '0') + '.png';
  const ghUrl = `${GH_RAW_BASE}/outputs/karussells/2026-06-echt1-leadmagnet/png/${png}`;
  const blotatoUrl = await uploadMedia(ghUrl);
  echtMediaUrls.push(blotatoUrl);
  await new Promise(r => setTimeout(r, 1200));
}

// JETZT = 3 Minuten ab jetzt
// Hardcoded time: aktuelle Zeit ist ca. Mi 17.6. 11:00 → schedule für 11:30
// Sicher: nehmen wir +10 Min als Puffer
const nowPlusMin = new Date(Date.now() + 5 * 60 * 1000).toISOString();
console.log('  Schedule echt1 für:', nowPlusMin);
const echtResult = await scheduleNow(ACCOUNT_ID, echtMediaUrls, cfg.text, nowPlusMin);
console.log('  ✓ Echt1 Submission:', echtResult.postSubmissionId || echtResult.id);

// === JOB 2: Sponsorin-Reel für heute 18:30 ===
console.log('\n[JOB 2] Sponsorin-Reel — neu schedulen für Mi 17.6. 18:30');
const captions = await fs.readFile(
  path.join(WORKSPACE, 'outputs/content-kalender/2026-06-captions-v2.md'), 'utf8'
);
const sections = captions.split(/\n##\s/).slice(1);
const sponsorinCaption = sections[2].match(/```\n([\s\S]+?)\n```/)[1].trim();

const sponsorinGhUrl = `${GH_RAW_BASE}/outputs/reels-compressed/2026-06-17-sponsorin-poste-mehr.mp4`;
const sponsorinBlotato = await uploadMedia(sponsorinGhUrl);
const sponsorinResult = await scheduleNow(
  ACCOUNT_ID,
  [sponsorinBlotato],
  sponsorinCaption,
  '2026-06-17T18:30:00+02:00'
);
console.log('  ✓ Sponsorin Submission:', sponsorinResult.postSubmissionId || sponsorinResult.id);

console.log('\n=== DONE ===');
console.log(`Echt1-Leadmagnet:    ${echtResult.postSubmissionId || echtResult.id}`);
console.log(`Sponsorin-Reel:      ${sponsorinResult.postSubmissionId || sponsorinResult.id}`);
