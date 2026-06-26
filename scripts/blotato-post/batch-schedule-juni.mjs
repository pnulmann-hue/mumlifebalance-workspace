/**
 * Batch-Schedule alle 6 Juni-Karussells direkt aus der Sandbox.
 * Nutzt GitHub Raw URLs als Source — Blotato fetcht selber.
 * Workflow:
 *   1. Pro Karussell: Config laden
 *   2. mediaUrls mit GitHub Raw URLs ersetzen
 *   3. POST /v2/media für jede URL (Blotato hostet auf CDN)
 *   4. POST /v2/posts mit Blotato-CDN-URLs + scheduledTime
 *   5. Submission-ID loggen
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WORKSPACE_ROOT = path.resolve(__dirname, '..', '..');

// --- .env laden ---
const envContent = await fs.readFile(path.join(__dirname, '.env'), 'utf8');
const envMap = Object.fromEntries(
  envContent.split('\n').filter(l => l.includes('=') && !l.startsWith('#')).map(l => {
    const [k, ...rest] = l.split('=');
    return [k.trim(), rest.join('=').trim().replace(/^["']|["']$/g, '')];
  })
);
const BLOTATO_API_KEY = envMap.BLOTATO_API_KEY;
if (!BLOTATO_API_KEY) throw new Error('BLOTATO_API_KEY fehlt in scripts/blotato-post/.env');

const BLOTATO_BASE = 'https://backend.blotato.com';
const HEADERS = {
  'Content-Type': 'application/json',
  'blotato-api-key': BLOTATO_API_KEY,
};

const GH_RAW_BASE = 'https://raw.githubusercontent.com/pnulmann-hue/mumlifebalance-workspace/main';

// --- Posts zu schedulen ---
const POSTS = [
  { config: '2026-06-16-di-mentoring-echt1-leadmagnet.json',           slidesDir: 'outputs/karussells/2026-06-echt1-leadmagnet/png' },
  { config: '2026-06-18-do-mentoring-story-putzen.json',              slidesDir: 'outputs/karussells/2026-06-story-beim-putzen/png' },
  { config: '2026-06-23-di-mentoring-echt1-teamcall.json',            slidesDir: 'outputs/karussells/2026-06-echt1-teamcall-anfrage/png' },
  { config: '2026-06-26-fr-mentoring-bootcamp-aus-dem-bauch.json',    slidesDir: 'outputs/karussells/2026-06-bootcamp-aus-dem-bauch/png' },
  { config: '2026-06-29-mo-mentoring-100-follower-anfragen.json',     slidesDir: 'outputs/karussells/2026-06-100-follower-anfragen/png' },
  { config: '2026-07-01-mi-mentoring-network-standbein.json',         slidesDir: 'outputs/karussells/2026-06-network-standbein/png' },
];

async function uploadMediaUrl(sourceUrl, idx) {
  const res = await fetch(`${BLOTATO_BASE}/v2/media`, {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify({ url: sourceUrl }),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`Media-Upload #${idx + 1} fehlgeschlagen (HTTP ${res.status}): ${text.slice(0, 300)}`);
  const json = JSON.parse(text);
  const hosted = json.url || json.mediaUrl || json.publicUrl;
  if (!hosted) throw new Error(`Media-Upload #${idx + 1}: keine URL in Response: ${text.slice(0, 300)}`);
  return hosted;
}

async function schedulePost(post) {
  const cfgPath = path.join(__dirname, 'post-configs', post.config);
  const cfg = JSON.parse(await fs.readFile(cfgPath, 'utf8'));

  // 1. Slide-URLs konstruieren (slide-01.png ... slide-07.png)
  const slideUrls = [];
  for (let i = 1; i <= 7; i++) {
    const num = String(i).padStart(2, '0');
    slideUrls.push(`${GH_RAW_BASE}/${post.slidesDir}/slide-${num}.png`);
  }

  console.log(`\n=== ${post.config} ===`);
  console.log(`Scheduled: ${cfg.scheduledTime} · Account: ${cfg.accountId} · Slides: ${slideUrls.length}`);

  // 2. Bilder zu Blotato hochladen (Blotato fetcht via URL)
  console.log('Upload zu Blotato CDN ...');
  const hosted = [];
  for (let i = 0; i < slideUrls.length; i++) {
    try {
      const url = await uploadMediaUrl(slideUrls[i], i);
      hosted.push(url);
      console.log(`  [${i + 1}/${slideUrls.length}] ${url.slice(0, 80)}...`);
    } catch (err) {
      console.error(`  [${i + 1}/${slideUrls.length}] FEHLER: ${err.message}`);
      return { ok: false, error: err.message };
    }
  }

  // 3. Post schedulen
  const body = {
    post: {
      accountId: cfg.accountId,
      content: {
        text: cfg.text,
        mediaUrls: hosted,
        platform: cfg.platform,
      },
      target: { targetType: cfg.platform },
    },
    scheduledTime: cfg.scheduledTime,
  };

  const res = await fetch(`${BLOTATO_BASE}/v2/posts`, {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify(body),
  });
  const text = await res.text();
  let json;
  try { json = JSON.parse(text); } catch { json = { raw: text }; }

  if (!res.ok) {
    console.error(`  ❌ Schedule-FEHLER (HTTP ${res.status}): ${text.slice(0, 500)}`);
    return { ok: false, error: text.slice(0, 500) };
  }

  console.log(`  ✅ Submission-ID: ${json.id || json.submissionId || JSON.stringify(json).slice(0, 200)}`);

  // 4. Config mit Blotato-CDN-URLs aktualisieren (für Re-Run / Tracking)
  cfg.mediaUrls = hosted;
  cfg._submissionId = json.id || json.submissionId;
  cfg._scheduledAt = new Date().toISOString();
  await fs.writeFile(cfgPath, JSON.stringify(cfg, null, 2));

  return { ok: true, id: json.id || json.submissionId };
}

// --- Run all ---
const results = [];
for (const post of POSTS) {
  try {
    const r = await schedulePost(post);
    results.push({ post: post.config, ...r });
  } catch (err) {
    console.error(`FATAL für ${post.config}: ${err.message}`);
    results.push({ post: post.config, ok: false, error: err.message });
  }
}

console.log('\n\n========== ZUSAMMENFASSUNG ==========');
for (const r of results) {
  console.log(`${r.ok ? '✅' : '❌'} ${r.post}${r.id ? ` → ${r.id}` : ''}${r.error ? ` (${r.error.slice(0, 100)})` : ''}`);
}
