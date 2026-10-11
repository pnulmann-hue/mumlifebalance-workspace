#!/usr/bin/env node
/**
 * Gleicht `post_content` eines Elementor-Beitrags wieder mit den Elementor-Daten ab.
 *
 * WARUM DAS NÖTIG IST:
 * Jedes Speichern im Block-Editor schreibt eine abgeflachte Fassung nach `post_content`
 * und wirft dabei die <p>-Tags raus. Für die Website ist das egal — Elementor rendert
 * aus `_elementor_data`. Aber **Rank Math liest `post_content`** und sieht dann statt
 * 45 Absätzen einen einzigen Block. Ergebnis: „Ein Absatz ist zu lang" unter Lesbarkeit,
 * obwohl kein Absatz länger als 65 Wörter ist.
 *
 * Nach jedem Speichern im Editor also einmal laufen lassen:
 *   node --env-file=scripts/wordpress/.env scripts/wordpress/sync-elementor-content.mjs 4048
 *
 * Danach: WP-Admin → Elementor → Werkzeuge → „Lösche Dateien und Daten."
 * (sonst zeigt die Website weiter die zwischengespeicherte Fassung)
 */

const WP = process.env.WP_URL?.replace(/\/$/, '');
const AUTH = 'Basic ' + Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString('base64');
const POST = process.argv[2];

if (!POST) {
  console.error('Bitte Beitrags-ID angeben, z.B.: ... sync-elementor-content.mjs 4048');
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

const absaetze = (html) => (html.match(/<p[ >]/g) || []).length;

const run = async () => {
  const vorher = await api(`posts/${POST}?context=edit`);
  if (!vorher.ok) { console.error(`Beitrag ${POST} nicht lesbar (HTTP ${vorher.status})`); process.exit(1); }

  const daten = JSON.parse(vorher.data.meta._elementor_data || '[]');
  let html = '';
  const lauf = (els) => els.forEach((e) => {
    const s = e.settings || {};
    if (typeof s.html === 'string' && s.html.includes('mama-artikel')) html = s.html;
    if (e.elements) lauf(e.elements);
  });
  lauf(daten);

  if (!html) { console.error('Kein Artikel-HTML in den Elementor-Daten gefunden (fehlt die Klasse "mama-artikel"?)'); process.exit(1); }

  const vorherAbs = absaetze(vorher.data.content.raw);
  const nachherAbs = absaetze(html);

  if (vorherAbs === nachherAbs) {
    console.log(`Nichts zu tun — post_content hat bereits ${vorherAbs} Absätze.`);
    return;
  }

  const res = await api(`posts/${POST}`, { method: 'POST', body: JSON.stringify({ content: html }) });
  if (!res.ok) { console.error(`Fehlgeschlagen (HTTP ${res.status})`, JSON.stringify(res.data).slice(0, 300)); process.exit(1); }

  console.log(`✅ Beitrag ${POST} abgeglichen`);
  console.log(`   Absätze in post_content: ${vorherAbs} → ${absaetze(res.data.content.raw)}`);
  console.log(`   Zeichen: ${vorher.data.content.raw.length} → ${res.data.content.raw.length}`);
  console.log(`\n   Jetzt noch: Elementor → Werkzeuge → „Lösche Dateien und Daten."`);
};

run();
