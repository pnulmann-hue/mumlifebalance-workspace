/**
 * Deploy Bio-Check Landingpage zu WordPress
 *
 * Nutzt WP REST API mit Application Password Auth.
 *
 * Run:
 *   node --env-file=.env deploy-bio-check.js
 *
 * Was es macht:
 *   1. Lädt patricia-hero.jpg zu WP Media hoch (falls noch nicht da)
 *   2. Ersetzt {{PATRICIA_FOTO_URL}} im HTML-Template
 *   3. Erstellt Seite "Bio-Check für Network-Mamas" mit Slug /bio-check
 *   4. Status: draft (zum sicheren Vorschauen) → später auf publish umstellen
 */

import { readFile } from 'node:fs/promises';
import { basename } from 'node:path';

const WP_URL = process.env.WP_URL;
const WP_USER = process.env.WP_USER;
const WP_APP_PASSWORD = process.env.WP_APP_PASSWORD;

if (!WP_URL || !WP_USER || !WP_APP_PASSWORD) {
  console.error('❌ Fehlende ENV: WP_URL, WP_USER, WP_APP_PASSWORD');
  console.error('   Prüfe scripts/wordpress/.env');
  process.exit(1);
}

const authHeader = 'Basic ' + Buffer.from(`${WP_USER}:${WP_APP_PASSWORD}`).toString('base64');

async function wpRequest(path, options = {}) {
  const url = `${WP_URL}/wp-json${path}`;
  const headers = {
    'Authorization': authHeader,
    'Content-Type': 'application/json',
    ...options.headers,
  };
  const res = await fetch(url, { ...options, headers });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`WP ${res.status} ${url}: ${text.slice(0, 500)}`);
  }
  return res.json();
}

async function uploadMedia(filePath, title = null) {
  const buffer = await readFile(filePath);
  const filename = basename(filePath);

  // Prüfen ob das Bild schon existiert (via Titel-Suche)
  const search = encodeURIComponent(title || filename.replace(/\.[^.]+$/, ''));
  const existing = await wpRequest(`/wp/v2/media?search=${search}&per_page=5`);
  const match = existing.find((m) => m.title?.rendered === (title || filename.replace(/\.[^.]+$/, '')));
  if (match) {
    console.log(`ℹ️  Bild existiert bereits: ${match.source_url}`);
    return match.source_url;
  }

  const url = `${WP_URL}/wp-json/wp/v2/media`;
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': authHeader,
      'Content-Type': 'image/jpeg',
      'Content-Disposition': `attachment; filename="${filename}"`,
    },
    body: buffer,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Upload ${res.status}: ${text.slice(0, 500)}`);
  }
  const media = await res.json();
  console.log(`✅ Foto hochgeladen: ${media.source_url}`);
  return media.source_url;
}

async function findPageBySlug(slug) {
  const results = await wpRequest(`/wp/v2/pages?slug=${slug}&status=any&per_page=1`);
  return results[0] || null;
}

async function createOrUpdatePage({ title, slug, content, status = 'draft', template = '' }) {
  const existing = await findPageBySlug(slug);
  const body = { title, slug, content, status };
  if (template) body.template = template;

  if (existing) {
    console.log(`ℹ️  Seite existiert (ID ${existing.id}) — wird aktualisiert`);
    return wpRequest(`/wp/v2/pages/${existing.id}`, {
      method: 'PUT',
      body: JSON.stringify(body),
    });
  }
  console.log(`📝 Seite wird neu erstellt`);
  return wpRequest('/wp/v2/pages', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

// ============================================================
// Main
// ============================================================

async function main() {
  console.log('🚀 Bio-Check Landingpage Deploy startet...\n');

  // 1. Foto hochladen
  console.log('📸 Schritt 1: Foto zu WP Media hochladen');
  const fotoPath = '../bio-check-bot/public/images/patricia-hero.jpg';
  const fotoUrl = await uploadMedia(fotoPath, 'Patricia Ulmann - Bio Check');

  // 2. HTML-Template laden + Platzhalter ersetzen
  console.log('\n📄 Schritt 2: HTML-Template laden');
  const templatePath = '../../outputs/bio-check-bot/wordpress-embed.html';
  let html = await readFile(templatePath, 'utf-8');
  html = html.replaceAll('{{PATRICIA_FOTO_URL}}', fotoUrl);
  console.log(`✅ Template geladen (${html.length} Zeichen), Foto-URL eingesetzt`);

  // 3. Seite erstellen/updaten
  console.log('\n📝 Schritt 3: WordPress-Seite erstellen/aktualisieren');
  const pageContent = `<!-- wp:html -->\n${html}\n<!-- /wp:html -->`;

  const page = await createOrUpdatePage({
    title: 'Bio-Check für Network-Mamas',
    slug: 'bio-check',
    content: pageContent,
    status: 'draft', // Erst als Entwurf — später auf publish
    template: 'elementor_canvas', // versucht Elementor Canvas, fällt sonst auf default
  });

  console.log('\n✅ Fertig!');
  console.log(`   Seiten-ID: ${page.id}`);
  console.log(`   Status:    ${page.status}`);
  console.log(`   URL:       ${page.link}`);
  console.log(`   Vorschau:  ${page.link}${page.status === 'draft' ? '?preview=true' : ''}`);
  console.log('\n🎯 Nächste Schritte:');
  console.log('   1. URL oben öffnen → checken ob alles passt');
  console.log('   2. Wenn gut: Seite in WP-Admin auf "Veröffentlichen" stellen');
  console.log('   3. In die Hauptnavigation einfügen (optional)');
}

main().catch((err) => {
  console.error('\n❌ FEHLER:', err.message);
  process.exit(1);
});
