/**
 * NUR die 3 Single-Image-Posts via Blotato (Retry).
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

const READ_CAPTIONS_FILE = path.join(WORKSPACE, 'outputs/content-kalender/2026-06-captions-v2.md');

const SINGLE_POSTS = [
  { slug: '2026-06-produktbilder-reichweite', section: 10, date: '2026-06-11T18:30:00+02:00', pngs: ['01.png', '02.png'] },
  { slug: '2026-06-sonntag-21-uhr', section: 11, date: '2026-06-12T18:30:00+02:00', pngs: ['01.png', '02.png'] },
  { slug: '2026-06-5-mamas-zusammen', section: 12, date: '2026-07-02T18:30:00+02:00', pngs: ['01.png', '02.png'] },
];

async function loadCaption(section) {
  const md = await fs.readFile(READ_CAPTIONS_FILE, 'utf8');
  const sections = md.split(/\n##\s/).slice(1);
  if (section > sections.length) throw new Error(`Section ${section} not found`);
  const sec = sections[section - 1];
  const match = sec.match(/```\n([\s\S]+?)\n```/);
  if (!match) throw new Error(`No code block in section ${section}`);
  return match[1].trim();
}

async function uploadMedia(url) {
  console.log(`  Upload: ${url.split('/').pop()}`);
  const res = await fetch(`${BLOTATO_BASE}/v2/media`, {
    method: 'POST', headers: HEADERS, body: JSON.stringify({ url }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Upload failed: ${res.status} ${err.substring(0, 200)}`);
  }
  const data = await res.json();
  return data.url;
}

async function schedulePost(post, mediaUrls, text) {
  const body = {
    post: {
      accountId: ACCOUNT_ID,
      content: { text, mediaUrls, platform: 'instagram' },
      target: { targetType: 'instagram' },
    },
    scheduledTime: post.date,
  };
  const res = await fetch(`${BLOTATO_BASE}/v2/posts`, {
    method: 'POST', headers: HEADERS, body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Schedule failed: ${res.status} ${err.substring(0, 200)}`);
  }
  return await res.json();
}

const results = { success: [], failed: [] };
for (const post of SINGLE_POSTS) {
  console.log(`\n[SINGLE] ${post.slug}`);
  try {
    const caption = await loadCaption(post.section);
    const mediaUrls = [];
    for (const png of post.pngs) {
      const ghUrl = `${GH_RAW_BASE}/outputs/single-image/${post.slug}/png/${png}`;
      const blotatoUrl = await uploadMedia(ghUrl);
      mediaUrls.push(blotatoUrl);
    }
    const result = await schedulePost(post, mediaUrls, caption);
    console.log(`  ✓ Submission: ${JSON.stringify(result).substring(0, 100)}`);
    results.success.push({ slug: post.slug, result });
  } catch (e) {
    console.error(`  ✗ FAIL: ${e.message}`);
    results.failed.push({ slug: post.slug, error: e.message });
  }
  await new Promise(r => setTimeout(r, 4000));
}

console.log(`\n=== DONE: ${results.success.length} success, ${results.failed.length} failed ===`);
