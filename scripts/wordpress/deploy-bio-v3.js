/**
 * Deploy Bio V3 zu WordPress (mumlifebalance.ch/bio)
 * Run: node --env-file=.env deploy-bio-v3.js
 */

import { readFile } from 'node:fs/promises';

const WP_URL = process.env.WP_URL;
const WP_USER = process.env.WP_USER;
const WP_APP_PASSWORD = process.env.WP_APP_PASSWORD;

if (!WP_URL || !WP_USER || !WP_APP_PASSWORD) {
  console.error('❌ Fehlende ENV');
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
  const HTML_PATH = 'C:/Users/pnulm/Desktop/Mein Business/.claude/worktrees/upbeat-yalow-d35cfb/outputs/link-in-bio/index.html';
  const FOTO_URL = 'https://mumlifebalance.ch/wp-content/uploads/2026/05/patricia-scaled.jpg';

  console.log('📖 Lese Bio V3 HTML...');
  let html = await readFile(HTML_PATH, 'utf-8');
  html = html.replace(/src="patricia\.jpg"/g, `src="${FOTO_URL}"`);

  const styleMatch = html.match(/<style>([\s\S]*?)<\/style>/);
  const styleBlock = `<style>${styleMatch[1]}</style>`;
  const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/);
  const body = bodyMatch[1];

  // Google Fonts werden vom WP-Theme bereits geladen (Philosopher ist Standard
  // im Brand) — wir verzichten auf eigenen Import um WAF-Trigger zu vermeiden.
  const wpContent = `<!-- wp:html -->\n${styleBlock}\n${body}\n<!-- /wp:html -->`;
  console.log(`📦 Payload: ${wpContent.length} Zeichen`);

  const existing = await findPageBySlug('bio');
  const body_data = {
    title: '',  // Kein Titel oben — Avatar + Name kommen aus dem HTML-Block selbst
    slug: 'bio',
    content: wpContent,
    status: 'draft',
  };

  let result;
  if (existing) {
    console.log(`🔄 Update Seite ID ${existing.id}...`);
    result = await wpRequest(`/wp/v2/pages/${existing.id}`, { method: 'POST', body: JSON.stringify(body_data) });
  } else {
    console.log('🚀 Erstelle neue Seite...');
    result = await wpRequest('/wp/v2/pages', { method: 'POST', body: JSON.stringify(body_data) });
  }

  console.log(`\n✅ ${existing ? 'AKTUALISIERT' : 'ERSTELLT'}`);
  console.log(`   ID:       ${result.id}`);
  console.log(`   Status:   ${result.status}`);
  console.log(`   Preview:  ${result.link}`);
  console.log(`   Live-URL: https://mumlifebalance.ch/bio (sobald publiziert)`);
}

main().catch((err) => {
  console.error('\n❌ FEHLER:', err.message);
  process.exit(1);
});
