/* =============================================================
   Vercel API Route: /api/story — Story-Generator
   =============================================================
   Alltagssituation + Produkt → fertige Story-Abfolge (JSON)

   Regeln/Wissen: lib/system-prompt.md
   Environment:   ANTHROPIC_API_KEY (Pflicht), ZUGANGSCODES (Pflicht, kommagetrennt),
                  ANTHROPIC_MODEL (optional)

   Request:  POST { code, modus, situation, produkt, zielgruppe, anlass, ziel,
                    phase, details, reaktion, stichwort, schreibweise }
   ============================================================= */

import Anthropic from '@anthropic-ai/sdk';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';

export const config = { runtime: 'nodejs', maxDuration: 120 };

const MODEL = process.env.ANTHROPIC_MODEL || 'claude-sonnet-5';
const MAX_FELD = 1500; // Zeichen je Feld

let promptCache = null;
async function systemPrompt() {
  if (promptCache) return promptCache;
  for (const p of [join(process.cwd(), 'lib', 'system-prompt.md'), join(process.cwd(), 'scripts/story-generator/lib/system-prompt.md')]) {
    try { promptCache = await readFile(p, 'utf-8'); return promptCache; } catch { /* next */ }
  }
  throw new Error('system-prompt.md nicht gefunden');
}

const feld = (x) => (typeof x === 'string' ? x.trim().slice(0, MAX_FELD) : '');

const PHASEN = {
  aufwaermen: 'Aufwärmen (vor der Öffnung)',
  offen: 'Türen offen (erster Verkaufstag)',
  mitte: 'Mittendrin (Verkaufsphase läuft)',
  letzter: 'Letzter Tag',
  danach: 'Danach (Verkauf ist vorbei)',
};

function auftrag(e) {
  const zeilen = [
    `Alltagssituation: ${e.situation}`,
    `Produkt / Angebot: ${e.produkt}`,
    `Zielgruppe (für wen sie erzählt): ${e.zielgruppe || '(nicht angegeben — neutral bleiben)'}`,
    `Anlass: ${e.anlass || 'du wählst'}`,
  ];
  if (e.modus === 'pitch') {
    zeilen.push(`Sie ist gerade im Pitch. Phase: ${PHASEN[e.phase] || PHASEN.mitte}`);
    zeilen.push(`Angaben zu Preis, Frist, Inhalt: ${e.details || '(keine — Platzhalter setzen, wo nötig)'}`);
  } else {
    zeilen.push(`Ganz normaler Tag. Die Brücke führt zu: ${e.ziel === 'angebot' ? 'dem bezahlten Angebot' : 'dem Freebie bzw. dem kostenlosen Einstieg'}`);
  }
  zeilen.push(e.reaktion === 'stichwort'
    ? `Aufruf: Stichwort per Nachricht oder Kommentar. Stichwort: ${e.stichwort ? e.stichwort.toUpperCase() : '[STICHWORT]'}`
    : 'Aufruf: Link-Sticker in der Story.');
  zeilen.push(e.schreibweise === 'de'
    ? 'Schreibweise: Deutschland (ß wo üblich).'
    : 'Schreibweise: Schweiz — immer „ss“, nie „ß“.');
  return `${zeilen.join('\n')}\n\nBau die Story-Abfolge. Antworte AUSSCHLIESSLICH mit gültigem JSON in der Form aus dem System-Prompt.`;
}

const VERBOTE = [
  [/[Nn]icht[^.!?]{0,80}[,.:]\s*[Ss]ondern/, 'nicht … sondern'],
  [/\b[Ss]ondern\b/, 'sondern (Gegensatz nach Schema)'],
  [/[Kk]ennst du das/, 'Floskel „Kennst du das“'],
  [/(Problem|Frage|Punkt|Grund) ist nicht/, 'Das Problem ist nicht … (Gegensatz)'],
  [/\b(entsteht|liegt|ist|kommt|geht|fängt)\s+nicht\b[^.!?]{0,60}[.!?:]\s+(Es|Er|Sie|Das)\s+\1\b/, 'Kontrast über zwei Sätze (X nicht … Es X …)'],
  [/[Ss]tell dir[^.!?]{0,60}vor/, 'Stell dir vor'],
  [/(?:^|[\s„"])\p{L}+\.\s+\p{L}+\.(?:\s|$)/u, 'Stakkato (zwei Ein-Wort-Sätze hintereinander)'],
  [/\b(ihr Lieben|Ihr Lieben|habt ihr|seid ihr|euch)\b/, 'ihr/euch statt du'],
];

function texteAus(d) {
  const s = (d.slides || []).flatMap((x) => [x.overlay, x.sprechtext, x.sticker]);
  return [...s, d.regie_tipp, d.bogen].filter((x) => typeof x === 'string' && x).join('\n');
}

function verboteFinden(d, schreibweise) {
  const regeln = schreibweise === 'de' ? VERBOTE : [...VERBOTE, [/ß/, 'ß statt ss']];
  const saetze = texteAus(d).split(/(?<=[.!?])\s+|\n/);
  const funde = [];
  for (const [re, name] of regeln) {
    for (let i = 0; i < saetze.length; i++) {
      const ctx = saetze[i] + ' ' + (saetze[i + 1] || '');
      if (re.test(saetze[i]) || (name.startsWith('nicht') && re.test(ctx))) { funde.push(`${name}: „${saetze[i].trim().slice(0, 160)}“`); break; }
    }
  }
  return funde;
}

function jsonAus(text) {
  let t = text.trim().replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/i, '');
  const a = t.indexOf('{'); const b = t.lastIndexOf('}');
  if (a !== -1 && b !== -1) t = t.slice(a, b + 1);
  return JSON.parse(t);
}

function codeOk(code) {
  const liste = (process.env.ZUGANGSCODES || '').split(',').map((x) => x.trim().toUpperCase()).filter(Boolean);
  return liste.length > 0 && liste.includes(String(code || '').trim().toUpperCase());
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  try {
    const b = req.body || {};
    if (!codeOk(b.code)) return res.status(401).json({ error: 'Diesen Zugangscode kenne ich nicht. Er steht in deiner Kaufbestätigung.' });

    const e = {
      modus: b.modus === 'pitch' ? 'pitch' : 'alltag',
      situation: feld(b.situation), produkt: feld(b.produkt), zielgruppe: feld(b.zielgruppe),
      anlass: ['Nähe', 'Mehrwert', 'Haltung'].includes(b.anlass) ? b.anlass : '',
      ziel: b.ziel === 'angebot' ? 'angebot' : 'freebie',
      phase: PHASEN[b.phase] ? b.phase : 'mitte', details: feld(b.details),
      reaktion: b.reaktion === 'stichwort' ? 'stichwort' : 'link',
      stichwort: feld(b.stichwort).replace(/[^\p{L}\p{N}-]/gu, '').slice(0, 30),
      schreibweise: b.schreibweise === 'de' ? 'de' : 'ch',
    };
    if (e.situation.length < 15) return res.status(400).json({ error: 'Erzähl die Situation in ein, zwei Sätzen — je konkreter, desto besser.' });
    if (e.produkt.length < 3) return res.status(400).json({ error: 'Welches Produkt oder Angebot soll am Schluss kommen?' });

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) return res.status(500).json({ error: 'ANTHROPIC_API_KEY nicht gesetzt' });
    const client = new Anthropic({ apiKey });
    const system = await systemPrompt();

    async function rufen(nachrichten, versuch = 1) {
      try {
        return await client.messages.create({
          model: MODEL, max_tokens: 6000, system,
          thinking: { type: 'disabled' },
          messages: nachrichten,
        });
      } catch (err) {
        const kurz = err.status >= 500 || err.status === 429 || err.name === 'APIConnectionError';
        if (kurz && versuch < 2) { await new Promise((r) => setTimeout(r, 1500)); return rufen(nachrichten, versuch + 1); }
        throw err;
      }
    }
    const text = (r) => r.content.filter((x) => x.type === 'text').map((x) => x.text).join('\n').trim();

    const verlauf = [{ role: 'user', content: auftrag(e) }];
    let antwort = text(await rufen(verlauf));
    let daten;
    for (let runde = 0; runde <= 2; runde++) {
      try { daten = jsonAus(antwort); } catch { daten = null; }
      const funde = daten ? verboteFinden(daten, e.schreibweise) : ['Die Antwort war kein gültiges JSON.'];
      if (!funde.length || runde === 2) break;
      console.log(`Korrektur Runde ${runde + 1}:`, funde.map((f) => f.split(':')[0]));
      verlauf.push({ role: 'assistant', content: antwort });
      verlauf.push({ role: 'user', content: `Bitte korrigieren:\n${funde.map((f) => '- ' + f).join('\n')}\nSchreib nur diese Stellen neu (direkt sagen, was ist, keine Gegensatz-Schablone) und gib das komplette JSON nochmal aus.` });
      antwort = text(await rufen(verlauf));
    }
    if (!daten || !Array.isArray(daten.slides)) return res.status(502).json({ error: 'Hat nicht geklappt — bitte nochmal.', retryable: true });

    console.log('story OK', { modell: MODEL, slides: daten.slides.length }); // kein Inhalt ins Log
    return res.status(200).json(daten);
  } catch (err) {
    console.error('story Fehler:', { name: err.name, message: err.message, status: err.status });
    return res.status(503).json({ error: 'Hat nicht geklappt — bitte nochmal.', retryable: true });
  }
}
