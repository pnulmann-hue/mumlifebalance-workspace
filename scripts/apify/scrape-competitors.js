#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..', '..');
const WATCHLIST_PATH = path.join(REPO_ROOT, 'context', 'competitor-watchlist.json');
const OUTPUT_DIR = path.join(REPO_ROOT, 'outputs', 'apify-runs');

const APIFY_ACTOR = 'apify~instagram-profile-scraper';
const APIFY_ENDPOINT = `https://api.apify.com/v2/acts/${APIFY_ACTOR}/run-sync-get-dataset-items`;
const ACTOR_TIMEOUT_SEC = 180;

const token = process.env.APIFY_API_TOKEN;
if (!token) {
  console.error('APIFY_API_TOKEN env var is required');
  process.exit(1);
}

async function loadWatchlist() {
  const raw = await fs.readFile(WATCHLIST_PATH, 'utf8');
  return JSON.parse(raw);
}

async function scrapeBatch(handles) {
  const url = `${APIFY_ENDPOINT}?token=${token}&timeout=${ACTOR_TIMEOUT_SEC}`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      usernames: handles,
      resultsLimit: 25,
      addParentData: false
    })
  });
  if (!response.ok) {
    throw new Error(`Apify HTTP ${response.status}: ${await response.text()}`);
  }
  return response.json();
}

function indexByHandle(items) {
  const out = {};
  for (const item of items) {
    const handle = item.username || item.ownerUsername;
    if (!handle) continue;
    out[handle.toLowerCase()] = item;
  }
  return out;
}

function generateSummary(date, accounts, byHandle) {
  let md = `# Konkurrenz-Scrape — ${date}\n\n`;
  md += `Auto-generiert via \`scripts/apify/scrape-competitors.js\` (Actor: ${APIFY_ACTOR}).\n\n`;

  for (const account of accounts) {
    const profile = byHandle[account.handle.toLowerCase()];
    md += `## ${account.label} (@${account.handle}) — ${account.profile}\n\n`;

    if (!profile) {
      md += `_Keine Daten erhalten._\n\n`;
      continue;
    }

    md += `- **Followers:** ${(profile.followersCount ?? '?').toLocaleString?.('de-CH') ?? profile.followersCount}\n`;
    md += `- **Following:** ${(profile.followsCount ?? '?').toLocaleString?.('de-CH') ?? profile.followsCount}\n`;
    md += `- **Posts gesamt:** ${(profile.postsCount ?? '?').toLocaleString?.('de-CH') ?? profile.postsCount}\n`;
    if (profile.fullName) md += `- **Name:** ${profile.fullName}\n`;
    if (profile.biography) md += `- **Bio:** ${profile.biography.replace(/\n/g, ' / ')}\n`;
    if (profile.externalUrl) md += `- **Link:** ${profile.externalUrl}\n`;
    md += `\n`;

    const posts = profile.latestPosts || [];
    if (posts.length === 0) {
      md += `_Keine Posts im Sample._\n\n`;
      continue;
    }

    const sorted = [...posts].sort((a, b) => (b.likesCount ?? 0) - (a.likesCount ?? 0));
    md += `### Top 5 Posts (nach Likes)\n\n`;
    for (const p of sorted.slice(0, 5)) {
      const likes = p.likesCount?.toLocaleString('de-CH') ?? '?';
      const comments = p.commentsCount?.toLocaleString('de-CH') ?? '?';
      const type = p.type || p.productType || 'Post';
      md += `- **${likes} Likes · ${comments} Kommentare** · ${type}`;
      if (p.timestamp) md += ` · ${p.timestamp.slice(0, 10)}`;
      md += `\n`;
      if (p.caption) {
        const firstLine = p.caption.split('\n')[0].slice(0, 240);
        md += `  > "${firstLine}${p.caption.length > 240 ? '…' : ''}"\n`;
      }
      if (p.url) md += `  ${p.url}\n`;
    }
    md += `\n`;
  }

  return md;
}

async function main() {
  const watchlist = await loadWatchlist();

  const override = process.env.INPUT_HANDLES?.trim();
  const handles = override
    ? override.split(',').map(h => h.trim().replace(/^@/, '')).filter(Boolean)
    : watchlist.accounts.map(a => a.handle);

  console.log(`Scraping ${handles.length} accounts: ${handles.join(', ')}`);

  let items;
  try {
    items = await scrapeBatch(handles);
  } catch (err) {
    console.error(`Apify error: ${err.message}`);
    process.exit(1);
  }

  const byHandle = indexByHandle(items);
  const date = new Date().toISOString().slice(0, 10);
  await fs.mkdir(OUTPUT_DIR, { recursive: true });

  const accountsForSummary = override
    ? handles.map(h => ({ handle: h, label: h, profile: 'ad-hoc' }))
    : watchlist.accounts;

  const jsonPath = path.join(OUTPUT_DIR, `competitors-${date}.json`);
  await fs.writeFile(
    jsonPath,
    JSON.stringify({ date, scraped: handles, results: items }, null, 2)
  );

  const mdPath = path.join(OUTPUT_DIR, `competitors-${date}.md`);
  await fs.writeFile(mdPath, generateSummary(date, accountsForSummary, byHandle));

  const got = Object.keys(byHandle);
  const missing = handles.filter(h => !got.includes(h.toLowerCase()));
  console.log(`✓ ${got.length}/${handles.length} accounts scraped`);
  if (missing.length > 0) console.log(`  Missing: ${missing.join(', ')}`);
  console.log(`  JSON: ${path.relative(REPO_ROOT, jsonPath)}`);
  console.log(`  MD:   ${path.relative(REPO_ROOT, mdPath)}`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
