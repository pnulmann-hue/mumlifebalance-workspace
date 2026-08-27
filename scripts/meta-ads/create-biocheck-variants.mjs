const T = process.env.META_ACCESS_TOKEN;
const ACT = process.env.META_AD_ACCOUNT_ID;
const ADSET = '120254824830370054';
const PAGE = '100753756193662';
const HASH = '2bf8f1491a7f16fcdb8fa69d7f21acdf';
const URL = 'https://mumlifebalance.ch/bio-check';
const DESC = 'Persönliche Analyse, 5 fertige Bio-Vorschläge & PDF – kostenlos.';

const post = (p, params) => fetch('https://graph.facebook.com/v20.0/' + p, { method: 'POST', body: new URLSearchParams({ ...params, access_token: T }) }).then(r => r.json());

// 1) Ad-Set auf Instagram-only stellen
const targeting = { age_min: 28, age_max: 50, genders: [2], geo_locations: { countries: ['CH', 'AT', 'DE'] }, flexible_spec: [{ interests: [{ id: '6003305961221', name: 'Direktvertrieb' }] }], targeting_automation: { advantage_audience: 0 }, publisher_platforms: ['instagram'], instagram_positions: ['stream', 'story', 'reels', 'explore'] };
const upd = await post(ADSET, { targeting: JSON.stringify(targeting) });
console.log('AD-SET Instagram-only:', JSON.stringify(upd));

const variants = [
  { name: 'Bio-Check · Variante 2', headline: 'Warum dein Profil keine Kunden bringt', msg: `Der häufigste Grund, warum sich niemand auf dein Angebot meldet, hat nichts mit deiner Followerzahl zu tun.

Ich seh es ständig bei vielen im Network: Sie geben sich Mühe, posten, sind aktiv — und wundern sich, warum trotzdem kaum jemand schreibt. Dabei entscheidet sich das meiste schon in dem Moment, in dem jemand zum ersten Mal auf ihr Profil klickt. Steht da oben nur „Mama & Beraterin", ist die Chance oft vertan, bevor sie begonnen hat.

Mein kostenloser Bio-Check zeigt dir in rund 10 Minuten, was deine Bio gerade aussendet — und was sie aussenden müsste:
✅ eine persönliche Analyse deines Profils
✅ 5 fertige Bio-Vorschläge
✅ dein PDF per E-Mail

Mach jetzt den kostenlosen Bio-Check. 🤍
👉 mumlifebalance.ch/bio-check` },
  { name: 'Bio-Check · Variante 3', headline: 'Ohne Kaltakquise sichtbar werden', msg: `Du musst nicht ständig fremde Leute anschreiben, damit dein Network wächst.

Wenn dir das Abtelefonieren genauso widerstrebt wie mir früher, dann gibt es einen anderen Weg: ein Profil, das die Arbeit für dich macht — bei dem die richtigen Menschen von selbst draufklicken, verstehen, was du für sie tun kannst, und dir schreiben.

Der erste Schritt ist deine Bio. Die checkst du mit meinem kostenlosen Bio-Check in rund 10 Minuten:
✅ persönliche Analyse
✅ 5 fertige Bio-Vorschläge
✅ PDF per E-Mail

Ich bin Patricia, vierfache Mama, und hab mein Network so aufgebaut — ohne Kaltakquise.

Mach jetzt den kostenlosen Bio-Check. 🤍
👉 mumlifebalance.ch/bio-check` },
  { name: 'Bio-Check · Variante 4', headline: 'Aus Steckbrief wird Kundenmagnet', msg: `In meiner Instagram-Bio stand früher nur „Mama & Networkerin" — und genau deshalb hat sich kaum jemand gemeldet.

Ich dachte lange, ich müsste einfach mehr posten. Erst als ich verstanden hab, dass mein Profil in Sekunden zeigen muss, für wen ich da bin und was ich löse, kamen plötzlich Nachrichten von Menschen, die ich gar nicht kannte.

Damit du dir die Jahre Ausprobieren sparst, hab ich meinen Bio-Check gebaut. Kostenlos, in rund 10 Minuten:
✅ persönliche Analyse deines Profils
✅ 5 fertige Bio-Vorschläge
✅ PDF per E-Mail

Mach jetzt den kostenlosen Bio-Check. 🤍
👉 mumlifebalance.ch/bio-check` },
  { name: 'Bio-Check · Variante 5', headline: 'Zieht dein Profil die Richtigen an?', msg: `Du postest — und trotzdem meldet sich niemand? Oft liegt das nicht an deiner Reichweite, sondern an deiner Bio, die in Sekunden nicht verrät, warum jemand bei dir bleiben soll.

Mein kostenloser Bio-Check gibt dir in rund 10 Minuten eine persönliche Analyse, 5 fertige Bio-Vorschläge und dein PDF.

Mach jetzt den kostenlosen Bio-Check. 🤍
👉 mumlifebalance.ch/bio-check` },
];

for (const v of variants) {
  const oss = { page_id: PAGE, link_data: { message: v.msg, link: URL, name: v.headline, description: DESC, image_hash: HASH, call_to_action: { type: 'LEARN_MORE' } } };
  const cr = await post(ACT + '/adcreatives', { name: v.name + ' · Quadrat', object_story_spec: JSON.stringify(oss) });
  if (!cr.id) { console.log(v.name, 'CREATIVE-FEHLER:', JSON.stringify(cr)); continue; }
  const ad = await post(ACT + '/ads', { name: v.name, adset_id: ADSET, creative: JSON.stringify({ creative_id: cr.id }), status: 'PAUSED' });
  console.log(v.name, '→ AD:', ad.id || JSON.stringify(ad));
}
