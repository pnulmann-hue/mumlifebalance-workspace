/**
 * Blotato Schedule Post — schedulet einen Instagram-Post
 *
 * NEU seit 2026-04-23: Media werden zuerst via POST /v2/media auf Blotato
 * hochgeladen (fetch-and-host). Damit sind abgelaufene Canva-Presigned-URLs
 * kein Problem mehr — Blotato hält die Bilder permanent.
 *
 * Nutzung:
 *   node schedule-post.js --config=<pfad-zum-json>
 *   node schedule-post.js --config=<pfad-zum-json> --skip-upload   # wenn mediaUrls schon Blotato-gehostet sind
 *
 * Config-JSON-Struktur:
 * {
 *   "accountId": "41414",
 *   "text": "Caption inkl. Hashtags",
 *   "mediaUrls": ["url1.jpg", "url2.jpg", ...],
 *   "scheduledTime": "2026-04-22T20:30:00+02:00",
 *   "platform": "instagram",
 *   "mediaType": "image"
 * }
 */

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WORKSPACE_ROOT = path.resolve(__dirname, '..', '..');

const BLOTATO_BASE = 'https://backend.blotato.com';

// --- Args parsen ---
const args = Object.fromEntries(
  process.argv.slice(2).map(a => {
    const [k, ...rest] = a.replace(/^--/, '').split('=');
    return [k, rest.join('=') || true];
  })
);

if (!args.config) {
  console.error('FEHLER: --config=<pfad-zum-json> fehlt');
  process.exit(1);
}

// --- .env laden ---
const envPath = path.join(WORKSPACE_ROOT, '.env');
const envContent = await fs.readFile(envPath, 'utf8');
const envMap = Object.fromEntries(
  envContent
    .split('\n')
    .filter(line => line.includes('=') && !line.startsWith('#'))
    .map(line => {
      const [k, ...rest] = line.split('=');
      return [k.trim(), rest.join('=').trim().replace(/^["']|["']$/g, '')];
    })
);

const BLOTATO_API_KEY = envMap.BLOTATO_API_KEY;
if (!BLOTATO_API_KEY) {
  console.error('FEHLER: BLOTATO_API_KEY nicht in .env gefunden');
  process.exit(1);
}

// --- Config-JSON laden ---
const configPath = path.resolve(args.config);
const config = JSON.parse(await fs.readFile(configPath, 'utf8'));

console.log('Blotato Post Scheduling');
console.log(`  Config-Datei:   ${configPath}`);
console.log(`  Account:        ${config.accountId}`);
console.log(`  Media-Anzahl:   ${config.mediaUrls.length}`);
console.log(`  Scheduled Time: ${config.scheduledTime}`);
console.log(`  Platform:       ${config.platform}`);
console.log(`  Media Type:     ${config.mediaType}`);
console.log(`  Caption Länge:  ${config.text.length} Zeichen`);
console.log('');

// --- Step 1: Media auf Blotato hochladen (falls noetig) ---
const HEADERS = {
  'Content-Type': 'application/json',
  'blotato-api-key': BLOTATO_API_KEY,
};

function isBlotatoHosted(url) {
  return url.includes('blotato.com') || url.includes('database.blotato.com');
}

async function uploadMediaUrl(sourceUrl, index) {
  const response = await fetch(`${BLOTATO_BASE}/v2/media`, {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify({ url: sourceUrl }),
  });
  const text = await response.text();
  let json;
  try { json = JSON.parse(text); } catch { json = { raw: text }; }

  if (!response.ok) {
    throw new Error(`Media-Upload #${index + 1} fehlgeschlagen (HTTP ${response.status}): ${text}`);
  }

  // Response-Format laut Blotato-Doku: { "url": "https://database.blotato.com/...", "id": "..." }
  const hostedUrl = json.url || json.mediaUrl || json.publicUrl;
  if (!hostedUrl) {
    throw new Error(`Media-Upload #${index + 1}: keine URL im Response: ${JSON.stringify(json)}`);
  }
  return hostedUrl;
}

let finalMediaUrls;
if (args['skip-upload']) {
  console.log('⏭  --skip-upload gesetzt — Media-URLs werden direkt verwendet.');
  finalMediaUrls = config.mediaUrls;
} else {
  console.log(`Lade ${config.mediaUrls.length} Medien auf Blotato hoch (POST /v2/media) ...`);
  finalMediaUrls = [];
  for (let i = 0; i < config.mediaUrls.length; i++) {
    const sourceUrl = config.mediaUrls[i];
    if (isBlotatoHosted(sourceUrl)) {
      console.log(`  [${i + 1}/${config.mediaUrls.length}] bereits Blotato-gehostet, \u00fcberspringe Upload`);
      finalMediaUrls.push(sourceUrl);
      continue;
    }
    try {
      const hostedUrl = await uploadMediaUrl(sourceUrl, i);
      finalMediaUrls.push(hostedUrl);
      console.log(`  [${i + 1}/${config.mediaUrls.length}] \u2705 ${hostedUrl.slice(0, 70)}...`);
    } catch (err) {
      console.error(`  [${i + 1}/${config.mediaUrls.length}] \u274c ${err.message}`);
      process.exit(1);
    }
  }
  console.log(`\n\u2705 Alle ${finalMediaUrls.length} Medien hochgeladen.\n`);
}

// --- Step 2: Post schedulen ---
// mediaType nur setzen bei "reel" oder "story" (Karussell/Feed-Post laesst mediaType weg)
const target = {
  targetType: config.platform,
};
if (config.mediaType === 'reel' || config.mediaType === 'story') {
  target.mediaType = config.mediaType;
}

const body = {
  post: {
    accountId: config.accountId,
    content: {
      text: config.text,
      mediaUrls: finalMediaUrls,
      platform: config.platform,
    },
    target,
  },
  scheduledTime: config.scheduledTime,
};

console.log('Sende POST /v2/posts ...');
const response = await fetch(`${BLOTATO_BASE}/v2/posts`, {
  method: 'POST',
  headers: HEADERS,
  body: JSON.stringify(body),
});

const responseText = await response.text();
let responseJson;
try {
  responseJson = JSON.parse(responseText);
} catch {
  responseJson = { raw: responseText };
}

console.log(`HTTP-Status: ${response.status}`);
console.log('Response:');
console.log(JSON.stringify(responseJson, null, 2));

if (!response.ok) {
  console.error('\nFEHLER beim Scheduling — Response war nicht 2xx.');
  process.exit(1);
}

console.log('\n\u2705 Post erfolgreich gescheduled.');
if (responseJson.post && responseJson.post.id) {
  console.log(`Post-ID: ${responseJson.post.id}`);
}

// --- Step 3: Blotato-gehostete URLs zurueck in die Config schreiben ---
// Damit Re-Runs und Referenzen die permanenten URLs haben.
if (!args['skip-upload']) {
  const updatedConfig = { ...config, mediaUrls: finalMediaUrls };
  await fs.writeFile(configPath, JSON.stringify(updatedConfig, null, 2) + '\n', 'utf8');
  console.log(`\n\ud83d\udcbe Config aktualisiert mit Blotato-URLs: ${configPath}`);
}
