/**
 * Re-Schedule der 4 ABAB-Fix-Posts via Blotato (11.6.2026).
 * Uploadet alle Slides neu zu Blotato CDN + erstellt neue Submissions.
 * Die ALTEN Submissions bleiben — Patricia muss die in Blotato-UI manuell canceln.
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

// 4 Posts mit Pfad-Mapping + Caption-Section
const POSTS = [
  {
    slug: '2026-06-sonntag-21-uhr',
    folder: 'single-image',
    section: 11,
    date: '2026-06-12T18:30:00+02:00',
    pngs: ['01.png', '02.png'],
  },
  {
    slug: '2026-06-echt1-teamcall-anfrage',
    folder: 'karussells',
    section: null, // Karussell caption from config
    configFile: '2026-06-23-di-mentoring-echt1-teamcall.json',
    date: '2026-06-23T18:30:00+02:00',
    pngs: ['01.png', '02.png', '03.png', '04.png', '05.png', '06.png', '07.png'],
  },
  {
    slug: '2026-06-network-standbein',
    folder: 'karussells',
    section: null,
    configFile: '2026-07-01-mi-mentoring-network-standbein.json',
    date: '2026-07-01T18:30:00+02:00',
    pngs: ['01.png', '02.png', '03.png', '04.png', '05.png', '06.png', '07.png'],
  },
  {
    slug: '2026-06-5-mamas-zusammen',
    folder: 'single-image',
    section: 12,
    date: '2026-07-02T18:30:00+02:00',
    pngs: ['01.png', '02.png'],
  },
];

async function loadCaptionFromSection(section) {
  const md = await fs.readFile(READ_CAPTIONS_FILE, 'utf8');
  const sections = md.split(/\n##\s/).slice(1);
  if (section > sections.length) throw new Error(`Section ${section} not found`);
  const sec = sections[section - 1];
  const match = sec.match(/```\n([\s\S]+?)\n```/);
  if (!match) throw new Error(`No code block in section ${section}`);
  return match[1].trim();
}

async function loadCaptionFromConfig(configFile) {
  const cfgPath = path.join(__dirname, 'post-configs', configFile);
  const cfg = JSON.parse(await fs.readFile(cfgPath, 'utf8'));
  return cfg.text;
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

for (const post of POSTS) {
  console.log(`\n[POST] ${post.slug} → ${post.date}`);
  try {
    const caption = post.section
      ? await loadCaptionFromSection(post.section)
      : await loadCaptionFromConfig(post.configFile);

    const mediaUrls = [];
    for (const png of post.pngs) {
      const ghUrl = `${GH_RAW_BASE}/outputs/${post.folder}/${post.slug}/png/${png}`;
      const blotatoUrl = await uploadMedia(ghUrl);
      mediaUrls.push(blotatoUrl);
      await new Promise(r => setTimeout(r, 1500));
    }

    const result = await schedulePost(post, mediaUrls, caption);
    const newSubId = result.postSubmissionId || result.id || JSON.stringify(result).substring(0, 80);
    console.log(`  ✓ NEW Submission: ${newSubId}`);

    // Update config if exists
    if (post.configFile) {
      const cfgPath = path.join(__dirname, 'post-configs', post.configFile);
      const cfg = JSON.parse(await fs.readFile(cfgPath, 'utf8'));
      cfg._oldSubmissionId = cfg._submissionId || cfg._newSubmissionId;
      cfg._newSubmissionId_v2 = newSubId;
      cfg._abab_fix_at = '2026-06-11';
      cfg.mediaUrls = mediaUrls;
      await fs.writeFile(cfgPath, JSON.stringify(cfg, null, 2), 'utf8');
    }

    results.success.push({ slug: post.slug, submission: newSubId });
  } catch (e) {
    console.error(`  ✗ FAIL: ${e.message}`);
    results.failed.push({ slug: post.slug, error: e.message });
  }
  await new Promise(r => setTimeout(r, 4000));
}

console.log(`\n=== ${results.success.length} success · ${results.failed.length} failed ===`);
results.failed.forEach(f => console.log(`  ✗ ${f.slug}: ${f.error}`));
results.success.forEach(s => console.log(`  ✓ ${s.slug}: ${s.submission}`));
