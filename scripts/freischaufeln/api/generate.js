/* =============================================================
   Vercel API Route: /api/generate
   =============================================================
   KI-Gehirn für Freischaufeln. Steuert die 3 Schritte:
   1 = Familien-Aufgaben vorschlagen (nach Intake)
   2 = Halbieren (Kategorie + Vorschlag pro Aufgabe)
   3 = Haushalts-Blöcke + Business-Fenster

   Voice/Regeln kommen aus lib/system-prompt.md.

   Environment:
   - ANTHROPIC_API_KEY (Pflicht)

   Request:  POST { step: 1|2|3, intake, tasks, categories }
   Response: das im System-Prompt definierte JSON pro Schritt
   ============================================================= */

import Anthropic from '@anthropic-ai/sdk';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';

export const config = { runtime: 'nodejs', maxDuration: 60 };

let promptCache = null;
async function loadSystemPrompt() {
  if (promptCache) return promptCache;
  const candidates = [
    join(process.cwd(), 'lib', 'system-prompt.md'),
    join(process.cwd(), 'scripts/freischaufeln/lib/system-prompt.md'),
  ];
  for (const path of candidates) {
    try { promptCache = await readFile(path, 'utf-8'); return promptCache; } catch { /* next */ }
  }
  throw new Error('system-prompt.md nicht gefunden');
}

function stepInstruction(step, { intake, tasks, categories }) {
  const intakeStr = JSON.stringify(intake || {});
  if (step === 1) {
    return `SCHRITT 1 — KLARHEIT.\nIntake der Nutzerin: ${intakeStr}\n\nErzeuge jetzt die typische Wochen-Aufgabenliste für genau diese Familiensituation (15–22 Aufgaben), sortiert nach Mental-Load (sichtbar/mental/emotional).\nAntworte AUSSCHLIESSLICH mit gültigem JSON in genau dieser Form (keine Markdown-Fences, kein Text drumherum):\n{"schritt":1,"intro":"<2-3 warme Sätze>","aufgaben":[{"id":1,"name":"...","load":"sichtbar|mental|emotional|hut","frequenz":"..."}]}`;
  }
  if (step === 2) {
    return `SCHRITT 2 — HALBIEREN.\nIntake: ${intakeStr}\nDie (von der Nutzerin bestätigte/ergänzte) Aufgaben:\n${JSON.stringify(tasks || [])}\n\nSchlage pro Aufgabe genau EINE Kategorie vor (weg | delegieren | zusammenlegen | behalten) plus einen konkreten 1-Satz-Vorschlag. Sei mutig — mindestens die Hälfte soll weg/delegiert/zusammengelegt sein.\nAntworte AUSSCHLIESSLICH mit gültigem JSON (keine Fences):\n{"schritt":2,"eintraege":[{"id":1,"kategorie":"weg|delegieren|zusammenlegen|behalten","vorschlag":"<1 Satz>"}]}`;
  }
  return `SCHRITT 3 — WANN + BUSINESS-FENSTER.\nIntake: ${intakeStr}\nAufgaben mit Kategorien:\n${JSON.stringify(categories || [])}\n\nBaue aus den behalten/zusammenlegen-Aufgaben 2–3 feste Haushalts-Blöcke (Wochentag+Uhrzeit+Dauer). Identifiziere dann aus der freigewordenen Zeit ihr geschütztes Business-Fenster (entsprechend business_stunden_ziel), an eine ruhige Tageszeit gelegt, plus 1–2 Sätze wie sie es schützt. Schluss: warmer Abschluss + die offene Schleife (siehe Prompt).\nAntworte AUSSCHLIESSLICH mit gültigem JSON (keine Fences):\n{"schritt":3,"haushalts_bloecke":[{"tag":"...","zeit":"...","dauer":"...","inhalt":"..."}],"delegier_liste":["..."],"weg_liste":["..."],"business_fenster":{"tage":"...","zeit":"...","stunden":3,"schutz":"..."},"schluss":"<warmer Abschluss + offene Schleife>"}`;
}

function extractJson(text) {
  let t = text.trim();
  // Markdown-Fences entfernen falls doch vorhanden
  t = t.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/i, '').trim();
  const first = t.indexOf('{');
  const last = t.lastIndexOf('}');
  if (first !== -1 && last !== -1) t = t.slice(first, last + 1);
  return JSON.parse(t);
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  try {
    const { step, intake, tasks, categories } = req.body || {};
    if (![1, 2, 3].includes(step)) return res.status(400).json({ error: 'step 1|2|3 erforderlich' });

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) return res.status(500).json({ error: 'ANTHROPIC_API_KEY nicht gesetzt' });

    const systemPrompt = await loadSystemPrompt();
    const client = new Anthropic({ apiKey });

    async function call(attempt = 1) {
      try {
        return await client.messages.create({
          model: 'claude-sonnet-4-5',
          max_tokens: 3000,
          system: systemPrompt,
          messages: [{ role: 'user', content: stepInstruction(step, { intake, tasks, categories }) }],
        });
      } catch (err) {
        const transient = err.status >= 500 || err.status === 429 || err.name === 'APIConnectionError';
        if (transient && attempt < 2) { await new Promise((r) => setTimeout(r, 1500)); return call(attempt + 1); }
        throw err;
      }
    }

    const response = await call();
    const text = response.content.filter((b) => b.type === 'text').map((b) => b.text).join('\n').trim();

    let data;
    try { data = extractJson(text); }
    catch (e) {
      console.error('JSON-Parse fehlgeschlagen:', text.slice(0, 300));
      return res.status(502).json({ error: 'KI-Antwort war kein gültiges JSON', retryable: true });
    }

    console.log('generate OK', { step, in: response.usage?.input_tokens, out: response.usage?.output_tokens });
    return res.status(200).json(data);
  } catch (err) {
    console.error('generate error:', { name: err.name, message: err.message, status: err.status });
    const retryable = err.status >= 500 || err.status === 429 || err.name === 'APIConnectionError' || err.name === 'APITimeoutError';
    return res.status(retryable ? 503 : 500).json({ error: 'Hat nicht geklappt — bitte nochmal.', retryable });
  }
}
