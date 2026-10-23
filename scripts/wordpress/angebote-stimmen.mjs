#!/usr/bin/env node
/**
 * Mehr Kundenstimmen auf der Angebote-Seite (/angebote/, WP 3099) — 22.10.2026, Patricia:
 * „kannst du bitte noch mehr kundenstimmen ergänzen?“
 *
 * Quelle: outputs/produkte/mba-launch/testimonials/_INDEX.md — die ROHFASSUNG, wörtlich
 * (nicht die getrimmte zitate-uebersicht.md). Freigaben: Susanne + Miriam schriftlich im
 * Feedbackformular, alle Screenshots von Patricia am 1.7.2026. Nadja hat KEINE Freigabe
 * und bleibt draussen. Nur Vornamen.
 *
 * Wiederholbar: eine Stimme, deren Anfang schon im Karussell steht, wird übersprungen.
 *   node --env-file=.env angebote-stimmen.mjs [--trocken]
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

const benutzt = new Set();
const ids = (knoten) => { for (const e of knoten) { benutzt.add(e.id); ids(e.elements || []); } };
const neueId = () => {
  let id;
  do { id = Math.floor(Math.random() * 0xfffffff).toString(16).padStart(7, '0'); } while (benutzt.has(id));
  benutzt.add(id);
  return id;
};
const klon = (e) => {
  const k = JSON.parse(JSON.stringify(e));
  const neu = (n) => { n.id = neueId(); (n.elements || []).forEach(neu); };
  neu(k);
  return k;
};

const KARUSSELL = '6c60090';
const VORLAGE = '5ac4697';   // erste Folie (MBA-Teilnehmerin) — Bild · Name · Text

// Reihenfolge = Reihenfolge im Karussell, eingefügt nach der MBA-Teilnehmerin
const STIMMEN = [
  ['Susanne · Instagram-Kundenmaschine',
    'Den Instagram-Kundenmaschine-Kurs von Patricia kann ich wärmstens empfehlen. Ich habe viel gelernt über mich und meine Strategie nochmal komplett überarbeitet — und bin nach dem Kurs auch noch weiter dabei, das neue Wissen umzusetzen.'],
  ['Andrea · Story-Challenge',
    'Ich bin mitten in den Skiferien in die Story-Challenge gestartet, und ehrlich gesagt war es nicht immer einfach … Trotzdem habe ich weitergemacht. Meine Storyviews sind gestiegen, die Umfragen wurden aktiver genutzt und der Austausch mit meiner Community wurde spürbar intensiver. Nicht, weil ich Tricks gemacht habe, sondern weil ich mich mehr gezeigt habe. Und ich werde definitiv dranbleiben.'],
  ['Mentee',
    'Auf Insta läufts. Diese Woche ein Starterpaket verkauft. Und meine Follower sind sehr aktiv, wenn ich ein Call to Action mache. Jetzt darf ich noch mehr über meine Schmerzgrenze rausgehen und mich mal live zeigen.'],
  ['Miriam · Instagram-Kundenmaschine',
    'Die Instagram-Kundenmaschine hat mir ein einfaches und doch umfassendes Verständnis für die businessfokussierte Arbeit mit Instagram gegeben.'],
  ['Mentee · Positionierung',
    'Das Schönste an einer klaren Positionierung ist, dass ich den ‚Stein im Schuh‘ bei meiner Zielgruppe kenne und ansprechen kann — und somit Postsideen habe. Die Richtung ist klar.'],
  ['Mentee',
    'Ich möchte das, was ich mache, mit mehr Sinn machen. Bei den Insights sehe ich bereits Veränderung … Ich war bisher von der Wirkung im Vergleich zum Invest nicht so überzeugt — jetzt vertraue ich dem Prozess.'],
  ['Miriam · Story-Challenge',
    'Herzlichen Dank für die Instagram Story Challenge … Während der Woche konnte ich bereits viel mehr Interaktion auf meinem Profil beobachten. Mega cool. Deine Erklärungen sind wertvoll, leicht verständlich und gut umsetzbar.'],
  ['Teilnehmerin der Story-Challenge',
    'Mit deinem Workbook fiel es einfacher, die Storys zu erstellen und auch die Brücke zu meinem Angebot zu machen. Die Konsistenz, eine Woche dran zu bleiben, war sehr gut. Herzlichen Dank für deine Begleitung, deine Videos und Voice zu jedem Tag.'],
];

const seite = await api(`pages/${SEITE}?context=edit`);
if (!seite.ok) { console.error('Seite nicht lesbar:', seite.status); process.exit(1); }
const daten = JSON.parse(seite.data.meta._elementor_data);
ids(daten);

const karussell = finde(daten, KARUSSELL);
const vorlage = finde(daten, VORLAGE);
if (!karussell || !vorlage) { console.error('Karussell oder Vorlage-Folie nicht gefunden'); process.exit(1); }

const textVon = (folie) => folie.elements[0].elements.find((w) => w.widgetType === 'text-editor').settings.editor;
const schonDa = (zitat) => karussell.elements.some((f) => textVon(f).includes(zitat.slice(0, 40)));

let pos = karussell.elements.indexOf(vorlage) + 1;
const getan = [];
for (const [name, zitat] of STIMMEN) {
  if (schonDa(zitat)) { pos++; continue; }
  const folie = klon(vorlage);
  const [, h, t] = folie.elements[0].elements;
  h.settings.title = name;
  t.settings.editor = `<p>${zitat}</p>`;
  folie.settings._title = `Stimme ${name}`;
  karussell.elements.splice(pos, 0, folie);
  karussell.settings.carousel_items.splice(pos, 0, { slide_title: name, _id: neueId() });
  pos++;
  getan.push(name);
}

if (karussell.elements.length !== karussell.settings.carousel_items.length) {
  console.error('Folien und Karussell-Einträge laufen auseinander — nichts gespeichert'); process.exit(1);
}
if (!getan.length) { console.log('Nichts zu tun — alle Stimmen schon da.'); process.exit(0); }
console.log(`Neue Stimmen (${getan.length}):\n - ` + getan.join('\n - ') + `\nIm Karussell: ${karussell.elements.length}`);
if (TROCKEN) { console.log('(--trocken: nichts gespeichert)'); process.exit(0); }

const r = await api(`pages/${SEITE}`, { method: 'POST', body: JSON.stringify({ meta: { _elementor_data: JSON.stringify(daten) } }) });
if (!r.ok) { console.error('Speichern fehlgeschlagen:', r.status, JSON.stringify(r.data).slice(0, 300)); process.exit(1); }
console.log('Gespeichert.');
