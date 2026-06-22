/**
 * Bootcamp-Ad auf Multi-Placement umbauen
 * =======================================
 * Eine Anzeige, zwei Bilder: 4:5 im Feed, 9:16 in Story/Reels (Meta wählt
 * automatisch nach Platzierung). Erweitert das bestehende AdSet um Story/Reels,
 * baut ein neues Creative mit asset_feed_spec + Platzierungs-Regeln und ersetzt
 * die alte Einzelbild-Anzeige.
 *
 *   node --env-file=.env bootcamp-ad-multiplacement.js
 */

import { readFileSync } from 'node:fs';
import { basename } from 'node:path';

const V = 'v21.0';
const BASE = `https://graph.facebook.com/${V}`;
const TOKEN = process.env.META_ACCESS_TOKEN;
const ACC = process.env.META_AD_ACCOUNT_ID;
const PAGE_ID = '100753756193662';
const LANDING_URL = 'https://mumlifebalance.ch/bootcamp/';

const ADSET_ID = '120252801002370054';
const OLD_AD_ID = '120252801740660054';
const OLD_CREATIVE_ID = '1807043860328341';

const FEED_IMG = 'C:/Users/pnulm/Downloads/bootcamp_ad_customer_magnet.png';   // 4:5
const STORY_IMG = 'C:/Users/pnulm/Downloads/bootcamp_story_ad_magnet.png';    // 9:16

const PRIMARY_TEXT = `Wie viele Stunden hast du diese Woche in dein Business gesteckt, ohne dass am Ende etwas Fertiges dabei rauskam?

Ich kenne das selber. Du sitzt abends am Laptop, öffnest fünf Tabs, fängst drei Dinge an und um halb elf machst du den Deckel zu, weil die Kinder morgen früh wieder wach sind.

Ich führe mein Business mit vier Kindern in rund 18 Stunden pro Woche. Möglich macht das ein fester Wochenrhythmus und mittlerweile eine KI, die mir die Hälfte der Arbeit abnimmt. Genau diese KI lernst du im Mama-Business-Bootcamp kennen — sie heisst PIA und ist fünf Tage lang deine Mentorin.

So sieht deine Woche aus:

✅ Tag 1: dein Thema wird klar — PIA schreibt dir deine Bio
✅ Tag 2: deine ersten Hooks, mit denen Interessenten beim Scrollen hängenbleiben
✅ Tag 3: eine Mini-Wochenstruktur, die in dein Mama-Leben passt
✅ Tag 4: deine erste eigene Angebots-Idee
✅ Tag 5: dein roter Faden, der alles verbindet

Fünf Tage, kostenlos, alles in einer Telegram-Gruppe. Morgens kommt von mir ein kurzer Impuls, den Rest machst du in deinem Tempo, wann es zwischen Familie und Alltag passt.

Am Ende der Woche hast du deinen ersten Schritt schwarz auf weiss — und zur Abwechslung mal etwas Fertiges in der Hand.

👉 https://mumlifebalance.ch/bootcamp/`;

const TARGETING = {
  geo_locations: { countries: ['CH', 'AT', 'DE'], location_types: ['frequently_in', 'home', 'recent'] },
  age_min: 30,
  age_max: 45,
  genders: [2],
  flexible_spec: [{ interests: [
    { id: '6003389760112' }, { id: '6003723474182' }, { id: '6006944110643' },
  ] }],
  publisher_platforms: ['facebook', 'instagram'],
  facebook_positions: ['feed', 'story', 'facebook_reels'],
  instagram_positions: ['stream', 'story', 'reels'],
  targeting_automation: { advantage_audience: 0 },
};

async function post(path, params) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ ...params, access_token: TOKEN }),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`${path} → ${res.status}: ${text.slice(0, 700)}`);
  return JSON.parse(text);
}

async function del(id) {
  const res = await fetch(`${BASE}/${id}?access_token=${TOKEN}`, { method: 'DELETE' });
  return res.text();
}

async function upload(path) {
  const buf = readFileSync(path);
  const form = new FormData();
  form.append('access_token', TOKEN);
  form.append('source', new Blob([buf], { type: 'image/png' }), basename(path));
  const res = await fetch(`${BASE}/${ACC}/adimages`, { method: 'POST', body: form });
  const text = await res.text();
  if (!res.ok) throw new Error(`adimages → ${res.status}: ${text.slice(0, 600)}`);
  const data = JSON.parse(text);
  return data.images[Object.keys(data.images)[0]].hash;
}

(async () => {
  try {
    console.log('1️⃣  AdSet-Platzierungen auf Feed + Story/Reels erweitern...');
    await post(`/${ADSET_ID}`, { targeting: JSON.stringify(TARGETING) });
    console.log('   ✅ Platzierungen aktualisiert');

    console.log('2️⃣  Beide Bilder hochladen...');
    const feedHash = await upload(FEED_IMG);
    const storyHash = await upload(STORY_IMG);
    console.log(`   ✅ feed: ${feedHash}`);
    console.log(`   ✅ story: ${storyHash}`);

    console.log('3️⃣  Multi-Placement-Creative bauen...');
    const assetFeedSpec = {
      images: [
        { hash: feedHash, adlabels: [{ name: 'feed_img' }] },
        { hash: storyHash, adlabels: [{ name: 'story_img' }] },
      ],
      bodies: [{ text: PRIMARY_TEXT }],
      titles: [{ text: '5 Tage zum ersten Business-Schritt' }],
      descriptions: [{ text: 'Kostenloses Mama-Business-Bootcamp, 29.6.–3.7. · per Telegram, mit PIA.' }],
      link_urls: [{ website_url: LANDING_URL }],
      call_to_action_types: ['SIGN_UP'],
      ad_formats: ['SINGLE_IMAGE'],
      asset_customization_rules: [
        {
          customization_spec: {
            publisher_platforms: ['facebook', 'instagram'],
            facebook_positions: ['story', 'facebook_reels'],
            instagram_positions: ['story', 'reels'],
          },
          image_label: { name: 'story_img' },
        },
        {
          // Standard-Regel (niedrigste Priorität) mit leerer customization_spec —
          // fängt alle übrigen Platzierungen (Feed). Von Meta erzwungen.
          customization_spec: {},
          image_label: { name: 'feed_img' },
          is_default: true,
        },
      ],
    };

    const creative = await post(`/${ACC}/adcreatives`, {
      name: 'Bootcamp Creative — Multi-Placement (Feed 4:5 + Story 9:16)',
      object_story_spec: JSON.stringify({ page_id: PAGE_ID }),
      asset_feed_spec: JSON.stringify(assetFeedSpec),
    });
    console.log(`   ✅ creative_id: ${creative.id}`);

    console.log('4️⃣  Neue Anzeige (PAUSED) erstellen...');
    const ad = await post(`/${ACC}/ads`, {
      name: 'Bootcamp · Feed 4:5 + Story 9:16 · Kunden finden statt suchen',
      adset_id: ADSET_ID,
      creative: JSON.stringify({ creative_id: creative.id }),
      status: 'PAUSED',
    });
    console.log(`   ✅ ad_id: ${ad.id}`);

    console.log('5️⃣  Alte Einzelbild-Anzeige + Creative entfernen...');
    console.log('   alt ad:', await del(OLD_AD_ID));
    console.log('   alt creative:', await del(OLD_CREATIVE_ID));

    console.log('\n🎉 Fertig — eine Anzeige, zwei Formate, automatisch nach Platzierung.');
    console.log(`   AdSet: ${ADSET_ID}`);
    console.log(`   Ad:    ${ad.id}`);
    console.log(`   Creative: ${creative.id}`);
  } catch (e) {
    console.error('\n❌ Fehler:', e.message);
    process.exitCode = 1;
  }
})();
