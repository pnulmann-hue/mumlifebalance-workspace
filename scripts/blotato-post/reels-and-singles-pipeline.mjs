/**
 * Blotato Upload + Schedule für:
 *  - 7 Reels (BIO + POV excluded)
 *  - 3 Single-Image-Posts
 *  - 7 Karussells (5 neu uploaden, 2 cancel+neu schedule)
 *
 * Workflow pro Video/Image:
 *   1. Push MP4/PNG nach GitHub Repo (für Raw URL)
 *   2. POST /v2/media mit Raw URL (Blotato fetcht selber)
 *   3. POST /v2/posts mit Blotato-CDN-URL + scheduledTime
 *   4. Submission-ID loggen
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WORKSPACE = path.resolve(__dirname, '..', '..');

// --- .env laden ---
const envContent = await fs.readFile(path.join(__dirname, '.env'), 'utf8');
const envMap = Object.fromEntries(
  envContent.split('\n').filter(l => l.includes('=') && !l.startsWith('#')).map(l => {
    const [k, ...rest] = l.split('=');
    return [k.trim(), rest.join('=').trim().replace(/^["']|["']$/g, '')];
  })
);
const BLOTATO_API_KEY = envMap.BLOTATO_API_KEY;
if (!BLOTATO_API_KEY) throw new Error('BLOTATO_API_KEY fehlt');
const BLOTATO_BASE = 'https://backend.blotato.com';
const HEADERS = {
  'blotato-api-key': BLOTATO_API_KEY,
  'Content-Type': 'application/json',
};

const GH_RAW_BASE = 'https://raw.githubusercontent.com/pnulmann-hue/mumlifebalance-workspace/main';
const ACCOUNT_ID = '41414';  // Mentoring

const READ_CAPTIONS_FILE = path.join(WORKSPACE, 'outputs/content-kalender/2026-06-captions-v2.md');

// Mapping: slug → caption-section in V2.md (positions 1-13)
const REEL_POSTS = [
  // Reels (mediaType: video)
  { slug: '2026-06-10-story-story-idee-dms', section: 2, type: 'reel', date: '2026-06-10T18:30:00+02:00' },
  { slug: '2026-06-17-sponsorin-poste-mehr', section: 3, type: 'reel', date: '2026-06-17T18:30:00+02:00' },
  { slug: '2026-06-19-webinar-bootcamp-pivot', section: 4, type: 'reel', date: '2026-06-19T18:30:00+02:00' },
  { slug: '2026-06-22-bootcamp-was-passiert', section: 5, type: 'reel', date: '2026-06-22T18:30:00+02:00' },
  { slug: '2026-06-24-liebe-kinder-mein-ding', section: 6, type: 'reel', date: '2026-06-24T18:30:00+02:00' },
  { slug: '2026-06-25-bootcamp-sommer-postest', section: 7, type: 'reel', date: '2026-06-25T18:30:00+02:00' },
  { slug: '2026-06-30-mein-mittwoch', section: 8, type: 'reel', date: '2026-06-30T18:30:00+02:00' },
  { slug: '2026-07-03-heute-oeffnet-sich', section: 9, type: 'reel', date: '2026-07-03T18:30:00+02:00' },
];

const SINGLE_POSTS = [
  { slug: '2026-06-produktbilder-reichweite', section: 10, type: 'single', date: '2026-06-11T18:30:00+02:00', pngs: ['1.png'] },
  { slug: '2026-06-sonntag-21-uhr', section: 11, type: 'single', date: '2026-06-12T18:30:00+02:00', pngs: ['1.png'] },
  { slug: '2026-06-5-mamas-zusammen', section: 12, type: 'single', date: '2026-07-02T18:30:00+02:00', pngs: ['1.png'] },
];

async function loadCaption(section) {
  const md = await fs.readFile(READ_CAPTIONS_FILE, 'utf8');
  // Find section by number (1-13)
  const headerRegex = new RegExp(`^##\\s.*?${section}.*$`, 'gm');
  const headers = [...md.matchAll(headerRegex)];
  // Use ordinal index - V2 file has emoji prefixes like 1️⃣ 2️⃣ etc.
  // Simpler: just find sections by ## marker order
  const sections = md.split(/\n##\s/).slice(1);  // each section
  if (section > sections.length) throw new Error(`Section ${section} not found`);
  const sec = sections[section - 1];
  // Extract content between first ``` and second ```
  const match = sec.match(/```\n([\s\S]+?)\n```/);
  if (!match) throw new Error(`No code block in section ${section}`);
  return match[1].trim();
}

async function uploadMedia(url) {
  console.log(`  Upload to Blotato: ${url.substring(0, 80)}...`);
  const res = await fetch(`${BLOTATO_BASE}/v2/media`, {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify({ url }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Media upload failed: ${res.status} ${err}`);
  }
  const data = await res.json();
  console.log(`  ✓ Blotato URL: ${data.url}`);
  return data.url;
}

async function schedulePost(post, mediaUrls, text) {
  const isReel = post.type === 'reel';
  const body = {
    accountId: ACCOUNT_ID,
    platform: 'instagram',
    mediaType: isReel ? 'video' : 'image',
    scheduledTime: post.date,
    text,
    mediaUrls,
  };
  console.log(`  Schedule ${post.slug} for ${post.date}...`);
  const res = await fetch(`${BLOTATO_BASE}/v2/posts`, {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Schedule failed: ${res.status} ${err}`);
  }
  const data = await res.json();
  console.log(`  ✓ Submission ID: ${data.submissionId || data.id || JSON.stringify(data).substring(0, 100)}`);
  return data;
}

async function processReel(post) {
  console.log(`\n[REEL] ${post.slug}`);
  const caption = await loadCaption(post.section);
  const compressedPath = `outputs/reels-compressed/${post.slug}.mp4`;
  const ghUrl = `${GH_RAW_BASE}/${compressedPath}`;
  const blotatoUrl = await uploadMedia(ghUrl);
  const result = await schedulePost(post, [blotatoUrl], caption);
  return result;
}

async function processSingle(post) {
  console.log(`\n[SINGLE] ${post.slug}`);
  const caption = await loadCaption(post.section);
  const mediaUrls = [];
  for (const png of post.pngs) {
    const pngPath = `outputs/single-image/${post.slug}/png/${png}`;
    const ghUrl = `${GH_RAW_BASE}/${pngPath}`;
    const blotatoUrl = await uploadMedia(ghUrl);
    mediaUrls.push(blotatoUrl);
  }
  const result = await schedulePost(post, mediaUrls, caption);
  return result;
}

async function main() {
  const results = { success: [], failed: [] };
  for (const post of [...REEL_POSTS, ...SINGLE_POSTS]) {
    try {
      const result = post.type === 'reel' ? await processReel(post) : await processSingle(post);
      results.success.push({ slug: post.slug, data: result });
    } catch (e) {
      console.error(`  ✗ FAIL: ${e.message}`);
      results.failed.push({ slug: post.slug, error: e.message });
    }
    // Throttle to avoid rate limit
    await new Promise(r => setTimeout(r, 5000));
  }
  console.log(`\n=== DONE ===`);
  console.log(`Success: ${results.success.length}`);
  console.log(`Failed: ${results.failed.length}`);
  results.failed.forEach(f => console.log(`  - ${f.slug}: ${f.error}`));
}

main().catch(e => { console.error('FATAL:', e); process.exit(1); });
