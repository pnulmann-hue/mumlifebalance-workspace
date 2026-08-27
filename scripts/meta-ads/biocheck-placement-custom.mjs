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

async function uploadImg(file) {
  const buf = readFileSync(DIR + file);
  const fd = new FormData();
  fd.append('filename', new Blob([buf]), file);
  fd.append('access_token', T);
  const up = await fetch('https://graph.facebook.com/v20.0/' + ACT + '/adimages', { method: 'POST', body: fd }).then(r => r.json());
  return up.images ? Object.values(up.images)[0].hash : (console.log('IMG-ERR', file, JSON.stringify(up.error || up)), null);
}

const CONCEPTS = [
  { name: 'Bio-Check · Schaufenster', oldAd: '120254873036890054',
    sq: 'bio_check_variante_schaufenster_mit_echter_bio.png',
    pt: 'bio_check_variante_schaufenster_hochformat_mit_echter_bio.png',
    headline: 'Was sehen Menschen auf deinem Profil?',
    msg: `Was sehen Menschen in den ersten Sekunden, wenn sie auf dein Profil kommen? Genau das entscheidet, ob sie bleiben — oder weiterscrollen.

Dein Profil ist dein Schaufenster. Steht da oben nur „Mama & Beraterin", ist die Chance oft vertan, bevor sie begonnen hat. Dabei müsste deine Bio in Sekunden zeigen, für wen du da bist und was du löst.

Mein kostenloser Bio-Check zeigt dir in rund 10 Minuten:
✅ eine persönliche Analyse deines Profils
✅ 5 fertige Bio-Vorschläge
✅ dein PDF per E-Mail

Mach jetzt den kostenlosen Bio-Check. 🤍
👉 mumlifebalance.ch/bio-check` },
  { name: 'Bio-Check · Problem', oldAd: '120254873039620054',
    sq: 'bio_check_variante_problem_mit_echter_bio.png',
    pt: 'bio_check_variante_problem_hochformat_mit_echter_bio.png',
    headline: 'Du postest — aber niemand fragt an?',
    msg: `Du postest regelmässig — und trotzdem meldet sich niemand? Oft liegt das nicht an deiner Reichweite, sondern an deiner Bio, die in Sekunden nicht verrät, warum jemand bei dir bleiben soll.

Der häufigste Grund, warum sich niemand auf dein Angebot meldet, entscheidet sich schon in dem Moment, in dem jemand zum ersten Mal auf dein Profil klickt.

Mein kostenloser Bio-Check gibt dir in rund 10 Minuten:
✅ eine persönliche Analyse deines Profils
✅ 5 fertige Bio-Vorschläge
✅ dein PDF per E-Mail

Mach jetzt den kostenlosen Bio-Check. 🤍
👉 mumlifebalance.ch/bio-check` },
];

for (const c of CONCEPTS) {
  const sqHash = await uploadImg(c.sq);
  const ptHash = await uploadImg(c.pt);
  if (!sqHash || !ptHash) { console.log(c.name, '→ übersprungen (Bild-Fehler)'); continue; }

  const asset_feed_spec = {
    images: [
      { hash: sqHash, adlabels: [{ name: 'sq' }] },
      { hash: ptHash, adlabels: [{ name: 'pt' }] },
    ],
    bodies: [{ text: c.msg }],
    titles: [{ text: c.headline }],
    descriptions: [{ text: DESC }],
    link_urls: [{ website_url: URL }],
    call_to_action_types: ['LEARN_MORE'],
    ad_formats: ['SINGLE_IMAGE'],
    asset_customization_rules: [
      { customization_spec: { publisher_platforms: ['instagram'], instagram_positions: ['story', 'reels'] }, image_label: { name: 'pt' } },
      { customization_spec: { publisher_platforms: ['instagram'] }, image_label: { name: 'sq' } },
    ],
  };

  const cr = await post(ACT + '/adcreatives', {
    name: c.name + ' · Platzierung',
    object_story_spec: JSON.stringify({ page_id: PAGE }),
    asset_feed_spec: JSON.stringify(asset_feed_spec),
  });
  if (!cr.id) { console.log(c.name, 'CREATIVE-FEHLER:', JSON.stringify(cr.error || cr)); continue; }

  const ad = await post(ACT + '/ads', { name: c.name + ' (Feed+Story)', adset_id: ADSET, creative: JSON.stringify({ creative_id: cr.id }), status: 'ACTIVE' });
  if (!ad.id) { console.log(c.name, 'AD-FEHLER:', JSON.stringify(ad.error || ad)); continue; }
  console.log(c.name, '→ NEUE AD:', ad.id);

  // alte 1:1-only-Anzeige pausieren
  const p = await post(c.oldAd, { status: 'PAUSED' });
  console.log('   alte 1:1-Ad pausiert:', p.success ? 'ok' : JSON.stringify(p));
}
console.log('FERTIG.');
