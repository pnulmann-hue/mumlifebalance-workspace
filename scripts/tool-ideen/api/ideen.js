/* =============================================================
   Vercel API Route: /api/ideen — Tool-Ideen-Generator
   =============================================================
   Nische + Mailadresse rein, fünf Ideen für ein Gratis-Tool raus.

   Ablauf: Kontakt in ActiveCampaign anlegen (Liste + Tag) → Zähler lesen
   → bei MAX_DURCHGAENGE Schluss → Claude → Zähler + Nische zurückschreiben.
   Ohne ActiveCampaign gibt es keine Ideen: ohne Zähler gäbe es keine Grenze.

   Environment: ANTHROPIC_API_KEY, AC_API_URL, AC_API_KEY (Pflicht)
                ANTHROPIC_MODEL, AC_LISTE, AC_TAG, AC_FELD_ZAEHLER,
                AC_FELD_NISCHE, MAX_DURCHGAENGE (optional, Vorgaben unten)

   Request:  POST { art: 'thema', angaben: {produkt, erfahrung, ergebnisse, fragen, perspektive, wem}, email, einverstanden }
             POST { art: 'tools', nische, produkt?, email, einverstanden }   (website = Honigtopf)
   ============================================================= */

import Anthropic from '@anthropic-ai/sdk';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';

export const config = { runtime: 'nodejs', maxDuration: 120 };

const MODEL = process.env.ANTHROPIC_MODEL || 'claude-sonnet-5-5';
const LISTE = process.env.AC_LISTE || '2';            // Regulärer Newsletter/Interessenten
const TAG = process.env.AC_TAG || '108';              // 0€ Nischengenerator
const FELD_ZAEHLER = process.env.AC_FELD_ZAEHLER || '19';
const FELD_NISCHE = process.env.AC_FELD_NISCHE || '20';
const MAX = Number(process.env.MAX_DURCHGAENGE || 10);

// art "thema": Nischengenerator nach Patricias Kurs „Finde dein Thema“ (lib/thema-prompt.md)
// art "tools": fünf Gratis-Tool-Ideen zu einem Thema (lib/system-prompt.md)
const PROMPTS = { thema: 'thema-prompt.md', tools: 'system-prompt.md' };
const promptCache = {};
async function systemPrompt(art) {
  if (promptCache[art]) return promptCache[art];
  const datei = PROMPTS[art];
  for (const p of [join(process.cwd(), 'lib', datei), join(process.cwd(), 'scripts/tool-ideen/lib', datei)]) {
    try { promptCache[art] = await readFile(p, 'utf-8'); return promptCache[art]; } catch { /* nächster */ }
  }
  throw new Error(datei + ' nicht gefunden');
}

const FELDER = ['produkt', 'erfahrung', 'ergebnisse', 'fragen', 'perspektive', 'wem'];
function angabenText(a) {
  const namen = { produkt: 'Was ich in meinem Network anbiete', erfahrung: 'Quelle 1, meine Erfahrung',
    ergebnisse: 'Quelle 2, meine Ergebnisse', fragen: 'Quelle 4, was mich die Leute immer wieder fragen, wofür ich gelobt werde',
    perspektive: 'Quelle 3, meine Perspektive und was ich gern mache', wem: 'Wem ich am liebsten helfen würde' };
  return FELDER.filter((k) => a[k]).map((k) => `${namen[k]}: ${a[k]}`).join('\n\n');
}

// ---------- ActiveCampaign ----------
async function ac(pfad, methode = 'GET', body) {
  const r = await fetch(`${process.env.AC_API_URL}/api/3${pfad}`, {
    method: methode,
    headers: { 'Api-Token': process.env.AC_API_KEY, Accept: 'application/json', 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!r.ok) throw Object.assign(new Error(`AC ${methode} ${pfad.split('?')[0]} ${r.status}`), { ac: true });
  return r.json();
}

async function kontaktUndZaehler(email) {
  const { contact } = await ac('/contact/sync', 'POST', { contact: { email } });
  const { fieldValues = [] } = await ac(`/contacts/${contact.id}/fieldValues`);
  const z = fieldValues.find((f) => String(f.field) === FELD_ZAEHLER);
  return { id: contact.id, zaehler: Number(z?.value) || 0 };
}

async function eintragen(id) {
  // Liste und Tag; ein bereits vorhandener Tag oder Listeneintrag ist kein Fehler
  await Promise.allSettled([
    ac('/contactLists', 'POST', { contactList: { list: LISTE, contact: id, status: 1 } }),
    ac('/contactTags', 'POST', { contactTag: { contact: id, tag: TAG } }),
  ]);
}

// ---------- Prüfung der KI-Antwort ----------
const VERBOTE = [
  [/[Nn]icht[^.!?]{0,80}[,.:]\s*[Ss]ondern/, 'nicht … sondern'],
  [/\b[Ss]ondern\b/, 'sondern'],
  [/(Problem|Frage|Punkt|Grund) ist nicht/, 'Das Problem ist nicht …'],
  [/[Ss]tell dir[^.!?]{0,60}vor/, 'Stell dir vor'],
  [/ß/, 'ß statt ss'],
  [/\b[Kk]und(:)?innen?\b/, 'Kundin (falsche Ebene)'],
  [/\b(heilt|heilen|lindert|lindern|gegen (Krankheit|Schmerzen|Depression))\b/, 'Heilversprechen'],
];

function extractJson(text) {
  let t = text.trim().replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/i, '').trim();
  const a = t.indexOf('{'), b = t.lastIndexOf('}');
  if (a !== -1 && b !== -1) t = t.slice(a, b + 1);
  return JSON.parse(t);
}

function verboteFinden(roh) {
  let text = roh;
  try {
    const d = extractJson(roh);
    const alle = (x) => (typeof x === 'string' ? [x] : Array.isArray(x) ? x.flatMap(alle) : x && typeof x === 'object' ? Object.values(x).flatMap(alle) : []);
    text = alle(d).join('\n');
  } catch { /* roh prüfen */ }
  const saetze = text.split(/(?<=[.!?])\s+|\n/);
  const funde = [];
  for (const [re, name] of VERBOTE) {
    for (let i = 0; i < saetze.length; i++) {
      const s = saetze[i];
      if (re.test(s) || (name.startsWith('nicht') && re.test(s + ' ' + (saetze[i + 1] || '')))) {
        funde.push(`${name}: „${s.trim().slice(0, 160)}“`); break;
      }
    }
  }
  return funde;
}

function gueltig(art, d) {
  if (art === 'thema') {
    return d && Array.isArray(d.themen) && d.themen.length >= 2
      && d.themen.every((t) => t && t.satz && /^Ich helfe /.test(t.satz) && t.produkt && Array.isArray(t.beitraege));
  }
  return d && Array.isArray(d.ideen) && d.ideen.length >= 3
    && d.ideen.every((i) => i && i.name && i.problem && i.ergebnis && i.auftrag);
}

// ---------- Handler ----------
export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  try {
    const { art: rohArt, angaben: rohAngaben, email: rohEmail, nische: rohNische, produkt: rohProdukt, einverstanden, website } = req.body || {};
    const art = rohArt === 'thema' ? 'thema' : 'tools';
    const angaben = {};
    for (const k of FELDER) angaben[k] = String((rohAngaben || {})[k] || '').trim().slice(0, 1200);
    if (website) return res.status(200).json({ ideen: [] }); // Honigtopf: nur Bots füllen dieses Feld
    const email = String(rohEmail || '').trim().toLowerCase();
    const nische = String(rohNische || '').trim().slice(0, 600);
    const produkt = String(rohProdukt || '').trim().slice(0, 200);
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 120) return res.status(400).json({ error: 'Bitte gib eine gültige Mailadresse ein.' });
    if (art === 'tools' && nische.length < 8) return res.status(400).json({ error: 'Beschreib dein Thema in einem Satz, damit die Ideen passen.' });
    if (art === 'thema' && (angaben.erfahrung + angaben.ergebnisse + angaben.fragen).length < 30) {
      return res.status(400).json({ error: 'Schreib bei deiner Erfahrung, deinen Ergebnissen oder den Fragen, die man dir stellt, noch ein paar Sätze mehr. Daraus entsteht dein Thema.' });
    }
    if (einverstanden !== true) return res.status(400).json({ error: 'Bitte bestätige, dass du Mails von mir bekommen möchtest.' });
    for (const k of ['ANTHROPIC_API_KEY', 'AC_API_URL', 'AC_API_KEY']) {
      if (!process.env[k]) return res.status(500).json({ error: `${k} nicht gesetzt` });
    }

    const kontakt = await kontaktUndZaehler(email);
    if (kontakt.zaehler >= MAX) {
      return res.status(429).json({ error: `Du hast deine ${MAX} Durchgänge gebraucht. Wenn du mit einer Idee weitermachen willst, schreib mir auf Instagram.`, rest: 0 });
    }
    await eintragen(kontakt.id);

    const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
    const auftrag = art === 'thema'
      ? `Meine Angaben:\n\n${angabenText(angaben)}\n\nFinde drei Themen für mich und formuliere je einen Experten-Satz. Antworte nur mit dem JSON.`
      : `Mein Thema: ${nische}\n${produkt ? `Was ich in meinem Network anbiete: ${produkt}\n` : ''}\nGib mir fünf Ideen für ein Gratis-Tool. Antworte nur mit dem JSON.`;
    async function call(verlauf, versuch = 1) {
      try {
        return await client.messages.create({
          model: MODEL, max_tokens: 6000, system: await systemPrompt(art),
          // Sonnet 5.5 schaltet das Vorab-Denken so ab („disabled“ lehnt es mit 400 ab)
          thinking: { type: 'between_tools' }, messages: verlauf,
        });
      } catch (err) {
        const voruebergehend = err.status >= 500 || err.status === 429 || err.name === 'APIConnectionError';
        if (voruebergehend && versuch < 2) { await new Promise((r) => setTimeout(r, 1500)); return call(verlauf, versuch + 1); }
        throw err;
      }
    }
    const text = (r) => r.content.filter((b) => b.type === 'text').map((b) => b.text).join('\n').trim();

    const verlauf = [{ role: 'user', content: auftrag }];
    let antwort = await call(verlauf);
    let roh = text(antwort);
    for (let runde = 1; runde <= 2; runde++) {
      const funde = verboteFinden(roh);
      if (!funde.length) break;
      console.log(`Verbot (Runde ${runde}):`, funde.map((f) => f.split(':')[0]));
      antwort = await call([...verlauf, { role: 'assistant', content: roh }, { role: 'user', content:
        `In deiner Antwort stehen verbotene Muster:\n${funde.map((f) => '- ' + f).join('\n')}\nSchreib genau diese Stellen neu. Kein Gegensatz mit „sondern“, keine Heilversprechen, für die Zielgruppe „deine Leute“ statt „Kundin“. Gib danach das komplette JSON nochmal aus.` }]);
      roh = text(antwort);
    }

    let daten;
    try { daten = extractJson(roh); } catch { daten = null; }
    if (!gueltig(art, daten)) {
      console.error('Antwort unbrauchbar:', antwort.stop_reason, roh.length, 'Zeichen');
      return res.status(502).json({ error: 'Das hat nicht geklappt, bitte nochmal. Der Versuch zählt nicht.', retryable: true });
    }

    const neu = kontakt.zaehler + 1;
    await ac('/contact/sync', 'POST', { contact: { email, fieldValues: [
      { field: FELD_ZAEHLER, value: String(neu) }, { field: FELD_NISCHE, value: (art === 'thema' ? daten.themen[0].satz : nische).slice(0, 250) },
    ] } }).catch((e) => console.error('Zähler nicht geschrieben:', e.message));

    console.log('ideen OK', { art, model: MODEL, in: antwort.usage?.input_tokens, out: antwort.usage?.output_tokens, durchgang: neu });
    return res.status(200).json({ ...daten, rest: Math.max(0, MAX - neu), max: MAX });
  } catch (err) {
    console.error('ideen Fehler:', { name: err.name, message: err.message, status: err.status });
    if (err.ac) return res.status(503).json({ error: 'Die Anmeldung hat gerade nicht geklappt, bitte versuch es in ein paar Minuten nochmal.', retryable: true });
    const nochmal = err.status >= 500 || err.status === 429 || err.name === 'APIConnectionError' || err.name === 'APITimeoutError';
    return res.status(nochmal ? 503 : 500).json({ error: 'Das hat nicht geklappt, bitte nochmal.', retryable: nochmal });
  }
}
