/**
 * Deploy Instagram-Starterguide Landingpage zu WordPress
 * Ziel: https://mumlifebalance.ch/instagram-starterguide  (als DRAFT)
 *
 * Run:  cd scripts/wordpress && node --env-file=.env deploy-starterguide.js
 *
 * ⚠️  VOR DEM DEPLOY: In outputs/funnels/0-euro-starterguide/landing/index.html
 *     die AC-Form-Platzhalter ersetzen (STARTERGUIDE_AC_FORM_ID / STARTERGUIDE_AC_TOKEN).
 *     Solange Platzhalter drin sind, warnt das Script und bricht ab.
 */

import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HTML_PATH = resolve(__dirname, '../../outputs/funnels/0-euro-starterguide/landing/index.html');
const SLUG = 'instagram-starterguide';
const PAGE_TITLE = '0€ Instagram-Starterguide';

const WP_URL = process.env.WP_URL;
const WP_USER = process.env.WP_USER;
const WP_APP_PASSWORD = process.env.WP_APP_PASSWORD;

if (!WP_URL || !WP_USER || !WP_APP_PASSWORD) {
  console.error('❌ Fehlende ENV (WP_URL / WP_USER / WP_APP_PASSWORD). .env anlegen.');
  process.exit(1);
}

const authHeader = 'Basic ' + Buffer.from(`${WP_USER}:${WP_APP_PASSWORD}`).toString('base64');

async function wpRequest(path, options = {}) {
  const url = `${WP_URL}/wp-json${path}`;
  const headers = { 'Authorization': authHeader, 'Content-Type': 'application/json', ...options.headers };
  const res = await fetch(url, { ...options, headers });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`WP ${res.status}: ${text.slice(0, 400)}`);
  }
  return res.json();
}

async function findPageBySlug(slug) {
  const results = await wpRequest(`/wp/v2/pages?slug=${slug}&status=any&per_page=1`);
  return results[0] || null;
}

async function main() {
  console.log('📖 Lese Starterguide-Landing HTML...');
  let html = await readFile(HTML_PATH, 'utf-8');

  if (html.includes('STARTERGUIDE_AC_FORM_ID') || html.includes('STARTERGUIDE_AC_TOKEN')) {
    console.error('\n⚠️  AC-Formular-Platzhalter noch nicht ersetzt!');
    console.error('   Lege in ActiveCampaign ein Formular für den Starterguide an');
    console.error('   und ersetze STARTERGUIDE_AC_FORM_ID + STARTERGUIDE_AC_TOKEN in der index.html.');
    console.error('   (Zum reinen Layout-Test diese Prüfung temporär auskommentieren.)\n');
    process.exit(1);
  }

  // Style + Body extrahieren (Gutenberg wp:html-Block) — analog deploy-bio-v3.js
  const styleMatch = html.match(/<style>([\s\S]*?)<\/style>/);
  const styleBlock = styleMatch ? `<style>${styleMatch[1]}</style>` : '';
  const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/);
  const body = bodyMatch[1];

  const wpContent = `<!-- wp:html -->\n${styleBlock}\n${body}\n<!-- /wp:html -->`;
  console.log(`📦 Payload: ${wpContent.length} Zeichen`);

  const existing = await findPageBySlug(SLUG);
  const body_data = {
    title: PAGE_TITLE,
    slug: SLUG,
    content: wpContent,
    status: 'draft',   // IMMER Draft — Patricia prüft & publiziert selbst
  };

  let result;
  if (existing) {
    console.log(`🔄 Update Seite ID ${existing.id}...`);
    result = await wpRequest(`/wp/v2/pages/${existing.id}`, { method: 'POST', body: JSON.stringify(body_data) });
  } else {
    console.log('🚀 Erstelle neue Seite...');
    result = await wpRequest('/wp/v2/pages', { method: 'POST', body: JSON.stringify(body_data) });
  }

  console.log(`\n✅ ${existing ? 'AKTUALISIERT' : 'ERSTELLT'} (Status: ${result.status})`);
  console.log(`   ID:       ${result.id}`);
  console.log(`   Preview:  ${result.link}`);
  console.log(`   Live-URL: https://mumlifebalance.ch/${SLUG}  (sobald publiziert)`);
  console.log(`\n👉 Danach: Bio-Link „Starterguide" auf diese URL zeigen lassen.`);
}

main().catch((err) => {
  console.error('\n❌ FEHLER:', err.message);
  process.exit(1);
});
