/**
 * Retry: 5-Mamas Foto-Cover für Do 2.7. 18:30 nochmal hochladen.
 * Patricia hat versehentlich den NEUEN gelöscht statt den ALTEN.
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

const POST = {
  slug: '2026-06-5-mamas-zusammen',
  folder: 'single-image',
  section: 12,
  date: '2026-07-02T18:30:00+02:00',
  pngs: ['01.png', '02.png'],
};

async function loadCaption(section) {
  const md = await fs.readFile(
    path.join(WORKSPACE, 'outputs/content-kalender/2026-06-captions-v2.md'),
    'utf8'
  );
  const sections = md.split(/\n##\s/).slice(1);
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
  if (!res.ok) throw new Error(`Upload failed: ${res.status} ${await res.text()}`);
  const data = await res.json();
  return data.url;
}

console.log(`[POST] ${POST.slug} → ${POST.date}`);
const caption = await loadCaption(POST.section);

const mediaUrls = [];
for (const png of POST.pngs) {
  const ghUrl = `${GH_RAW_BASE}/outputs/${POST.folder}/${POST.slug}/png/${png}`;
  const blotatoUrl = await uploadMedia(ghUrl);
  mediaUrls.push(blotatoUrl);
  await new Promise(r => setTimeout(r, 1500));
}

const body = {
  post: {
    accountId: ACCOUNT_ID,
    content: { text: caption, mediaUrls, platform: 'instagram' },
    target: { targetType: 'instagram' },
  },
  scheduledTime: POST.date,
};
const res = await fetch(`${BLOTATO_BASE}/v2/posts`, {
  method: 'POST', headers: HEADERS, body: JSON.stringify(body),
});
if (!res.ok) {
  console.error(`✗ FAIL: ${res.status} ${await res.text()}`);
  process.exit(1);
}
const data = await res.json();
console.log(`\n✓ NEW Submission: ${data.postSubmissionId || data.id || JSON.stringify(data)}`);
