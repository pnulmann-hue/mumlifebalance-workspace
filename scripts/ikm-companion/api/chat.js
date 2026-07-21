/* =============================================================
   Vercel API Route: /api/chat
   =============================================================
   Proxy fuer Claude API. Nimmt messages[] entgegen, haengt
   System-Prompt davor, ruft Anthropic API, liefert Text zurueck.

   Generischer Kurs-Companion-Bot — wird vom /assistent-Skill
   pro Kurs aus dem Template erzeugt.

   Environment:
   - ANTHROPIC_API_KEY (Pflicht)

   Request:
   POST /api/chat
   Body: { messages: [{role, content}], user: {name, email} }

   Response:
   { text: string, meta: { stop_reason } }
   ============================================================= */

import Anthropic from '@anthropic-ai/sdk';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';

export const config = {
  runtime: 'nodejs',
  maxDuration: 60,
};

let systemPromptCache = null;

async function loadSystemPrompt() {
  if (systemPromptCache) return systemPromptCache;

  const candidates = [
    join(process.cwd(), 'lib', 'system-prompt.md'),
  ];

  for (const path of candidates) {
    try {
      const content = await readFile(path, 'utf-8');
      systemPromptCache = content;
      return content;
    } catch {
      // try next
    }
  }
  throw new Error('system-prompt.md nicht gefunden — pruefe den Pfad im Deploy');
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { messages = [], user = {} } = req.body || {};

    if (!Array.isArray(messages) || messages.length === 0) {
      return res.status(400).json({ error: 'messages required' });
    }

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) {
      return res.status(500).json({ error: 'ANTHROPIC_API_KEY nicht gesetzt' });
    }

    const systemPrompt = await loadSystemPrompt();
    const userContext = `\n\n---\n**User-Kontext:**\n- Name: ${user.name || '(unbekannt)'}\n- E-Mail: ${user.email || '(nicht uebergeben)'}\n\nSprich sie persoenlich an, wenn du den Vornamen hast.`;

    const client = new Anthropic({ apiKey });

    // Retry-Logic: Bei transientem Anthropic-Fehler (5xx, overload, network)
    // einmal automatisch nochmal probieren mit kurzem Backoff
    async function callAnthropic(attempt = 1) {
      try {
        return await client.messages.create({
          model: 'claude-sonnet-4-5',
          max_tokens: 8000,
          system: systemPrompt + userContext,
          messages: messages.map((m) => ({
            role: m.role === 'assistant' ? 'assistant' : 'user',
            content: m.content,
          })),
        });
      } catch (err) {
        const transient = err.status >= 500 || err.status === 429 || err.name === 'APIConnectionError';
        if (transient && attempt < 2) {
          await new Promise((r) => setTimeout(r, 1500));
          return callAnthropic(attempt + 1);
        }
        throw err;
      }
    }

    const response = await callAnthropic();

    const text = response.content
      .filter((block) => block.type === 'text')
      .map((block) => block.text)
      .join('\n')
      .trim();

    // Telemetry: Token-Verbrauch loggen
    const usage = response.usage || {};
    console.log('Chat OK:', {
      input: usage.input_tokens,
      output: usage.output_tokens,
      stop_reason: response.stop_reason,
      messages_count: messages.length,
    });

    if (response.stop_reason === 'max_tokens') {
      console.warn('max_tokens reached — Output abgeschnitten', usage);
    }
    if ((usage.input_tokens || 0) > 150000) {
      console.warn('Input-Tokens > 150k — Conversation wird gross', usage);
    }

    return res.status(200).json({
      text,
      meta: {
        retryable: false,
        stop_reason: response.stop_reason,
      },
    });
  } catch (err) {
    console.error('Chat error (full):', {
      name: err.name,
      message: err.message,
      status: err.status,
      type: err.error?.type,
      stack: err.stack?.split('\n').slice(0, 5).join('\n'),
    });

    const retryable =
      err.status >= 500 ||
      err.status === 429 ||
      err.name === 'APIConnectionError' ||
      err.name === 'APITimeoutError';

    return res.status(retryable ? 503 : 500).json({
      error: 'Bot-Antwort hat nicht geklappt — bitte nochmal probieren.',
      type: err.name || 'Error',
      retryable,
    });
  }
}
