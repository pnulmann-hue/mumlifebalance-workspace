/**
 * Nachrichten-Klassifizierung via Claude Haiku.
 * Entscheidet ob eine Nachricht "wichtig" ist + gibt Zusammenfassung.
 */

import Anthropic from "@anthropic-ai/sdk";

let _anthropic: Anthropic | null = null;
function anthropic(): Anthropic {
  if (!_anthropic) {
    _anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  }
  return _anthropic;
}

export type Category =
  | "announcement"
  | "strategy"
  | "event"
  | "learning"
  | "noise"
  | "file";

export interface ClassificationResult {
  isImportant: boolean;
  category: Category;
  summary: string;
  reasoning: string;
}

export async function classifyMessage(
  text: string,
  chatTitle: string,
  senderName: string
): Promise<ClassificationResult> {
  const prompt = `Du analysierst eine Telegram-Nachricht aus einer doTERRA Business-Gruppe für Patricia, eine Network Marketing Unternehmerin ("Mum Life Balance").

Gruppe: "${chatTitle}"
Absender: "${senderName}"
Nachricht:
"""
${text}
"""

Entscheide ob WICHTIG für Patricia. Wichtig sind:
- Ankündigungen (neue Aktionen, Boni, Premier Club Start, Monatsaktionen)
- Strategien & Tipps (Business-Aufbau, Instagram, Positionierung, Verkauf, Teamaufbau)
- Events (neue Webinare, Calls, Schulungen)
- Learnings (Öl-Wissen, Produktinfos, wertvolle Takeaways)

NICHT wichtig: Small Talk, Begrüssungen, Danke-Nachrichten, Emoji-Reaktionen, banale Smalltalk-Fragen.

Antworte in reinem JSON (kein Markdown, kein Text drumherum):
{
  "isImportant": true|false,
  "category": "announcement"|"strategy"|"event"|"learning"|"noise"|"file",
  "summary": "1-2 Sätze Zusammenfassung auf Deutsch",
  "reasoning": "Kurzer Grund (ein Satz)"
}`;

  try {
    const response = await anthropic().messages.create({
      model: "claude-haiku-4-5-20251001",
      max_tokens: 400,
      messages: [{ role: "user", content: prompt }],
    });

    const content = response.content[0];
    if (content.type !== "text") throw new Error("Unexpected response");

    const jsonText = content.text
      .replace(/^```json\s*/i, "")
      .replace(/^```\s*/, "")
      .replace(/\s*```$/, "")
      .trim();

    const result = JSON.parse(jsonText);

    return {
      isImportant: Boolean(result.isImportant),
      category: (result.category as Category) || "noise",
      summary: result.summary || "",
      reasoning: result.reasoning || "",
    };
  } catch (err) {
    console.error("Classification error:", err);
    return {
      isImportant: false,
      category: "noise",
      summary: "",
      reasoning: "Fehler bei Klassifizierung",
    };
  }
}
