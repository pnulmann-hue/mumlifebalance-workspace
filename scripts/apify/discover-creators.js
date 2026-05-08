#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..', '..');
const KEYWORDS_PATH = path.join(REPO_ROOT, 'context', 'discovery-keywords.json');
const OUTPUT_DIR = path.join(REPO_ROOT, 'outputs', 'apify-runs');

const HASHTAG_ACTOR = 'apify~instagram-hashtag-scraper';
const PROFILE_ACTOR = 'apify~instagram-profile-scraper';
const ACTOR_TIMEOUT_SEC = 240;

const token = process.env.APIFY_API_TOKEN;
if (!token) {
  console.error('APIFY_API_TOKEN env var is required');
  process.exit(1);
}

const REQUESTED_NICHE = (process.env.INPUT_NICHE || 'both').toLowerCase();

async function callActor(actorId, input) {
  const url = `https://api.apify.com/v2/acts/${actorId}/run-sync-get-dataset-items?token=${token}&timeout=${ACTOR_TIMEOUT_SEC}`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input)
  });
  if (!response.ok) {
    throw new Error(`${actorId} HTTP ${response.status}: ${(await response.text()).slice(0, 400)}`);
  }
  return response.json();
}

async function scrapeHashtag(hashtag, postsPerHashtag) {
  return callActor(HASHTAG_ACTOR, {
    hashtags: [hashtag],
    resultsLimit: postsPerHashtag
  });
}

async function scrapeProfiles(handles) {
  if (handles.length === 0) return [];
  return callActor(PROFILE_ACTOR, {
    usernames: handles,
    resultsLimit: 5,
    addParentData: false
  });
}

function aggregateByCreator(allPosts) {
  const map = new Map();
  for (const post of allPosts) {
    const handle = (post.ownerUsername || '').toLowerCase();
    if (!handle) continue;
    if (!map.has(handle)) {
      map.set(handle, {
        handle: post.ownerUsername,
        fullName: post.ownerFullName || '',
        posts: [],
        totalLikes: 0,
        totalComments: 0,
        hashtags: new Set()
      });
    }
    const entry = map.get(handle);
    entry.posts.push({
      url: post.url,
      caption: post.caption,
      likes: post.likesCount || 0,
      comments: post.commentsCount || 0,
      type: post.type || post.productType,
      timestamp: post.timestamp,
      hashtag: post._sourceHashtag
    });
    entry.totalLikes += post.likesCount || 0;
    entry.totalComments += post.commentsCount || 0;
    entry.hashtags.add(post._sourceHashtag);
  }
  return [...map.values()];
}

function rankCreators(creators, settings) {
  return creators
    .filter(c => c.posts.length >= settings.min_appearances_to_qualify)
    .filter(c => c.totalLikes >= settings.min_total_likes_to_qualify)
    .map(c => ({
      ...c,
      hashtagCount: c.hashtags.size,
      score: c.hashtags.size * 1000 + c.totalLikes
    }))
    .sort((a, b) => b.score - a.score);
}

function generateReport(niche, nicheConfig, ranked, profilesByHandle, settings) {
  const date = new Date().toISOString().slice(0, 10);
  const top = ranked.slice(0, settings.top_n_in_report);

  let md = `# Discovery — ${nicheConfig.label}\n\n`;
  md += `**Datum:** ${date}\n`;
  md += `**Hashtags gescrapt:** ${nicheConfig.hashtags.length} (${nicheConfig.hashtags.map(h => '#' + h).join(', ')})\n`;
  md += `**Posts pro Hashtag:** ${settings.posts_per_hashtag}\n`;
  md += `**Unique Creators gefunden:** ${ranked.length}\n`;
  md += `**Top angereichert:** ${Math.min(settings.top_n_to_enrich, ranked.length)}\n`;
  md += `**Im Report gezeigt:** ${top.length}\n\n`;
  md += `Ranking-Score: \`hashtag-Erscheinungen × 1000 + Total-Likes\` — bevorzugt Creator, die unter mehreren relevanten Hashtags performen.\n\n---\n\n`;

  top.forEach((c, idx) => {
    const profile = profilesByHandle[c.handle.toLowerCase()];
    md += `## ${idx + 1}. ${c.fullName || c.handle} · @${c.handle}\n\n`;
    if (profile) {
      const followers = profile.followersCount?.toLocaleString('de-CH') ?? '?';
      const posts = profile.postsCount?.toLocaleString('de-CH') ?? '?';
      md += `- **Follower:** ${followers}\n`;
      md += `- **Posts gesamt:** ${posts}\n`;
      if (profile.biography) md += `- **Bio:** ${profile.biography.replace(/\n/g, ' / ').slice(0, 240)}\n`;
      if (profile.externalUrl) md += `- **Link:** ${profile.externalUrl}\n`;
    } else {
      md += `- **Profil-Daten:** _nicht angereichert (außerhalb Top-${settings.top_n_to_enrich})_\n`;
    }
    md += `- **Erscheint unter:** ${c.hashtagCount} Hashtag${c.hashtagCount === 1 ? '' : 's'} (${[...c.hashtags].map(h => '#' + h).join(', ')})\n`;
    md += `- **Engagement gesamt:** ${c.totalLikes.toLocaleString('de-CH')} Likes · ${c.totalComments.toLocaleString('de-CH')} Kommentare über ${c.posts.length} Post${c.posts.length === 1 ? '' : 's'}\n`;
    md += `- **Avg pro Post:** ${Math.round(c.totalLikes / c.posts.length).toLocaleString('de-CH')} Likes\n`;
    md += `- **Profil:** https://instagram.com/${c.handle}\n\n`;

    const topPosts = [...c.posts].sort((a, b) => b.likes - a.likes).slice(0, 3);
    if (topPosts.length > 0) {
      md += `**Top Posts unter Watchlist-Hashtags:**\n`;
      for (const p of topPosts) {
        md += `- ${p.likes.toLocaleString('de-CH')} L · ${p.comments.toLocaleString('de-CH')} K · ${p.type || 'Post'}`;
        if (p.timestamp) md += ` · ${p.timestamp.slice(0, 10)}`;
        if (p.hashtag) md += ` · #${p.hashtag}`;
        md += `\n`;
        if (p.caption) {
          const firstLine = p.caption.split('\n')[0].slice(0, 200);
          md += `  > "${firstLine}${p.caption.length > 200 ? '…' : ''}"\n`;
        }
        if (p.url) md += `  ${p.url}\n`;
      }
      md += `\n`;
    }
    md += `---\n\n`;
  });

  return md;
}

async function discoverNiche(nicheKey, nicheConfig, settings) {
  console.log(`\n=== ${nicheConfig.label} ===`);
  const allPosts = [];
  for (const hashtag of nicheConfig.hashtags) {
    try {
      console.log(`  → #${hashtag}`);
      const posts = await scrapeHashtag(hashtag, settings.posts_per_hashtag);
      for (const p of posts) p._sourceHashtag = hashtag;
      allPosts.push(...posts);
    } catch (err) {
      console.error(`  ✗ #${hashtag}: ${err.message}`);
    }
  }
  console.log(`  → ${allPosts.length} posts collected, aggregating…`);

  const creators = aggregateByCreator(allPosts);
  const ranked = rankCreators(creators, settings);
  console.log(`  → ${ranked.length} unique creators after filter`);

  const handlesToEnrich = ranked
    .slice(0, settings.top_n_to_enrich)
    .map(c => c.handle);

  let profilesByHandle = {};
  if (handlesToEnrich.length > 0) {
    console.log(`  → enriching ${handlesToEnrich.length} top profiles`);
    try {
      const profiles = await scrapeProfiles(handlesToEnrich);
      for (const p of profiles) {
        const h = (p.username || '').toLowerCase();
        if (h) profilesByHandle[h] = p;
      }
    } catch (err) {
      console.error(`  ✗ profile enrichment failed: ${err.message}`);
    }
  }

  const md = generateReport(nicheKey, nicheConfig, ranked, profilesByHandle, settings);
  const date = new Date().toISOString().slice(0, 10);
  await fs.mkdir(OUTPUT_DIR, { recursive: true });
  const mdPath = path.join(OUTPUT_DIR, `discovery-${date}-${nicheKey}.md`);
  const jsonPath = path.join(OUTPUT_DIR, `discovery-${date}-${nicheKey}.json`);
  await fs.writeFile(mdPath, md);
  await fs.writeFile(
    jsonPath,
    JSON.stringify(
      {
        date,
        niche: nicheKey,
        config: nicheConfig,
        settings,
        ranked: ranked.map(c => ({ ...c, hashtags: [...c.hashtags] })),
        profiles: profilesByHandle
      },
      null,
      2
    )
  );

  console.log(`  ✓ ${path.relative(REPO_ROOT, mdPath)}`);
  console.log(`  ✓ ${path.relative(REPO_ROOT, jsonPath)}`);
}

async function main() {
  const config = JSON.parse(await fs.readFile(KEYWORDS_PATH, 'utf8'));
  const settings = config.settings;

  const niches =
    REQUESTED_NICHE === 'both'
      ? Object.keys(config.niches)
      : [REQUESTED_NICHE];

  for (const nicheKey of niches) {
    const nicheConfig = config.niches[nicheKey];
    if (!nicheConfig) {
      console.error(`Unknown niche: ${nicheKey}. Available: ${Object.keys(config.niches).join(', ')}`);
      process.exit(1);
    }
    await discoverNiche(nicheKey, nicheConfig, settings);
  }

  console.log('\nDone.');
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
