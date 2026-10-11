#!/usr/bin/env node
/**
 * Legt den Pfeiler-Blogartikel „Instagram für Network Marketing" als Elementor-Beitrag an.
 *
 * Baut dieselbe Struktur wie das Beispiel (Post 4047):
 *   Container → HTML-Widget mit dem gesamten Artikel-Markup
 * ABER: Der <style>-Block liegt in einem ZWEITEN Widget am Ende statt am Anfang,
 * damit Rank Math das Keyword im ersten Zehntel des Inhalts findet.
 *
 * Nutzung:
 *   node --env-file=scripts/wordpress/.env scripts/wordpress/deploy-blog-instagram-strategie.mjs
 */

import fs from 'node:fs';
import path from 'node:path';

const WP = process.env.WP_URL?.replace(/\/$/, '');
const AUTH = 'Basic ' + Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString('base64');

const SCRATCH = process.argv[2];
if (!SCRATCH) {
  console.error('Bitte Pfad zum Scratchpad-Ordner als Argument übergeben.');
  process.exit(1);
}

const body = fs.readFileSync(path.join(SCRATCH, 'body-instagram-strategie.html'), 'utf8');
const MIT_CSS = process.argv.includes('--mit-css');
const style = MIT_CSS ? fs.readFileSync(path.join(SCRATCH, 'style-block.html'), 'utf8') : '';

const TITLE = 'Instagram für Network Marketing: die Strategie, die auch mit vier Kindern funktioniert';
const SLUG = 'instagram-network-marketing-strategie';
const EXCERPT = 'Instagram für Network Marketing ohne Namensliste und ohne täglich Produktbilder: die 6 Schritte, die auch neben Familie und Job funktionieren.';

async function wp(route, options = {}) {
  const res = await fetch(`${WP}/wp-json/wp/v2/${route}`, {
    ...options,
    headers: { Authorization: AUTH, 'Content-Type': 'application/json', ...(options.headers || {}) },
  });
  const text = await res.text();
  let data;
  try { data = JSON.parse(text); } catch { data = { raw: text.slice(0, 400) }; }
  return { status: res.status, ok: res.ok, data };
}

// 1) Kategorie sicherstellen
async function ensureCategory(name, slug) {
  const found = await wp(`categories?slug=${slug}`);
  if (found.ok && Array.isArray(found.data) && found.data.length) {
    console.log(`Kategorie existiert bereits: [${found.data[0].id}] ${found.data[0].name}`);
    return found.data[0].id;
  }
  const created = await wp('categories', { method: 'POST', body: JSON.stringify({ name, slug }) });
  if (!created.ok) {
    console.error('Kategorie konnte nicht angelegt werden:', created.status, created.data);
    return null;
  }
  console.log(`Kategorie angelegt: [${created.data.id}] ${created.data.name}`);
  return created.data.id;
}

// 2) Elementor-Struktur bauen — Artikel zuerst, Style am Ende
function elementorData() {
  const id = () => Math.random().toString(16).slice(2, 9);
  const container = (html) => ({
    id: id(), elType: 'container', settings: {}, isInner: false,
    elements: [{ id: id(), elType: 'widget', widgetType: 'html', settings: { html }, elements: [] }],
  });
  const teile = [container(body)];
  if (MIT_CSS) teile.push(container(style));
  return JSON.stringify(teile);
}

const run = async () => {
  const catId = await ensureCategory('Instagram & Network Marketing', 'instagram-network-marketing');

  const payload = {
    title: TITLE,
    slug: SLUG,
    status: 'draft',
    excerpt: EXCERPT,
    comment_status: 'closed',
    content: body + '\n' + style,
    ...(catId ? { categories: [catId] } : {}),
    meta: {
      _elementor_edit_mode: 'builder',
      _elementor_template_type: 'wp-post',
      _elementor_data: elementorData(),
    },
  };

  const res = await wp('posts', { method: 'POST', body: JSON.stringify(payload) });
  if (!res.ok) {
    console.error(`\n❌ Fehlgeschlagen (HTTP ${res.status})`);
    console.error(JSON.stringify(res.data).slice(0, 600));
    if (res.status === 403) console.error('\n→ Sieht nach der Imunify360-WAF aus (CSS-dichter POST). Fallback: HTML manuell ins Elementor-HTML-Widget einfügen.');
    process.exit(1);
  }

  console.log(`\n✅ Beitrag angelegt`);
  console.log(`   ID:       ${res.data.id}`);
  console.log(`   Status:   ${res.data.status}`);
  console.log(`   Slug:     ${res.data.slug}`);
  console.log(`   Elementor: ${WP}/wp-admin/post.php?post=${res.data.id}&action=elementor`);
  console.log(`   Klassisch: ${WP}/wp-admin/post.php?post=${res.data.id}&action=edit`);
};

run();
