/**
 * Webinar-Ad-Creator — lädt ein Visual hoch + erstellt Ad-Creative + Ad
 * ====================================================================
 *
 * Verwendung:
 *   node --env-file=.env create-webinar-ad.js <pfad-zum-visual.jpg>
 *
 * Voraussetzungen (sind schon erfüllt):
 *   - Campaign `120250147108050054` (KI-Mastermind Webinar Mai 2026, PAUSED)
 *   - AdSet `120250147119200054` (Cold DACH Frauen 30-45, CHF 15/Tag, PAUSED)
 *
 * Was passiert:
 *   1. Bild wird zu Meta hochgeladen → image_hash
 *   2. AdCreative wird erstellt mit:
 *      - Primärtext: Story-Driven Variante 1 (siehe outputs/ads/...)
 *      - Überschrift: "Mama + KI = 5h/Woche zurück"
 *      - Beschreibung: "90-Min Live-Webinar. Live-Geschenk inkl."
 *      - CTA: ANMELDEN
 *      - URL: https://webinar.mumlifebalance.ch/
 *   3. Ad wird angelegt (PAUSED) — du aktivierst sie in Meta Ads Manager
 *
 * Reviewen + Aktivieren:
 *   → Meta Ads Manager öffnen → Kampagne "KI-Mastermind Webinar Mai 2026"
 *   → Anzeige reviewen
 *   → Status auf ACTIVE setzen
 */

import { readFileSync, statSync, existsSync } from 'node:fs';
import { basename } from 'node:path';

const API_VERSION = 'v21.0';
const BASE_URL = `https://graph.facebook.com/${API_VERSION}`;
const TOKEN = process.env.META_ACCESS_TOKEN;
const ACC = process.env.META_AD_ACCOUNT_ID;
const PAGE_ID = '100753756193662';
const CAMPAIGN_ID = '120250147108050054';
const ADSET_ID = '120250147119200054';
const LANDING_URL = 'https://webinar.mumlifebalance.ch/';

if (!TOKEN || !ACC) {
  console.error('❌ META_ACCESS_TOKEN oder META_AD_ACCOUNT_ID fehlt in .env');
  process.exit(1);
}

const imagePath = process.argv[2];
if (!imagePath) {
  console.error('Usage: node --env-file=.env create-webinar-ad.js <pfad-zum-visual.jpg>');
  process.exit(1);
}
if (!existsSync(imagePath)) {
  console.error(`❌ Visual nicht gefunden: ${imagePath}`);
  process.exit(1);
}

const stats = statSync(imagePath);
console.log(`📷 Visual: ${imagePath} (${(stats.size / 1024).toFixed(0)} KB)`);

// ============================================================
// 1. Bild hochladen
// ============================================================

async function uploadImage() {
  const fileBuffer = readFileSync(imagePath);
  const fileName = basename(imagePath);
  const ext = fileName.split('.').pop().toLowerCase();
  const mimeType = ext === 'png' ? 'image/png' : 'image/jpeg';

  const form = new FormData();
  form.append('access_token', TOKEN);
  form.append('source', new Blob([fileBuffer], { type: mimeType }), fileName);

  const res = await fetch(`${BASE_URL}/${ACC}/adimages`, { method: 'POST', body: form });
  const text = await res.text();
  if (!res.ok) throw new Error(`Image upload ${res.status}: ${text.slice(0, 500)}`);
  const data = JSON.parse(text);
  // Hash ist unter data.images[<fileName>].hash
  const fileKey = Object.keys(data.images || {})[0];
  if (!fileKey) throw new Error(`No image hash returned: ${text}`);
  return data.images[fileKey].hash;
}

// ============================================================
// 2. Ad-Creative erstellen (5 Primärtexte + 5 Überschriften via Dynamic Creative Optimization)
// ============================================================

async function createCreative(imageHash) {
  const message = `Nach dem Tod meiner Schwester habe ich verstanden: Eine Mutter darf ein eigenes Leben leben.

Heute baue ich digitale Mitarbeiter für meinen Haushalt + Business — und gewinne 5+ Stunden pro Woche zurück.

Am Mi 20.5. zeige ich dir live wie du das auch schaffst — ohne Tech-Studium. 90 Minuten, kostenlos.`;

  const linkData = {
    link: LANDING_URL,
    message,
    name: 'Mama + KI = 5h/Woche zurück',
    description: '90-Min Live-Webinar mit konkreten Demos. Live-Geschenk: Kochassistent-Starter-Pack (CHF 49).',
    image_hash: imageHash,
    call_to_action: { type: 'SIGN_UP', value: { link: LANDING_URL } },
  };

  const objectStorySpec = {
    page_id: PAGE_ID,
    link_data: linkData,
  };

  const body = new URLSearchParams({
    name: 'KI-Webinar Creative A1 (Story-Driven)',
    object_story_spec: JSON.stringify(objectStorySpec),
    access_token: TOKEN,
  });

  const res = await fetch(`${BASE_URL}/${ACC}/adcreatives`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`Creative ${res.status}: ${text.slice(0, 500)}`);
  return JSON.parse(text).id;
}

// ============================================================
// 3. Ad erstellen (PAUSED)
// ============================================================

async function createAd(creativeId) {
  const body = new URLSearchParams({
    name: 'KI-Webinar A1 Story-Driven · 20.5.',
    adset_id: ADSET_ID,
    creative: JSON.stringify({ creative_id: creativeId }),
    status: 'PAUSED',
    access_token: TOKEN,
  });

  const res = await fetch(`${BASE_URL}/${ACC}/ads`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`Ad ${res.status}: ${text.slice(0, 500)}`);
  return JSON.parse(text).id;
}

// ============================================================
// Main
// ============================================================

(async () => {
  try {
    console.log('1️⃣  Bild hochladen...');
    const hash = await uploadImage();
    console.log(`   ✅ image_hash: ${hash}`);

    console.log('2️⃣  Ad-Creative erstellen...');
    const creativeId = await createCreative(hash);
    console.log(`   ✅ creative_id: ${creativeId}`);

    console.log('3️⃣  Ad erstellen (PAUSED)...');
    const adId = await createAd(creativeId);
    console.log(`   ✅ ad_id: ${adId}`);

    console.log('\n🎉 Fertig! Alles als PAUSED-Draft angelegt.\n');
    console.log('Was du jetzt machst:');
    console.log('  1. Meta Ads Manager öffnen: https://business.facebook.com/adsmanager/');
    console.log(`  2. Kampagne "KI-Mastermind Webinar Mai 2026" öffnen (${CAMPAIGN_ID})`);
    console.log(`  3. Ad "KI-Webinar A1 Story-Driven" reviewen (${adId})`);
    console.log('  4. Wenn alles passt: Kampagne + AdSet + Ad auf ACTIVE schalten');
    console.log('  5. Meta-Review wartet 30 Min - 2h, dann läuft die Anzeige.');
  } catch (err) {
    console.error('\n❌ Fehler:', err.message);
    process.exit(1);
  }
})();
