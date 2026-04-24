/**
 * WordPress REST API Helper
 * ==========================
 *
 * Generische Funktionen für alle WordPress-Operationen auf mumlifebalance.ch.
 * Credentials kommen aus scripts/wordpress/.env (WP_URL, WP_USER, WP_APP_PASSWORD).
 *
 * Nutzung:
 *   import { createPage, updatePage, uploadMedia, ... } from './wp-api.js';
 *
 * Oder direkt per CLI:
 *   node --env-file=.env wp-api.js <command> [args]
 *
 * Verfügbare Commands:
 *   list-pages [search]              - Alle Seiten auflisten (optional Such-Term)
 *   get-page <id-or-slug>            - Einzelne Seite holen
 *   create-page <title> [slug]       - Neue Seite aus Template erstellen (liest HTML von stdin)
 *   update-page <id> <json>          - Seite updaten (json mit Feldern)
 *   set-status <id> <status>         - Status ändern (publish/draft/private/trash)
 *   delete-page <id>                 - Seite komplett löschen
 *   upload-media <path> [title]      - Foto/Datei hochladen
 *   list-media [search]              - Medien auflisten
 *   list-menus                       - Alle Menüs auflisten (erfordert Core v5.9+)
 *   set-featured-image <id> <mediaId> - Beitragsbild setzen
 */

import { readFile } from 'node:fs/promises';
import { basename } from 'node:path';

const WP_URL = process.env.WP_URL;
const WP_USER = process.env.WP_USER;
const WP_APP_PASSWORD = process.env.WP_APP_PASSWORD;

if (!WP_URL || !WP_USER || !WP_APP_PASSWORD) {
  throw new Error('Fehlende ENV — benötigt WP_URL, WP_USER, WP_APP_PASSWORD in .env');
}

const AUTH_HEADER = 'Basic ' + Buffer.from(`${WP_USER}:${WP_APP_PASSWORD}`).toString('base64');

// ============================================================
// Low-Level: HTTP-Request zu WP-REST-API
// ============================================================

async function wpRequest(path, options = {}) {
  const url = `${WP_URL}/wp-json${path}`;
  const headers = {
    'Authorization': AUTH_HEADER,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    ...options.headers,
  };
  const res = await fetch(url, { ...options, headers });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`WP ${res.status} ${path}: ${text.slice(0, 500)}`);
  }
  if (res.status === 204) return null; // No content
  return res.json();
}

// ============================================================
// SEITEN
// ============================================================

export async function listPages({ search = '', status = 'any', perPage = 100 } = {}) {
  const q = new URLSearchParams({ per_page: String(perPage), status, _fields: 'id,slug,title,status,link,date' });
  if (search) q.set('search', search);
  return wpRequest(`/wp/v2/pages?${q}`);
}

export async function getPage(idOrSlug) {
  if (typeof idOrSlug === 'number' || /^\d+$/.test(idOrSlug)) {
    return wpRequest(`/wp/v2/pages/${idOrSlug}`);
  }
  const results = await wpRequest(`/wp/v2/pages?slug=${encodeURIComponent(idOrSlug)}&status=any&per_page=1`);
  return results[0] || null;
}

export async function findPageBySlug(slug) {
  const results = await wpRequest(`/wp/v2/pages?slug=${encodeURIComponent(slug)}&status=any&per_page=1`);
  return results[0] || null;
}

export async function createPage({ title, slug, content, status = 'draft', template = '', excerpt = '', parent = 0, meta = {} }) {
  const body = { title, slug, content, status, parent };
  if (template) body.template = template;
  if (excerpt) body.excerpt = excerpt;
  if (Object.keys(meta).length) body.meta = meta;
  return wpRequest('/wp/v2/pages', { method: 'POST', body: JSON.stringify(body) });
}

export async function updatePage(id, fields) {
  return wpRequest(`/wp/v2/pages/${id}`, { method: 'PUT', body: JSON.stringify(fields) });
}

export async function setPageStatus(id, status) {
  if (!['publish', 'draft', 'private', 'pending', 'trash'].includes(status)) {
    throw new Error(`Ungültiger Status: ${status}`);
  }
  return updatePage(id, { status });
}

export async function deletePage(id, force = false) {
  const q = force ? '?force=true' : '';
  return wpRequest(`/wp/v2/pages/${id}${q}`, { method: 'DELETE' });
}

export async function createOrUpdatePage(data) {
  if (!data.slug) throw new Error('slug required');
  const existing = await findPageBySlug(data.slug);
  if (existing) return updatePage(existing.id, data);
  return createPage(data);
}

// ============================================================
// BEITRÄGE (Posts)
// ============================================================

export async function listPosts({ search = '', status = 'any', perPage = 20, categories = [] } = {}) {
  const q = new URLSearchParams({ per_page: String(perPage), status });
  if (search) q.set('search', search);
  if (categories.length) q.set('categories', categories.join(','));
  return wpRequest(`/wp/v2/posts?${q}`);
}

export async function createPost({ title, slug, content, status = 'draft', categories = [], tags = [], featuredMediaId = 0 }) {
  const body = { title, slug, content, status };
  if (categories.length) body.categories = categories;
  if (tags.length) body.tags = tags;
  if (featuredMediaId) body.featured_media = featuredMediaId;
  return wpRequest('/wp/v2/posts', { method: 'POST', body: JSON.stringify(body) });
}

export async function updatePost(id, fields) {
  return wpRequest(`/wp/v2/posts/${id}`, { method: 'PUT', body: JSON.stringify(fields) });
}

// ============================================================
// MEDIEN
// ============================================================

export async function uploadMedia(filePath, { title, altText, mimeType } = {}) {
  const buffer = await readFile(filePath);
  const filename = basename(filePath);
  const effectiveTitle = title || filename.replace(/\.[^.]+$/, '');

  // Check Duplikat
  const search = encodeURIComponent(effectiveTitle);
  const existing = await wpRequest(`/wp/v2/media?search=${search}&per_page=5`);
  const match = existing.find((m) => m.title?.rendered === effectiveTitle);
  if (match) return match;

  // Upload
  const guessMime = () => {
    const ext = filename.toLowerCase().split('.').pop();
    const map = {
      jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', gif: 'image/gif',
      webp: 'image/webp', svg: 'image/svg+xml', pdf: 'application/pdf',
      mp4: 'video/mp4', webm: 'video/webm', mp3: 'audio/mpeg',
    };
    return map[ext] || 'application/octet-stream';
  };

  const url = `${WP_URL}/wp-json/wp/v2/media`;
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': AUTH_HEADER,
      'Content-Type': mimeType || guessMime(),
      'Content-Disposition': `attachment; filename="${filename}"`,
    },
    body: buffer,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Media upload ${res.status}: ${text.slice(0, 500)}`);
  }
  const media = await res.json();

  // Optional alt-Text setzen
  if (altText) {
    await wpRequest(`/wp/v2/media/${media.id}`, {
      method: 'PUT',
      body: JSON.stringify({ alt_text: altText, title: effectiveTitle }),
    });
  }
  return media;
}

export async function listMedia({ search = '', perPage = 20 } = {}) {
  const q = new URLSearchParams({ per_page: String(perPage) });
  if (search) q.set('search', search);
  return wpRequest(`/wp/v2/media?${q}`);
}

export async function deleteMedia(id) {
  return wpRequest(`/wp/v2/media/${id}?force=true`, { method: 'DELETE' });
}

// ============================================================
// MENÜS (Core Navigation API ab WP 5.9)
// ============================================================

export async function listMenus() {
  return wpRequest('/wp/v2/menus');
}

export async function listMenuItems(menuId) {
  return wpRequest(`/wp/v2/menu-items?menus=${menuId}&per_page=100`);
}

export async function addMenuItem(menuId, { title, url, parent = 0, menuOrder = 0 }) {
  return wpRequest('/wp/v2/menu-items', {
    method: 'POST',
    body: JSON.stringify({
      menus: menuId,
      title,
      url,
      type: 'custom',
      status: 'publish',
      parent,
      menu_order: menuOrder,
    }),
  });
}

// ============================================================
// BENUTZER
// ============================================================

export async function getMe() {
  return wpRequest('/wp/v2/users/me');
}

// ============================================================
// CLI-Runner (falls direkt ausgeführt)
// ============================================================

const thisFile = new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1');
const executedFile = process.argv[1]?.replace(/\\/g, '/');

if (executedFile && thisFile.endsWith(executedFile.split('/').pop())) {
  const [cmd, ...args] = process.argv.slice(2);
  const run = async () => {
    switch (cmd) {
      case 'list-pages': {
        const pages = await listPages({ search: args[0] || '' });
        pages.forEach((p) => console.log(`[${p.id}] ${p.status.padEnd(8)} ${p.slug.padEnd(30)} ${p.title.rendered}`));
        break;
      }
      case 'get-page': {
        const page = await getPage(args[0]);
        console.log(JSON.stringify(page, null, 2));
        break;
      }
      case 'set-status': {
        const result = await setPageStatus(args[0], args[1]);
        console.log(`✅ Status → ${result.status}`);
        console.log(`   URL:   ${result.link}`);
        break;
      }
      case 'delete-page': {
        await deletePage(args[0], true);
        console.log(`✅ Seite ${args[0]} gelöscht`);
        break;
      }
      case 'upload-media': {
        const m = await uploadMedia(args[0], { title: args[1] });
        console.log(`✅ Upload → ${m.source_url}  (ID ${m.id})`);
        break;
      }
      case 'list-media': {
        const media = await listMedia({ search: args[0] || '' });
        media.forEach((m) => console.log(`[${m.id}] ${m.title.rendered.padEnd(40)} ${m.source_url}`));
        break;
      }
      case 'list-menus': {
        const menus = await listMenus();
        menus.forEach((m) => console.log(`[${m.id}] ${m.name.padEnd(30)} (${m.locations.join(',') || 'ungenutzt'})`));
        break;
      }
      case 'whoami': {
        const me = await getMe();
        console.log(`Eingeloggt als: ${me.name} (ID ${me.id})`);
        console.log(`Capabilities:   ${Object.keys(me.capabilities || {}).filter((k) => me.capabilities[k]).slice(0, 6).join(', ')}...`);
        break;
      }
      default:
        console.error('Unbekannter Command. Verfügbar: list-pages, get-page, set-status, delete-page, upload-media, list-media, list-menus, whoami');
        process.exit(1);
    }
  };
  run().catch((err) => { console.error('❌', err.message); process.exit(1); });
}
