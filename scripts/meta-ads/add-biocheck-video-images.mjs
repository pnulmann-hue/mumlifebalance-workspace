import { readFileSync } from 'node:fs';

const T = process.env.META_ACCESS_TOKEN;
const ACT = process.env.META_AD_ACCOUNT_ID;
const ADSET = '120254824830370054';
const PAGE = '100753756193662';
const URL = 'https://mumlifebalance.ch/bio-check';
const DESC = 'Persönliche Analyse, 5 fertige Bio-Vorschläge & PDF – kostenlos.';
const DIR = 'C:/Users/pnulm/Downloads/';

const g = (u) => fetch('https://graph.facebook.com/v20.0/' + u + (u.includes('?') ? '&' : '?') + 'access_token=' + T).then(r => r.json());
const post = (p, params) => fetch('https://graph.facebook.com/v20.0/' + p, { method: 'POST', body: new URLSearchParams({ ...params, access_token: T }) }).then(r => r.json());
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

const MSG_VIDEO = `Du postest — und trotzdem bleibt's erstaunlich still? Keine Kommentare, keine Anfragen.

Oft liegt das gar nicht an deiner Reichweite, sondern an deiner Bio: In den Sekunden, in denen jemand draufschaut, wird nicht klar, für wen du da bist und was du löst. Also scrollt genau die richtige Person weiter.

Mein kostenloser Bio-Check zeigt dir in rund 10 Minuten, was deine Bio gerade aussendet — und was sie aussenden müsste:
✅ eine persönliche Analyse deines Profils
✅ 5 fertige Bio-Vorschläge
✅ dein PDF per E-Mail

Ich bin Patricia, Mama von vier Kindern — und hab mein Network genau so aufgebaut.

Mach jetzt den kostenlosen Bio-Check. 🤍
👉 mumlifebalance.ch/bio-check`;

const IMAGES = [
  { file: 'bio_check_variante_schaufenster_mit_echter_bio.png', name: 'Bio-Check · Schaufenster', headline: 'Was sehen Menschen auf deinem Profil?',
    msg: `Was sehen Menschen in den ersten Sekunden, wenn sie auf dein Profil kommen? Genau das entscheidet, ob sie bleiben — oder weiterscrollen.

Dein Profil ist dein Schaufenster. Steht da oben nur „Mama & Beraterin", ist die Chance oft vertan, bevor sie begonnen hat. Dabei müsste deine Bio in Sekunden zeigen, für wen du da bist und was du löst.

Mein kostenloser Bio-Check zeigt dir in rund 10 Minuten:
✅ eine persönliche Analyse deines Profils
✅ 5 fertige Bio-Vorschläge
✅ dein PDF per E-Mail

Mach jetzt den kostenlosen Bio-Check. 🤍
👉 mumlifebalance.ch/bio-check` },
  { file: 'bio_check_variante_problem_mit_echter_bio.png', name: 'Bio-Check · Problem', headline: 'Du postest — aber niemand fragt an?',
    msg: `Du postest regelmässig — und trotzdem meldet sich niemand? Oft liegt das nicht an deiner Reichweite, sondern an deiner Bio, die in Sekunden nicht verrät, warum jemand bei dir bleiben soll.

Der häufigste Grund, warum sich niemand auf dein Angebot meldet, entscheidet sich schon in dem Moment, in dem jemand zum ersten Mal auf dein Profil klickt.

Mein kostenloser Bio-Check gibt dir in rund 10 Minuten:
✅ eine persönliche Analyse deines Profils
✅ 5 fertige Bio-Vorschläge
✅ dein PDF per E-Mail

Mach jetzt den kostenlosen Bio-Check. 🤍
👉 mumlifebalance.ch/bio-check` },
  { file: 'bio_check_variante_neugier_profilfoto_original.png', name: 'Bio-Check · Neugier', headline: 'Zieht dein Profil die Richtigen an?',
    msg: `Zieht dein Profil gerade die Richtigen an — oder scrollen genau die Menschen weiter, für die dein Angebot perfekt gewesen wäre?

Das meiste entscheidet sich in den ersten Sekunden auf deinem Profil. Ist da nicht sofort klar, für wen du da bist und was du löst, ist die richtige Person weg, bevor sie dein Angebot überhaupt gesehen hat.

Mein kostenloser Bio-Check zeigt dir in rund 10 Minuten:
✅ eine persönliche Analyse deines Profils
✅ 5 fertige Bio-Vorschläge
✅ dein PDF per E-Mail

Mach jetzt den kostenlosen Bio-Check. 🤍
👉 mumlifebalance.ch/bio-check` },
];

// ---------- 1) VIDEO hochladen ----------
console.log('→ Lade Video hoch …');
const vbuf = readFileSync(DIR + 'Bio-Check Ad.mp4');
const vfd = new FormData();
vfd.append('source', new Blob([vbuf]), 'bio-check-ad.mp4');
vfd.append('name', 'Bio-Check Ad (Untertitel)');
vfd.append('access_token', T);
const vup = await fetch('https://graph.facebook.com/v20.0/' + ACT + '/advideos', { method: 'POST', body: vfd }).then(r => r.json());
const VID = vup.id;
console.log('   VIDEO-ID:', VID, vup.error ? '| ERR ' + JSON.stringify(vup.error) : '');
if (!VID) process.exit(1);

// Warten bis verarbeitet
let ready = false;
for (let i = 0; i < 40; i++) {
  await sleep(5000);
  const st = await g(VID + '?fields=status');
  const phase = st.status && (st.status.video_status || (st.status.processing_phase && st.status.processing_phase.status));
  process.stdout.write('   Status: ' + JSON.stringify(st.status) + '\n');
  if (st.status && st.status.video_status === 'ready') { ready = true; break; }
  if (st.status && st.status.processing_phase && st.status.processing_phase.status === 'complete') { ready = true; break; }
  if (st.status && st.status.video_status === 'error') { console.log('   VIDEO-FEHLER'); break; }
}
if (!ready) console.log('   ⚠️ Video evtl. noch in Verarbeitung — versuche trotzdem Creative …');

// Thumbnail holen
let thumb = null;
for (let i = 0; i < 6; i++) {
  const th = await g(VID + '/thumbnails?fields=uri,is_preferred');
  if (th.data && th.data.length) {
    const pref = th.data.find(x => x.is_preferred) || th.data[0];
    thumb = pref.uri; break;
  }
  await sleep(4000);
}
console.log('   THUMBNAIL:', thumb ? 'ok' : 'keins gefunden');

// Video-Creative + Ad
const vOss = { page_id: PAGE, video_data: { video_id: VID, title: 'Kostenloser Bio-Check in 10 Min', message: MSG_VIDEO, link_description: DESC, call_to_action: { type: 'LEARN_MORE', value: { link: URL } } } };
if (thumb) vOss.video_data.image_url = thumb;
const vcr = await post(ACT + '/adcreatives', { name: 'Bio-Check · Video · Creative', object_story_spec: JSON.stringify(vOss) });
console.log('   VIDEO-CREATIVE:', vcr.id || JSON.stringify(vcr));
if (vcr.id) {
  const vad = await post(ACT + '/ads', { name: 'Bio-Check · Video', adset_id: ADSET, creative: JSON.stringify({ creative_id: vcr.id }), status: 'ACTIVE' });
  console.log('   VIDEO-AD:', vad.id || JSON.stringify(vad));
}

// ---------- 2) BILDER hochladen ----------
for (const im of IMAGES) {
  const buf = readFileSync(DIR + im.file);
  const fd = new FormData();
  fd.append('filename', new Blob([buf]), im.file);
  fd.append('access_token', T);
  const up = await fetch('https://graph.facebook.com/v20.0/' + ACT + '/adimages', { method: 'POST', body: fd }).then(r => r.json());
  const hash = up.images ? Object.values(up.images)[0].hash : null;
  if (!hash) { console.log(im.name, 'BILD-FEHLER:', JSON.stringify(up.error || up)); continue; }
  const oss = { page_id: PAGE, link_data: { message: im.msg, link: URL, name: im.headline, description: DESC, image_hash: hash, call_to_action: { type: 'LEARN_MORE' } } };
  const cr = await post(ACT + '/adcreatives', { name: im.name + ' · Creative', object_story_spec: JSON.stringify(oss) });
  if (!cr.id) { console.log(im.name, 'CREATIVE-FEHLER:', JSON.stringify(cr)); continue; }
  const ad = await post(ACT + '/ads', { name: im.name, adset_id: ADSET, creative: JSON.stringify({ creative_id: cr.id }), status: 'ACTIVE' });
  console.log(im.name, '→ AD:', ad.id || JSON.stringify(ad));
}

// ---------- 3) Alte Duplikate pausieren (Variante 2/4/5) ----------
const ads = await g(ADSET + '/ads?fields=name,status&limit=50');
for (const a of (ads.data || [])) {
  if (['Bio-Check · Variante 2', 'Bio-Check · Variante 4', 'Bio-Check · Variante 5'].includes(a.name) && a.status === 'ACTIVE') {
    const r = await post(a.id, { status: 'PAUSED' });
    console.log('PAUSIERT:', a.name, r.success ? 'ok' : JSON.stringify(r));
  }
}
console.log('FERTIG.');
