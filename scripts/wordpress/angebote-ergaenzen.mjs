#!/usr/bin/env node
/**
 * Ergänzt die Angebote-Seite (/angebote/, WP 3099, Elementor) um die neuen Kurse
 * und zieht die Beschreibung der Instagram-Kundenmaschine nach (Patricia, 22.10.2026).
 *
 *   Easy KI   → Karte in Säule 2 (Businessaufbau)
 *   Mama-CEO  → Karte in Säule 3 (Mama-Business-Alltag)
 *   MBA       → eigener Block vor „VIP 1:1 Mentoring“ (Bündel über alle drei Säulen)
 *   Kundenmaschine → Evergreen-Kurs statt 8-Wochen-Gruppenprogramm
 *
 * Wiederholbar: Karten, deren Titel schon dasteht, werden nicht doppelt angelegt.
 *   node --env-file=.env angebote-ergaenzen.mjs [--trocken]
 *
 * Danach: WP-Admin → Elementor → Werkzeuge → „Lösche Dateien und Daten“,
 * sonst fehlt den neuen Elementen ihr generiertes CSS.
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

// --- Hilfen -------------------------------------------------------------------

const finde = (knoten, id) => {
  for (const e of knoten) {
    if (e.id === id) return e;
    const r = finde(e.elements || [], id);
    if (r) return r;
  }
  return null;
};

const alleTitel = (knoten, out = []) => {
  for (const e of knoten) {
    if (e.widgetType === 'heading') out.push(e.settings.title);
    alleTitel(e.elements || [], out);
  }
  return out;
};

const benutzt = new Set();
const neueId = () => {
  let id;
  do { id = Math.floor(Math.random() * 0xfffffff).toString(16).padStart(7, '0'); } while (benutzt.has(id));
  benutzt.add(id);
  return id;
};
const ids = (knoten) => { for (const e of knoten) { benutzt.add(e.id); ids(e.elements || []); } };

// Tiefe Kopie mit frischen IDs
const klon = (e) => {
  const k = JSON.parse(JSON.stringify(e));
  const neu = (n) => { n.id = neueId(); (n.elements || []).forEach(neu); };
  neu(k);
  return k;
};

// Karte aus einer bestehenden Karte (Bild · Titel · Text · Knopf)
const karte = (vorlage, { bild, titel, text, link }) => {
  const k = klon(vorlage);
  const [img, h, t, b] = k.elements;
  if (img.widgetType !== 'image' || h.widgetType !== 'heading' || t.widgetType !== 'text-editor' || b.widgetType !== 'button') {
    throw new Error('Vorlage hat nicht den Aufbau Bild · Titel · Text · Knopf');
  }
  img.settings.image = { ...img.settings.image, ...bild, source: 'library', size: '' };
  h.settings.title = titel;
  t.settings.editor = text;
  b.settings.link = { url: link, is_external: '', nofollow: '', custom_attributes: '' };
  return k;
};

// --- Inhalte ------------------------------------------------------------------

const EASY_KI = {
  titel: 'Easy KI für Networkerinnen – vom Chat zur Mitarbeiterin',
  bild: { id: 4285, url: `${WP}/wp-content/uploads/2026/09/kk-about.jpg`, alt: 'Patricia lächelt in die Kamera, im Hintergrund Bäume' },
  text: '<p>Du benutzt KI bisher vor allem wie Google? In zehn Kapiteln richtest du sie dir so ein, dass sie dich kennt und dir die Arbeit abnimmt, die du jede Woche wieder machst – Schritt für Schritt und ohne Fachwörter-Salat.</p><p>In der Mum Business Academy ist der Kurs schon mit dabei.</p>',
  link: `${WP}/ki-kurs/`,
};

const MAMA_CEO = {
  titel: 'Mama-CEO',
  bild: { id: 3597, url: `${WP}/wp-content/uploads/2026/05/379-Patricia_Nulmann_mumlifebalance_schoniaugeblick-379-scaled.jpg`, alt: 'Patricia steht mit ausgebreiteten Armen in einer Blumenwiese' },
  text: '<p>Lerne, wie du als Mama mit wenig Zeit genug aus deinem Business holst – mit Wochenrhythmus, Strukturen und KI als Hebel.</p><p>Fünf Säulen, sofort freigeschaltet, und du startest, wann es für dich passt.</p>',
  link: `${WP}/mama-ceo/`,
};

const MBA = {
  titel: 'Mum Business Academy',
  unter: 'Drei Kurse, ein ganzes Jahr Begleitung und PIA – alles, was dein Business braucht, an einem Ort',
  text: '<p>Instagram-Kundenmaschine, Mama-CEO und Digitale Produktwelt in einem Paket. Dazu PIA, deine KI-Mentorin, zwei Live-Calls pro Monat und die begleitete Telegram-Gruppe, in der ich persönlich antworte – ein ganzes Jahr lang.</p><p>Und Easy KI für Networkerinnen ist für dich gratis mit dabei.</p>',
  link: `${WP}/mba/`,
};

const KUNDENMASCHINE_TEXT = '<p>Baue dir eine klare Instagram-Routine auf, die aus Kontakten Gespräche macht und dir Kunden &amp; Partner bringt.</p><p>Ein Kurs für Mamas im Networkmarketing mit erprobtem Schritt-für-Schritt-System – sofort freigeschaltet, ohne Vorkenntnisse und in deinem eigenen Tempo.</p>';

// --- Ablauf -------------------------------------------------------------------

const seite = await api(`pages/${SEITE}?context=edit`);
if (!seite.ok) { console.error('Seite nicht lesbar:', seite.status, seite.data); process.exit(1); }
const daten = JSON.parse(seite.data.meta._elementor_data);
ids(daten);
const titel = alleTitel(daten);

const VORLAGE_KARTE = finde(daten, '1d5fd31');   // „Finde dein Thema“ — Bild · Titel · Text · Knopf
const SAEULE_2 = finde(daten, '04c7f1b');
const SAEULE_3 = finde(daten, 'f23c15a');
const VIP = '83d3315';
const KUNDENMASCHINE = finde(daten, '4fbe1f1');
for (const [n, e] of Object.entries({ VORLAGE_KARTE, SAEULE_2, SAEULE_3, KUNDENMASCHINE })) {
  if (!e) { console.error(`Element ${n} nicht gefunden — wurde die Seite im Editor umgebaut?`); process.exit(1); }
}

const getan = [];

if (!titel.includes(EASY_KI.titel)) { SAEULE_2.elements.push(karte(VORLAGE_KARTE, EASY_KI)); getan.push('Easy KI → Säule 2'); }
if (!titel.includes(MAMA_CEO.titel)) { SAEULE_3.elements.push(karte(VORLAGE_KARTE, MAMA_CEO)); getan.push('Mama-CEO → Säule 3'); }

if (!titel.includes(MBA.titel)) {
  const i = daten.findIndex((e) => e.id === VIP);
  if (i < 0) { console.error('VIP-Block nicht gefunden'); process.exit(1); }
  const block = klon(daten[i]);
  // Kein zweites Pusteblumen-Bild direkt hintereinander: heller Grund statt Foto
  delete block.settings.background_image;
  block.settings.background_color = '#F1ECDD';
  block.settings.padding = { unit: 'px', top: '60', right: '10', bottom: '60', left: '10', isLinked: false };
  const [h1, h2, txt, knopf] = block.elements[0].elements;
  h1.settings.title = MBA.titel;
  h2.settings.title = MBA.unter;
  txt.settings.editor = MBA.text;
  knopf.settings.link = { url: MBA.link, is_external: '', nofollow: '', custom_attributes: '' };
  knopf.settings.text = 'Mehr erfahren';
  daten.splice(i, 0, block);
  getan.push('MBA → eigener Block vor VIP 1:1 Mentoring');
}

if (KUNDENMASCHINE.settings.editor !== KUNDENMASCHINE_TEXT) {
  KUNDENMASCHINE.settings.editor = KUNDENMASCHINE_TEXT;
  getan.push('Kundenmaschine: Evergreen-Text');
}

if (!getan.length) { console.log('Nichts zu tun — alles schon da.'); process.exit(0); }
console.log('Änderungen:\n - ' + getan.join('\n - '));
if (TROCKEN) { console.log('(--trocken: nichts gespeichert)'); process.exit(0); }

const r = await api(`pages/${SEITE}`, {
  method: 'POST',
  body: JSON.stringify({ meta: { _elementor_data: JSON.stringify(daten) } }),
});
if (!r.ok) { console.error('Speichern fehlgeschlagen:', r.status, JSON.stringify(r.data).slice(0, 300)); process.exit(1); }

const nach = await api(`pages/${SEITE}?context=edit`);
const t2 = alleTitel(JSON.parse(nach.data.meta._elementor_data));
for (const t of [EASY_KI.titel, MAMA_CEO.titel, MBA.titel]) console.log(t2.includes(t) ? '✓' : '✗', t);
console.log('Status:', nach.data.status);
