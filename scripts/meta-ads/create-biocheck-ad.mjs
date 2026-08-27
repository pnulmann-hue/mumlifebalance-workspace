import { readFileSync } from 'node:fs';

const T = process.env.META_ACCESS_TOKEN;
const ACT = process.env.META_AD_ACCOUNT_ID;
const ADSET = '120254824830370054';
const URL = 'https://mumlifebalance.ch/bio-check';
const IMG = 'C:/Users/pnulm/Downloads/bio_check_meta_quadrat.png';

const g = (u) => fetch('https://graph.facebook.com/v20.0/' + u + (u.includes('?') ? '&' : '?') + 'access_token=' + T).then(r => r.json());
const post = (p, params) => fetch('https://graph.facebook.com/v20.0/' + p, { method: 'POST', body: new URLSearchParams({ ...params, access_token: T }) }).then(r => r.json());

const MSG = `Du postest regelmässig — und trotzdem bleibt es erstaunlich still. Keine Kommentare, keine Nachrichten, keine Anfragen.

Das Frustrierende daran ist, dass es meistens gar nicht an deiner Reichweite liegt. Oft ist es dein Profil selbst: In den drei Sekunden, in denen jemand draufschaut, wird nicht klar, für wen du da bist und was du löst. Also scrollt genau die richtige Person weiter, obwohl dein Angebot perfekt gepasst hätte.

Genau hier hilft dir mein kostenloser Bio-Check. In rund 10 Minuten hast du:
✅ eine persönliche Analyse deines Profils
✅ 5 fertige Bio-Vorschläge, aus denen ein Kundenmagnet wird
✅ dein PDF per E-Mail zum sofort Umsetzen

Ich bin Patricia, Mama von vier Kindern, und ich hab mein Network genau darüber aufgebaut — mit einem Profil, das Menschen anzieht, statt ihnen hinterherzulaufen.

Mach jetzt den kostenlosen Bio-Check. 🤍
👉 mumlifebalance.ch/bio-check`;

// 1) Page-ID aus bestehender Anzeige holen
const ex = await g('120254530706390054?fields=creative{object_story_spec{page_id}}');
const oss0 = (ex.creative && ex.creative.object_story_spec) || {};
const PAGE = oss0.page_id, IG = null;
console.log('PAGE:', PAGE, ex.error ? '| ERR ' + JSON.stringify(ex.error) : '');
if (!PAGE) process.exit(1);

// 2) Bild hochladen
const buf = readFileSync(IMG);
const fd = new FormData();
fd.append('filename', new Blob([buf]), 'biocheck_feed.png');
fd.append('access_token', T);
const up = await fetch('https://graph.facebook.com/v20.0/' + ACT + '/adimages', { method: 'POST', body: fd }).then(r => r.json());
const hash = up.images ? Object.values(up.images)[0].hash : null;
console.log('IMAGE HASH:', hash, up.error ? '| ERR ' + JSON.stringify(up.error) : '');
if (!hash) process.exit(1);

// 3) Creative
const oss = { page_id: PAGE, link_data: { message: MSG, link: URL, name: 'Kostenloser Bio-Check in 10 Min', description: 'Persönliche Analyse, 5 fertige Bio-Vorschläge & PDF – kostenlos.', image_hash: hash, call_to_action: { type: 'LEARN_MORE' } } };
if (IG) oss.instagram_actor_id = IG;
const cr = await post(ACT + '/adcreatives', { name: 'Bio-Check · Variante 1 · Quadrat', object_story_spec: JSON.stringify(oss) });
console.log('CREATIVE:', JSON.stringify(cr));
if (!cr.id) process.exit(1);

// 4) Anzeige (pausiert)
const ad = await post(ACT + '/ads', { name: 'Bio-Check · Variante 1', adset_id: ADSET, creative: JSON.stringify({ creative_id: cr.id }), status: 'PAUSED' });
console.log('AD:', JSON.stringify(ad));
