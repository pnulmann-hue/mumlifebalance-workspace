#!/usr/bin/env node
/**
 * Zweiter Durchgang auf der Angebote-Seite (/angebote/, WP 3099, Elementor) — 22.10.2026.
 *
 * Anlass: Eine Kundin rief an, weil sie nicht wusste, welches Angebot für sie passt.
 * Patricias Entscheide nach der Prüfung mit dem Copywriting-Skill:
 *   - Familienorga, Mama-Zeit und „Dein starkes Mama-Business“ raus
 *   - die sechs Schritte oben werden zur Roadmap: jeder Schritt nennt sein Angebot
 *   - Kundenstimmen aus context/kundinnen-geschichten.md (alle freigegeben)
 *   - Texte glätten: Gegensatz-Sätze, Kundinnen-Ebene, Leerzeichen — die Zahlen bleiben
 *     (Julia empfiehlt sie ausdrücklich)
 *   - Workbook-Knopf bekommt seinen Link
 *
 * Setzt angebote-ergaenzen.mjs voraus. Wiederholbar: Was schon erledigt ist, wird übersprungen.
 *   node --env-file=.env angebote-ueberarbeiten.mjs [--trocken]
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

const finde = (knoten, id) => {
  for (const e of knoten) {
    if (e.id === id) return e;
    const r = finde(e.elements || [], id);
    if (r) return r;
  }
  return null;
};

const entferne = (knoten, id) => {
  for (const e of knoten) {
    const i = (e.elements || []).findIndex((k) => k.id === id);
    if (i >= 0) { e.elements.splice(i, 1); return true; }
    if (entferne(e.elements || [], id)) return true;
  }
  return false;
};

const benutzt = new Set();
const ids = (knoten) => { for (const e of knoten) { benutzt.add(e.id); ids(e.elements || []); } };
const neueId = () => {
  let id;
  do { id = Math.floor(Math.random() * 0xfffffff).toString(16).padStart(7, '0'); } while (benutzt.has(id));
  benutzt.add(id);
  return id;
};

const getan = [];
const fehler = [];

// --- 1 · Raus ----------------------------------------------------------------
const RAUS = {
  '9acd8f2': 'Mama-Zeit',
  '1876255': 'Familienorga for real',
  'defb60e': 'Dein starkes Mama-Business (1:1)',
};

// --- 2 · Roadmap: jeder Schritt nennt sein Angebot ---------------------------
const TC = 'https://mumlifebalance.thrivecart.com';
const a = (url, text) => `<a href="${url}">${text}</a>`;
const ROADMAP = {
  '5e80fe3c': [a(`${WP}/von-0-auf-echt/`, 'Gratis-Workbook „Von 0 auf echt“')],
  '13e35d0a': [a(`${TC}/thema-finden/`, 'Mini-Kurs „Finde dein Thema“'), a(`${TC}/magnet-ich/`, 'Dein Magnet-Ich (1:1)')],
  '7cec7f39': [a(`${TC}/expertin/`, 'Mini-Kurs „Expertin statt Verkäuferin“'), a(`${TC}/instagram-kundenmaschine/`, 'Instagram-Kundenmaschine')],
  '1c71e5cb': [a(`${TC}/eigene-produkterstellung/`, 'Mini-Kurs „Vom Network-Wissen zum eigenen Produkt“'), a(`${TC}/digitale-produktwelt/`, 'Vom Network-Wissen zur digitalen Produktwelt')],
  // Patricia, 22.10.: Easy KI gehört zu Schritt 5, zu Schritt 6 die MBA
  '6a424b1a': [a(`${WP}/mama-ceo/`, 'Mama-CEO'), a(`${WP}/ki-kurs/`, 'Easy KI für Networkerinnen')],
  'a481811': [a(`${WP}/mba/`, 'Mum Business Academy')],
};
const MARKE_ROADMAP = 'data-roadmap="1"';
const roadmapWidget = (links) => ({
  id: neueId(),
  elType: 'widget',
  widgetType: 'text-editor',
  elements: [],
  settings: {
    editor: `<p ${MARKE_ROADMAP}><strong>Dein Angebot dazu:</strong><br />${links.join('<br />')}</p>`,
    align: 'center',
    _margin: { unit: 'px', top: '0', right: '0', bottom: '0', left: '0', isLinked: false },
  },
});

// --- 3 · Kundenstimmen --------------------------------------------------------
// Kundin B aus context/kundinnen-geschichten.md — Wortlaut, nicht nacherzählt
const STIMME_B = {
  name: 'Teilnehmerin der Mum Business Academy',
  text: '<p>Für mich war es ein jetzt oder nie Entscheid. Gleichzeitig auch das Vertrauen in dich, weil du aus deinen eigenen Erfahrungen sprichst und in einer ähnlichen Situation bist, wie ich auch. Mehrere Kinder, Network, eigene Selbständigkeit usw. Und ganz klar das ins Tun kommen, zusammen mit dir, mit der Gruppe und den regelmässigen Calls. Der Austausch in der Gruppe und die Calls sind für mich so wertvoll, gemeinsam Ideen finden, auch ein gemeinsames weitergehen und nicht alles alleine erschaffen oder selber erarbeiten müssen. All das hat mich dazu bewogen zu buchen, nochmals weiterzugehen und noch nicht aufzugeben. 💜</p>',
};
const KARUSSELL = '6c60090';
const SLIDE_ILSE = '5ac4697';     // Tagesplaner (alter Kurs) → wird Kundin B
const SLIDE_MIRIAM = '78aa8e4';   // Familienmanagement-Kurs (fällt weg) → raus

// --- 4 · Texte glätten (Zahlen bleiben) ---------------------------------------
const TEXTE = [
  ['45c84de', 'aufbaust,damit', 'aufbaust, damit'],
  ['3dc41dbb', 'Statt nur über Produkte zu sprechen, lernst du, über deine <strong>Erfahrungen, Werte und Expertise</strong> zu sprechen.',
    'Du lernst, über deine <strong>Erfahrungen, Werte und Expertise</strong> zu sprechen – die Produkte kommen dabei ganz von selbst mit.'],
  ['17d67927', 'Ein nachhaltiges Business im Network entsteht nicht durch Zufall – sondern durch Klarheit, Struktur und Haltung.',
    'Ein Business im Network, das bleibt, steht auf drei Dingen: Klarheit, Struktur und Haltung.'],
  ['17d67927', 'Diese drei Säulen bilden das Fundament von Mum Life Balance.</span></p><p><span style="font-weight: 400;">Diese drei Säulen zeigen dir, wie du aus Engagement &amp; Herz Struktur machst',
    'Diese drei Säulen sind das Fundament von Mum Life Balance. Sie zeigen dir, wie du aus Engagement &amp; Herz Struktur machst'],
  ['33e5d01e', 'Du lernst, dich im Network nicht über dein Unternehmen oder deine Produkte zu definieren, sondern über deine Persönlichkeit, deine Erfahrungen und dein Thema.',
    'Du lernst, dich im Network über deine Persönlichkeit, deine Erfahrungen und dein Thema zu zeigen – dein Unternehmen und die Produkte laufen im Hintergrund mit.'],
  ['1db41a09', 'Erfolg beginnt nicht auf Social Media – er beginnt bei dir.',
    'Erfolg fängt bei dir an, lange bevor du etwas auf Social Media postest.'],
  ['1db41a09', 'verlieren.Hier', 'verlieren. Hier'],
  ['29b9ef8c', 'dich als Expertin sichtbar zu machen, statt als reine Produktverkäuferin.',
    'dich als Expertin sichtbar zu machen, die man wegen ihres Themas fragt.'],
  ['29b9ef8c', 'Statt dich über dein Unternehmen zu definieren, entwickelst du deine eigene Marke – </span><span style="font-weight: 400;">damit Menschen dir folgen, weil du inspirierst, nicht, weil du etwas verkaufst.',
    'Du entwickelst deine eigene Marke – </span><span style="font-weight: 400;">und die Leute folgen dir, weil du sie inspirierst.'],
  ['43540a30', 'täglich Kunden  ohne 24/7 am Handy sitzen zu müssen.', 'täglich Kunden, ohne 24/7 am Handy sitzen zu müssen.'],
  ['35dde01c', 'endlich Kundinnen erreichst', 'endlich deine Kundschaft erreichst'],
  ['e4b6085', 'Ein Business, das dich trägt, entsteht nicht durch Zufall – sondern durch Strategie.In dieser Säule',
    'Ein Business, das dich trägt, braucht eine Strategie. In dieser Säule'],
  ['e4b6085', '–  damit', '– damit'],
  ['0071251', 'Mini-Kurs für 37 CHF.', 'Mini-Kurs für 39 CHF.'],
  ['705b67d', 'aber auch Herz.In dieser Säule', 'aber auch Herz. In dieser Säule'],
  ['705b67d', 'einer Frau, die sich selbst führt – statt sich überfordert zu fühlen.',
    'einer Frau, die sich selbst führt und den Überblick behält.'],
  ['ac42571', 'dass es dich nicht überfordert, </span><span style="font-weight: 400;">sondern wirklich funktioniert – mit Klarheit',
    'dass es zu deinem Alltag passt und wirklich funktioniert – </span><span style="font-weight: 400;">mit Klarheit'],
];
const TITEL = [
  ['c5ef87a', 'Mini-Kurs "Finde dein Thema als Networking-Mama in 60 Minuten"', 'Mini-Kurs „Finde dein Thema als Networking-Mama in 60 Minuten“'],
];

// --- 5 · Workbook-Knopf --------------------------------------------------------
const WORKBOOK_KNOPF = '586664b';
const WORKBOOK_URL = `${WP}/von-0-auf-echt/`;

// --- Ablauf -------------------------------------------------------------------

const seite = await api(`pages/${SEITE}?context=edit`);
if (!seite.ok) { console.error('Seite nicht lesbar:', seite.status); process.exit(1); }
const daten = JSON.parse(seite.data.meta._elementor_data);
ids(daten);

for (const [id, name] of Object.entries(RAUS)) {
  if (entferne(daten, id)) getan.push(`raus: ${name}`);
}

for (const [id, links] of Object.entries(ROADMAP)) {
  const box = finde(daten, id);
  if (!box) { fehler.push(`Roadmap-Schritt ${id} fehlt`); continue; }
  const vorhanden = box.elements.find((e) => (e.settings?.editor || '').includes(MARKE_ROADMAP));
  if (vorhanden) {
    const soll = roadmapWidget(links).settings.editor;
    if (vorhanden.settings.editor !== soll) {
      vorhanden.settings.editor = soll;
      getan.push(`Roadmap neu verlinkt: ${box.elements[0].settings.title}`);
    }
    continue;
  }
  const nachText = box.elements.findIndex((e) => e.widgetType === 'text-editor') + 1;
  box.elements.splice(nachText, 0, roadmapWidget(links));
  getan.push(`Roadmap: ${finde(daten, box.elements[0].id).settings.title}`);
}

const karussell = finde(daten, KARUSSELL);
const ilse = finde(daten, SLIDE_ILSE);
if (karussell && ilse) {
  const [, h, t] = ilse.elements[0].elements;
  if (h.settings.title !== STIMME_B.name) {
    h.settings.title = STIMME_B.name;
    t.settings.editor = STIMME_B.text;
    getan.push('Kundenstimme: MBA-Teilnehmerin statt Tagesplaner');
  }
  const i = karussell.elements.findIndex((e) => e.id === SLIDE_MIRIAM);
  if (i >= 0) {
    karussell.elements.splice(i, 1);
    karussell.settings.carousel_items.splice(i, 1);
    getan.push('Kundenstimme raus: Familienmanagement-Kurs');
  }
} else fehler.push('Kundenstimmen-Karussell nicht gefunden');

for (const [id, alt, neu] of TEXTE) {
  const e = finde(daten, id);
  if (!e) { fehler.push(`Text ${id} fehlt`); continue; }
  const s = e.settings.editor;
  if (s.includes(neu) && !s.includes(alt)) continue;
  const n = s.split(alt).length - 1;
  if (n !== 1) { fehler.push(`Text ${id}: Stelle ${n}× gefunden — „${alt.slice(0, 40)}…“`); continue; }
  e.settings.editor = s.replace(alt, neu);
  getan.push(`Text ${id}: „${alt.replace(/<[^>]+>/g, '').slice(0, 45)}…“`);
}
for (const [id, alt, neu] of TITEL) {
  const e = finde(daten, id);
  if (e?.settings.title === alt) { e.settings.title = neu; getan.push(`Titel ${id}`); }
}

const knopf = finde(daten, WORKBOOK_KNOPF);
if (knopf && knopf.settings.link?.url !== WORKBOOK_URL) {
  knopf.settings.link = { url: WORKBOOK_URL, is_external: '', nofollow: '', custom_attributes: '' };
  getan.push('Workbook-Knopf verlinkt');
}

if (fehler.length) { console.error('Abbruch, nichts gespeichert:\n - ' + fehler.join('\n - ')); process.exit(1); }
if (!getan.length) { console.log('Nichts zu tun — alles schon da.'); process.exit(0); }
console.log(`Änderungen (${getan.length}):\n - ` + getan.join('\n - '));
if (TROCKEN) { console.log('(--trocken: nichts gespeichert)'); process.exit(0); }

const r = await api(`pages/${SEITE}`, {
  method: 'POST',
  body: JSON.stringify({ meta: { _elementor_data: JSON.stringify(daten) } }),
});
if (!r.ok) { console.error('Speichern fehlgeschlagen:', r.status, JSON.stringify(r.data).slice(0, 300)); process.exit(1); }
const nach = JSON.parse((await api(`pages/${SEITE}?context=edit`)).data.meta._elementor_data);
console.log('Gespeichert ·', Object.keys(RAUS).every((id) => !finde(nach, id)) ? '✓ drei Karten raus' : '✗ Karten noch da',
  '·', finde(nach, WORKBOOK_KNOPF).settings.link.url);
