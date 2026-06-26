/**
 * Karussells für 18:30 einplanen.
 * Re-schedule alle 7 Karussells (mediaUrls bleiben gleich — Blotato-CDN URLs).
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

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

const CONFIGS = [
  '2026-06-15-mo-mentoring-bootcamp-promo-viral.json',
  '2026-06-16-di-mentoring-echt1-leadmagnet.json',
  '2026-06-18-do-mentoring-story-putzen.json',
  '2026-06-23-di-mentoring-echt1-teamcall.json',
  '2026-06-26-fr-mentoring-bootcamp-aus-dem-bauch.json',
  '2026-06-29-mo-mentoring-100-follower-anfragen.json',
  '2026-07-01-mi-mentoring-network-standbein.json',
];

const results = { success: [], failed: [] };

for (const configFile of CONFIGS) {
  console.log(`\n[KARUSSELL] ${configFile}`);
  try {
    const cfgPath = path.join(__dirname, 'post-configs', configFile);
    const cfg = JSON.parse(await fs.readFile(cfgPath, 'utf8'));

    const body = {
      post: {
        accountId: cfg.accountId,
        content: {
          text: cfg.text,
          mediaUrls: cfg.mediaUrls,
          platform: 'instagram',
        },
        target: { targetType: 'instagram' },
      },
      scheduledTime: cfg.scheduledTime,
    };

    console.log(`  Schedule for ${cfg.scheduledTime}, ${cfg.mediaUrls.length} slides`);
    const res = await fetch(`${BLOTATO_BASE}/v2/posts`, {
      method: 'POST', headers: HEADERS, body: JSON.stringify(body),
    });
    if (!res.ok) {
      const err = await res.text();
      throw new Error(`${res.status}: ${err.substring(0, 200)}`);
    }
    const data = await res.json();
    console.log(`  ✓ NEW Submission: ${JSON.stringify(data).substring(0, 120)}`);

    // Update config with new submissionId
    cfg._newSubmissionId = data.postSubmissionId || data.id;
    cfg._newScheduledAt = new Date().toISOString();
    await fs.writeFile(cfgPath, JSON.stringify(cfg, null, 2), 'utf8');

    results.success.push({ config: configFile, submission: cfg._newSubmissionId });
  } catch (e) {
    console.error(`  ✗ FAIL: ${e.message}`);
    results.failed.push({ config: configFile, error: e.message });
  }
  await new Promise(r => setTimeout(r, 4000));
}

console.log(`\n=== DONE: ${results.success.length} success, ${results.failed.length} failed ===`);
results.failed.forEach(f => console.log(`  - ${f.config}: ${f.error}`));
