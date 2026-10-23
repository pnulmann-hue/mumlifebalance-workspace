#!/usr/bin/env node
/**
 * MBA-Block auf der Angebote-Seite (/angebote/, WP 3099) neu — 22.10.2026, Patricia:
 * „die MBA soll prominenter beworben werden. gestalte das schöner bitte … nehme easy ki
 * auch oben dazu“.
 *
 *   - alter MBA-Block (Klon des VIP-Blocks, aus angebote-ergaenzen.mjs) fliegt raus
 *   - neuer Block auf Dunkelblau mit Foto, steht direkt nach dem Säulen-Überblick und
 *     vor den Kundenstimmen — dort, wo sie sich noch nicht durch die Einzelkurse gelesen hat
 *   - alle vier Kurse gleichwertig in einer Liste (Easy KI nicht mehr als Nachsatz),
 *     darunter was das ganze Jahr dazukommt; kein Preis (MBA-Preis nie auf Fremdseiten)
 *
 * Wiederholbar. node --env-file=.env angebote-mba-block.mjs [--trocken]
 * Danach Elementor → Werkzeuge → „Lösche Dateien und Daten“.
 */

const WP = process.env.WP_URL?.replace(/\/$/, '');
const AUTH = 'Basic ' + Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString('base64');
const SEITE = 3099;
const TROCKEN = process.argv.includes('--trocken');

if (!process.env.WP_APP_PASSWORD) {
  console.error('WP_APP_PASSWORD fehlt — mit --env-file=.env starten.');
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

const benutzt = new Set();
const ids = (knoten) => { for (const e of knoten) { benutzt.add(e.id); ids(e.elements || []); } };
const neueId = () => {
  let id;
  do { id = Math.floor(Math.random() * 0xfffffff).toString(16).padStart(7, '0'); } while (benutzt.has(id));
  benutzt.add(id);
  return id;
};

const FARBE = { petrol: '#12828c', dunkel: '#29556d', creme: '#F1ECDD', orange: '#DC822E' };
const MARKE = 'mba-block-2026-10';   // CSS-ID des Blocks, daran wird er wiedererkannt
// Patricia, 22.10.: „bitte die mum business academy nach der roadmap platzieren“
const NACH = '42fcc384';              // Roadmap (sechs Schritte) — der Block kommt direkt dahinter

const px = (n) => ({ unit: 'px', size: n, sizes: [] });
const rand = (o, r, u, l) => ({ unit: 'px', top: String(o), right: String(r), bottom: String(u), left: String(l), isLinked: false });

const widget = (widgetType, settings) => ({ id: neueId(), elType: 'widget', widgetType, settings, elements: [] });
const container = (settings, elements) => ({ id: neueId(), elType: 'container', isInner: true, settings: { content_width: 'full', ...settings }, elements });

const ueberschrift = (title, { size, tag = 'h2', color = FARBE.creme, gewicht = '500', abstand = 0, sizeMobil } = {}) =>
  widget('heading', {
    title, header_size: tag, title_color: color,
    typography_typography: 'custom', typography_font_size: px(size), typography_font_weight: gewicht,
    ...(sizeMobil ? { typography_font_size_mobile: px(sizeMobil) } : {}),
    _margin: rand(0, 0, abstand, 0),
  });

const liste = (punkte) => widget('icon-list', {
  icon_list: punkte.map((text) => ({ _id: neueId(), text, selected_icon: { value: 'fas fa-check', library: 'fa-solid' } })),
  icon_color: FARBE.orange, text_color: FARBE.creme,
  icon_size: px(15), space_between: px(10), text_indent: px(10),
  icon_typography_typography: 'custom', icon_typography_font_size: px(18), icon_typography_font_size_mobile: px(16),
  _margin: rand(0, 0, 24, 0),
});

const block = () => ({
  id: neueId(),
  elType: 'container',
  settings: {
    _element_id: MARKE,
    content_width: 'boxed',
    boxed_width: px(1100),
    flex_direction: 'row',
    flex_direction_mobile: 'column',
    flex_align_items: 'center',
    flex_gap: { unit: 'px', column: '56', row: '32', size: 56, isLinked: false },
    background_background: 'classic',
    background_color: FARBE.dunkel,
    padding: rand(90, 24, 90, 24),
    padding_mobile: rand(56, 20, 56, 20),
  },
  elements: [
    container({ width: { unit: '%', size: 42, sizes: [] }, width_mobile: { unit: '%', size: 100, sizes: [] } }, [
      widget('image', {
        image: { id: 3856, url: `${WP}/wp-content/uploads/2026/06/mba-patricia.jpg`, alt: 'Patricia lächelt in die Kamera, im Hintergrund Schilf und See', source: 'library', size: '' },
        width: { unit: '%', size: 100, sizes: [] },
        height: px(520), height_mobile: px(320),
        'object-fit': 'cover',
        image_border_radius: { unit: 'px', top: '18', right: '18', bottom: '18', left: '18', isLinked: true },
        custom_css: 'selector img { object-position: 72% 30%; }',
      }),
    ]),
    container({ width: { unit: '%', size: 58, sizes: [] }, width_mobile: { unit: '%', size: 100, sizes: [] } }, [
      ueberschrift('ALLES IN EINEM PAKET', { size: 14, tag: 'p', color: FARBE.orange, gewicht: '600', abstand: 8 }),
      ueberschrift('Mum Business Academy', { size: 44, sizeMobil: 32, abstand: 14 }),
      widget('text-editor', {
        editor: '<p>Dein ganzes Business-Jahr an einem Ort: alle vier Kurse, eine KI-Mentorin, die mitdenkt, und eine Gruppe, die mit dir dranbleibt.</p>',
        text_color: FARBE.creme,
        typography_typography: 'custom', typography_font_size: px(18),
        _margin: rand(0, 0, 18, 0),
      }),
      ueberschrift('Diese vier Kurse sind drin', { size: 20, tag: 'h3', abstand: 12 }),
      liste(['Instagram-Kundenmaschine', 'Mama-CEO', 'Digitale Produktwelt', 'Easy KI für Networkerinnen']),
      ueberschrift('Und dazu, ein ganzes Jahr lang', { size: 20, tag: 'h3', abstand: 12 }),
      liste(['PIA, deine KI-Mentorin', 'Zwei Live-Calls pro Monat', 'Die begleitete Telegram-Gruppe, in der ich persönlich antworte']),
      widget('button', {
        text: 'Mehr über die MBA',
        link: { url: `${WP}/mba/`, is_external: '', nofollow: '', custom_attributes: '' },
        size: 'md',
        background_color: FARBE.orange,
        button_background_hover_color: FARBE.petrol,
        button_text_color: '#FFFFFF',
        border_radius: { unit: 'px', top: '30', right: '30', bottom: '30', left: '30', isLinked: true },
        text_padding: rand(16, 34, 16, 34),
        typography_typography: 'custom', typography_font_size: px(17), typography_font_weight: '600',
      }),
    ]),
  ],
});

// --- Ablauf -------------------------------------------------------------------

const seite = await api(`pages/${SEITE}?context=edit`);
if (!seite.ok) { console.error('Seite nicht lesbar:', seite.status); process.exit(1); }
const daten = JSON.parse(seite.data.meta._elementor_data);
ids(daten);

const getan = [];

// alter Block: oberste Ebene, enthält eine Überschrift „Mum Business Academy“, ist aber nicht der neue
const hatMba = (e) => (e.elements || []).some((k) => (k.widgetType === 'heading' && k.settings.title === 'Mum Business Academy') || hatMba(k));
const alt = daten.findIndex((e) => e.settings?._element_id !== MARKE && hatMba(e));
if (alt >= 0) { daten.splice(alt, 1); getan.push('alter MBA-Block raus'); }

const roadmap = daten.findIndex((e) => e.id === NACH);
if (roadmap < 0) { console.error('Roadmap-Block nicht gefunden'); process.exit(1); }
const jetzt = daten.findIndex((e) => e.settings?._element_id === MARKE);
if (jetzt < 0) {
  daten.splice(roadmap + 1, 0, block());
  getan.push('neuer MBA-Block nach der Roadmap');
} else if (jetzt !== roadmap + 1) {
  const [mba] = daten.splice(jetzt, 1);
  daten.splice(daten.findIndex((e) => e.id === NACH) + 1, 0, mba);
  getan.push('MBA-Block hinter die Roadmap verschoben');
}

if (!getan.length) { console.log('Nichts zu tun — alles schon da.'); process.exit(0); }
console.log('Änderungen:\n - ' + getan.join('\n - '));
if (TROCKEN) { console.log('(--trocken: nichts gespeichert)'); process.exit(0); }

const r = await api(`pages/${SEITE}`, { method: 'POST', body: JSON.stringify({ meta: { _elementor_data: JSON.stringify(daten) } }) });
if (!r.ok) { console.error('Speichern fehlgeschlagen:', r.status, JSON.stringify(r.data).slice(0, 300)); process.exit(1); }
console.log('Gespeichert.');
