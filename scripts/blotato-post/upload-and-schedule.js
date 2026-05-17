/**
 * Upload-and-Schedule — One-Shot-Skript für KW 19
 *
 * Nimmt einen lokalen Ordner mit slide-01.png..slide-10.png + ein Config-JSON,
 * lädt alle PNGs zur WordPress Media Library hoch, ersetzt mediaUrls in der Config
 * mit den public WP-URLs, und ruft dann schedule-post.js auf.
 *
 * Nutzung:
 *   node upload-and-schedule.js \
 *     --slides-dir="../../outputs/karussells/render-2026-05-04/doterra-monatsfokus-hausarzt-wendepunkt" \
 *     --config="post-configs/2026-05-06-mi-doterra-d2-hausarzt.json"
 *
 * Voraussetzungen:
 *   - .env im Workspace-Root mit BLOTATO_API_KEY
 *   - scripts/wordpress/.env mit WP_URL + WP_USER + WP_APP_PASSWORD
 *   - Wird LOCAL ausgeführt (nicht in Web-Sandbox — die blockiert mumlifebalance.ch)
 */

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import { uploadMedia } from '../wordpress/wp-api.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const args = Object.fromEntries(
  process.argv.slice(2).map(a => {
    const [k, ...rest] = a.replace(/^--/, '').split('=');
    return [k, rest.join('=') || true];
  })
);

if (!args['slides-dir'] || !args.config) {
  console.error('FEHLER: --slides-dir=<pfad> und --config=<pfad> sind Pflicht');
  process.exit(1);
}

const slidesDir = path.resolve(args['slides-dir']);
const configPath = path.resolve(args.config);

// Slide-PNGs einlesen (slide-01.png ... slide-10.png)
const files = await fs.readdir(slidesDir);
const slideFiles = files
  .filter(f => /^slide-\d{2}\.png$/.test(f))
  .sort();

if (slideFiles.length === 0) {
  console.error(`FEHLER: keine slide-XX.png in ${slidesDir} gefunden`);
  process.exit(1);
}

console.log(`Slides gefunden: ${slideFiles.length} in ${slidesDir}`);

// Config lesen
const config = JSON.parse(await fs.readFile(configPath, 'utf-8'));
console.log(`Config: ${path.basename(configPath)} | ScheduledTime: ${config.scheduledTime}`);
console.log('');

// Alle PNGs zu WordPress Media-Library hochladen
console.log('--- Step 1: Upload zu WordPress Media-Library ---');
const wpUrls = [];
const slugBase = path.basename(slidesDir);
for (let i = 0; i < slideFiles.length; i++) {
  const file = slideFiles[i];
  const filePath = path.join(slidesDir, file);
  const title = `${slugBase}-${file.replace('.png', '')}`;
  try {
    const media = await uploadMedia(filePath, { title });
    wpUrls.push(media.source_url);
    console.log(`  [${i + 1}/${slideFiles.length}] ${file} → ${media.source_url.slice(0, 80)}...`);
  } catch (err) {
    console.error(`  [${i + 1}/${slideFiles.length}] FEHLER bei ${file}: ${err.message}`);
    process.exit(1);
  }
}

// mediaUrls in Config schreiben
config.mediaUrls = wpUrls;
await fs.writeFile(configPath, JSON.stringify(config, null, 2) + '\n', 'utf-8');
console.log(`\nConfig aktualisiert: ${configPath}`);

// Schedule-Post-Skript aufrufen
console.log('\n--- Step 2: Blotato Schedule (POST /v2/posts) ---');
const scheduleScript = path.join(__dirname, 'schedule-post.js');
await new Promise((resolve, reject) => {
  const child = spawn('node', [scheduleScript, `--config=${configPath}`], {
    stdio: 'inherit',
    cwd: __dirname,
  });
  child.on('close', code => {
    if (code === 0) resolve();
    else reject(new Error(`schedule-post.js exit code ${code}`));
  });
});

console.log('\nFERTIG.');
