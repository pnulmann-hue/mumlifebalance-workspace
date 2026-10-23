#!/usr/bin/env node
/**
 * Holt gestaltete Seiten aus dem 1140-px-Kasten auf die volle Breite (22.10.2026).
 *
 * Patricia: „bei einigen seiten ist sie eingezogen bei der ansicht am computer.“
 * Ursache (gemessen mit seiten-pruefen.mjs): Die Seite besteht aus EINEM Elementor-Container
 * im Modus „boxed“ (max. 1140 px, 10 px Rand), darin ein Text-/HTML-Widget mit der ganzen
 * gestalteten Seite. Farbflächen und Hero-Bilder hören deshalb bei 1140 px auf, links und
 * rechts bleibt Weiss, oben ein 10-px-Streifen.
 *
 * Lösung: genau diese Container auf content_width „full“ und Rand 0 stellen.
 * Am HTML selbst wird nichts geändert. Container mit mehreren echten Elementor-Widgets
 * (gebaute Seiten wie /angebote/) werden nicht angefasst.
 *
 *   node --env-file=.env seiten-vollbreite.mjs [--trocken] <seiten-id> …
 * Danach Elementor → Werkzeuge → „Lösche Dateien und Daten“.
 */

const WP = process.env.WP_URL?.replace(/\/$/, '');
const AUTH = 'Basic ' + Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString('base64');
const TROCKEN = process.argv.includes('--trocken');
const IDS = process.argv.slice(2).filter((a) => /^\d+$/.test(a));

if (!process.env.WP_APP_PASSWORD || !IDS.length) {
  console.error('Aufruf: node --env-file=.env seiten-vollbreite.mjs [--trocken] <seiten-id> …');
  process.exit(1);
}

const api = async (route, options = {}) => {
  const res = await fetch(`${WP}/wp-json/wp/v2/${route}`, {
    ...options,
    headers: { Authorization: AUTH, 'Content-Type': 'application/json', ...(options.headers || {}) },
  });
  const text = await res.text();
  let data; try { data = JSON.parse(text); } catch { data = { raw: text.slice(0, 300) }; }
  return { ok: res.ok, status: res.status, data };
};

const NUR_INHALT = new Set(['text-editor', 'html', 'shortcode']);
const NULL_RAND = { unit: 'px', top: '0', right: '0', bottom: '0', left: '0', isLinked: true };

for (const id of IDS) {
  const s = await api(`pages/${id}?context=edit`);
  if (!s.ok) { console.log(`${id}: nicht lesbar (${s.status})`); continue; }
  const roh = s.data.meta?._elementor_data;
  if (!roh) { console.log(`${id} ${s.data.slug}: keine Elementor-Daten — übersprungen`); continue; }
  const daten = JSON.parse(roh);
  let geaendert = 0;
  for (const c of daten) {
    if (c.elType !== 'container') continue;
    const kinder = c.elements || [];
    // nur Container, die ausschliesslich eingebettetes HTML tragen
    if (!kinder.length || !kinder.every((k) => k.elType === 'widget' && NUR_INHALT.has(k.widgetType))) continue;
    const st = c.settings || (c.settings = {});
    if (st.content_width === 'full' && JSON.stringify(st.padding) === JSON.stringify(NULL_RAND)) continue;
    st.content_width = 'full';
    st.padding = NULL_RAND;
    st.padding_tablet = NULL_RAND;
    st.padding_mobile = NULL_RAND;
    st.flex_gap = { unit: 'px', column: '0', row: '0', size: 0, isLinked: true };
    geaendert++;
  }
  if (!geaendert) { console.log(`${id} ${s.data.slug}: schon volle Breite oder kein passender Container`); continue; }
  if (TROCKEN) { console.log(`${id} ${s.data.slug}: ${geaendert} Container würden auf volle Breite gestellt`); continue; }
  const r = await api(`pages/${id}`, { method: 'POST', body: JSON.stringify({ meta: { _elementor_data: JSON.stringify(daten) } }) });
  console.log(`${id} ${s.data.slug}: ${r.ok ? `✓ ${geaendert} Container auf volle Breite` : `✗ ${r.status} ${JSON.stringify(r.data).slice(0, 120)}`}`);
}
