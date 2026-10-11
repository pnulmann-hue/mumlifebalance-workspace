#!/usr/bin/env node
/**
 * Entfernt den <style>-Block (und den davorstehenden HTML-Kommentar) aus einem
 * Elementor-Blogbeitrag — sinnvoll, seit das Artikel-CSS im Customizer liegt.
 *
 * Warum: Rank Math wertet post_content aus. Steht dort erst 9'000 Zeichen CSS,
 * findet Rank Math das Fokus-Keyword nicht im ersten Zehntel und rechnet die
 * Keyword-Dichte über den Gestaltungscode mit.
 *
 * Nutzung:
 *   node --env-file=scripts/wordpress/.env scripts/wordpress/css-aus-beitrag-entfernen.mjs <postId> [--sicherung <ordner>]
 */

import fs from 'node:fs';

const WP = process.env.WP_URL.replace(/\/$/, '');
const AUTH = 'Basic ' + Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString('base64');
const POST = process.argv[2];
const sicherungIdx = process.argv.indexOf('--sicherung');
const SICHERUNG = sicherungIdx !== -1 ? process.argv[sicherungIdx + 1] : null;

if (!POST) { console.error('Bitte Post-ID angeben.'); process.exit(1); }

const api = async (route, options = {}) => {
  const res = await fetch(`${WP}/wp-json/wp/v2/${route}`, {
    ...options,
    headers: { Authorization: AUTH, 'Content-Type': 'application/json', ...(options.headers || {}) },
  });
  const text = await res.text();
  let data; try { data = JSON.parse(text); } catch { data = { raw: text.slice(0, 300) }; }
  return { status: res.status, ok: res.ok, data };
};

/** Entfernt führenden HTML-Kommentar + <style>-Block */
const putzen = (html) => html
  .replace(/^\s*<!--[\s\S]*?-->\s*/, '')
  .replace(/<style>[\s\S]*?<\/style>\s*/g, '')
  .replace(/^\s+/, '');

const run = async () => {
  const vorher = await api(`posts/${POST}?context=edit`);
  if (!vorher.ok) { console.error('Beitrag nicht lesbar:', vorher.status); process.exit(1); }

  if (SICHERUNG) {
    const pfad = `${SICHERUNG}/sicherung-post-${POST}.json`;
    fs.writeFileSync(pfad, JSON.stringify(vorher.data, null, 2), 'utf8');
    console.log(`Sicherung geschrieben: ${pfad}`);
  }

  const daten = JSON.parse(vorher.data.meta._elementor_data);
  let gefunden = 0;
  const durchlaufen = (els) => els.forEach((e) => {
    const s = e.settings || {};
    if (typeof s.html === 'string' && s.html.includes('<style>')) {
      const alt = s.html.length;
      s.html = putzen(s.html);
      console.log(`   Widget ${e.id}: ${alt} → ${s.html.length} Zeichen (${alt - s.html.length} entfernt)`);
      gefunden++;
    }
    if (e.elements) durchlaufen(e.elements);
  });
  durchlaufen(daten);

  if (!gefunden) { console.log('Kein <style>-Block gefunden — nichts zu tun.'); return; }

  const neuerInhalt = putzen(vorher.data.content.raw);

  const res = await api(`posts/${POST}`, {
    method: 'POST',
    body: JSON.stringify({
      content: neuerInhalt,
      meta: { _elementor_data: JSON.stringify(daten) },
    }),
  });

  if (!res.ok) { console.error(`Fehlgeschlagen (HTTP ${res.status})`, JSON.stringify(res.data).slice(0, 300)); process.exit(1); }

  console.log(`\n✅ Beitrag ${POST} bereinigt`);
  console.log(`   post_content: ${vorher.data.content.raw.length} → ${res.data.content.raw.length} Zeichen`);
  console.log(`   CSS noch drin: ${res.data.content.raw.includes('<style>')}`);
  console.log(`   Beginnt jetzt mit: ${res.data.content.raw.trim().slice(0, 90).replace(/\s+/g, ' ')}`);
};

run();
