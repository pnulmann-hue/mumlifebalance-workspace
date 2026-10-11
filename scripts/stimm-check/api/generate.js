/* =============================================================
   Vercel API Route: /api/generate — Stimm-Check
   =============================================================
   Schritt 1 = Stimm-Brief aus den sechs Angaben + Textprobe
   Schritt 2 = erster Text mit diesem Brief

   Voice/Regeln: lib/system-prompt.md
   Environment:  ANTHROPIC_API_KEY (Pflicht), ANTHROPIC_MODEL (optional)

   Request:  POST { step: 1, angaben }  |  { step: 2, brief, auftrag }
   ============================================================= */

import Anthropic from '@anthropic-ai/sdk';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';

export const config = { runtime: 'nodejs', maxDuration: 120 };

const MODEL = process.env.ANTHROPIC_MODEL || 'claude-sonnet-5';
const MAX_FELD = 4000; // Zeichen je Eingabefeld, damit niemand ein Buch hineinkippt

let promptCache = null;
async function loadSystemPrompt() {
  if (promptCache) return promptCache;
  const candidates = [
    join(process.cwd(), 'lib', 'system-prompt.md'),
    join(process.cwd(), 'scripts/stimm-check/lib/system-prompt.md'),
  ];
  for (const path of candidates) {
    try { promptCache = await readFile(path, 'utf-8'); return promptCache; } catch { /* next */ }
  }
  throw new Error('system-prompt.md nicht gefunden');
}

function kuerzen(obj) {
  const out = {};
  for (const [k, v] of Object.entries(obj || {})) {
    out[k] = typeof v === 'string' ? v.slice(0, MAX_FELD) : v;
  }
  return out;
}

function stepInstruction(step, { angaben, brief, auftrag }) {
  if (step === 1) {
    return `SCHRITT 1 — DER STIMM-BRIEF.\nAngaben der Nutzerin:\n${JSON.stringify(kuerzen(angaben))}\n\nErzeuge jetzt Beobachtungen zum Klang (mit wörtlichen Zitaten aus "probe"), den Brief in sechs Abschnitten, die Floskeln und die Nachschärf-Fragen.\nAntworte AUSSCHLIESSLICH mit gültigem JSON in der Form aus dem System-Prompt (keine Fences).`;
  }
  return `SCHRITT 2 — DER ERSTE TEXT.\nIhr Stimm-Brief:\n${JSON.stringify(kuerzen(brief))}\n\nAuftrag:\n${JSON.stringify(kuerzen(auftrag))}\n\nSchreib den Text.\nAntworte AUSSCHLIESSLICH mit gültigem JSON in der Form aus dem System-Prompt (keine Fences).`;
}

function textAus(response) {
  return response.content.filter((b) => b.type === 'text').map((b) => b.text).join('\n').trim();
}

// Dieselben Muster wie scripts/cockpit/texte-pruefen.py, auch über die Satzgrenze
const VERBOTE = [
  [/[Nn]icht[^.!?]{0,80}[,.:]\s*[Ss]ondern/, 'nicht … sondern'],
  [/\b[Ss]ondern\b/, 'sondern (Gegensatz nach Schema)'],
  [/(Problem|Frage|Punkt|Grund) ist nicht/, 'Das Problem ist nicht … (Gegensatz)'],
  [/[Ss]tell dir[^.!?]{0,60}vor/, 'Stell dir vor'],
  [/ß/, 'ß statt ss'],
];
// Liefert die betroffenen Sätze wörtlich, damit die Korrektur weiss, WO sie ansetzen muss
function verboteFinden(roh) {
  // Die „So nicht“-Beispiele sind absichtlich schlechte KI-Sätze — die werden nicht geprüft.
  let text = roh;
  try {
    const d = extractJson(roh);
    const sammeln = (x, k) => (k === 'so_nicht' ? [] : typeof x === 'string' ? [x]
      : Array.isArray(x) ? x.flatMap((y) => sammeln(y)) : x && typeof x === 'object'
      ? Object.entries(x).flatMap(([kk, v]) => sammeln(v, kk)) : []);
    text = sammeln(d).join('\n');
  } catch { /* kein JSON: roh prüfen */ }
  const saetze = text.split(/(?<=[.!?])\s+|\n/);
  const funde = [];
  for (const [re, name] of VERBOTE) {
    for (const s of saetze) {
      const ctx = s + ' ' + (saetze[saetze.indexOf(s) + 1] || '');
      if (re.test(s) || (name.startsWith('nicht') && re.test(ctx))) { funde.push(`${name}: „${s.trim().slice(0, 160)}“`); break; }
    }
  }
  return funde;
}

function extractJson(text) {
  let t = text.trim();
  t = t.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/i, '').trim();
  const first = t.indexOf('{');
  const last = t.lastIndexOf('}');
  if (first !== -1 && last !== -1) t = t.slice(first, last + 1);
  return JSON.parse(t);
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  try {
    const { step, angaben, brief, auftrag } = req.body || {};
    if (![1, 2].includes(step)) return res.status(400).json({ error: 'step 1|2 erforderlich' });
    if (step === 1 && !angaben) return res.status(400).json({ error: 'angaben fehlen' });
    if (step === 2 && (!brief || !auftrag)) return res.status(400).json({ error: 'brief + auftrag fehlen' });

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) return res.status(500).json({ error: 'ANTHROPIC_API_KEY nicht gesetzt' });

    const systemPrompt = await loadSystemPrompt();
    const client = new Anthropic({ apiKey });

    async function call(attempt = 1, korrektur = null, vorher = null) {
      try {
        return await client.messages.create({
          model: MODEL,
          max_tokens: 10000, // mit Denkphase reichten 3000 nicht für Denken + JSON
          system: systemPrompt,
          // Ohne Denkphase: 19 s + 10 s statt 40 s + 61 s, Klang gleich gut (getestet 25.09.)
          thinking: { type: 'disabled' },
          messages: [
            { role: 'user', content: stepInstruction(step, { angaben, brief, auftrag }) },
            ...(korrektur ? [{ role: 'assistant', content: vorher }, { role: 'user', content: korrektur }] : []),
          ],
        });
      } catch (err) {
        const transient = err.status >= 500 || err.status === 429 || err.name === 'APIConnectionError';
        if (transient && attempt < 2) { await new Promise((r) => setTimeout(r, 1500)); return call(attempt + 1, korrektur, vorher); }
        throw err;
      }
    }

    let response = await call();
    let text = textAus(response);

    // Gegenprobe gegen Muster, die das Modell trotz Verbot baut. Höchstens zwei Korrekturrunden.
    for (let runde = 1; runde <= 2; runde++) {
      const treffer = verboteFinden(text);
      if (!treffer.length) break;
      console.log(`Verbot gefunden (Runde ${runde}), schreibe neu:`, treffer.map((x) => x.split(':')[0]));
      const liste = treffer.map((t) => '- ' + t).join('\n');
      response = await call(1, `In deiner Antwort stehen verbotene Muster:\n${liste}\nSchreib genau diese Sätze neu, ohne Gegensatz: sag nur, was IST, in einem eigenen Satz. Kein „sondern“, kein „nicht …, …“. Gib danach das komplette JSON nochmal aus.`, text);
      text = textAus(response);
    }

    let data;
    try { data = extractJson(text); }
    catch {
      console.error('JSON-Parse fehlgeschlagen:', response.stop_reason, text.length, 'Zeichen'); // kein Inhalt ins Log — die Seite verspricht, dass nichts gespeichert wird
      return res.status(502).json({ error: 'KI-Antwort war kein gültiges JSON', retryable: true });
    }

    console.log('generate OK', { step, model: MODEL, in: response.usage?.input_tokens, out: response.usage?.output_tokens });
    return res.status(200).json(data);
  } catch (err) {
    console.error('generate error:', { name: err.name, message: err.message, status: err.status });
    const retryable = err.status >= 500 || err.status === 429 || err.name === 'APIConnectionError' || err.name === 'APITimeoutError';
    return res.status(retryable ? 503 : 500).json({ error: 'Hat nicht geklappt — bitte nochmal.', retryable });
  }
}
