/**
 * Mail-Klassifikator: nutzt Claude um neue Mails zu kategorisieren.
 */

import Anthropic from "@anthropic-ai/sdk";

let _anthropic: Anthropic | null = null;
function anthropic(): Anthropic {
  if (!_anthropic) {
    _anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  }
  return _anthropic;
}

export type MailFolder =
  | "INBOX"
  | "INBOX/Wichtig"
  | "INBOX/Learnings"
  | "INBOX/Rechnungen"
  | "INBOX/Werbung"
  | "INBOX/Business"
  | "INBOX/Garteninfos"
  | "INBOX/Backen"
  | "INBOX/Kreuzfahrt"
  | "INBOX/Niklaus"
  | "INBOX/Kurszugänge"
  | "INBOX/Zeitschriften"
  | "Spam";

export interface MailClassification {
  targetFolder: MailFolder;
  markAsRead: boolean;
  notify: boolean;
  category: "wichtig" | "learning" | "rechnung" | "werbung" | "spam" | "info" | "ignored";
  summary: string;
  reasoning: string;
}

export interface MailContext {
  fromName?: string;
  fromAddress?: string;
  subject?: string;
  body?: string;
  date?: Date;
  hasAttachments?: boolean;
  mailbox: "GMX" | "Hoststar" | "Gmail";
}

const SYSTEM_PROMPT = `Du analysierst E-Mails fuer Patricia Ulmann ("Mum Life Balance", doTERRA Wellness Advocate, Mama, Solopreneurin).

ZIEL: Entscheide WOHIN die Mail soll, ob als gelesen markieren, ob Telegram-PUSH.

PATRICIAS BESTEHENDE ORDNER (bevorzugt verwenden wenn passend):
- INBOX/Business: Geschaeftliches, doTERRA, Kurse, Coaching, Kunden
- INBOX/Garteninfos: Garten/Permakultur Newsletter
- INBOX/Backen: Rezepte, Kochinspiration
- INBOX/Kreuzfahrt: Reise/Urlaub
- INBOX/Niklaus: Familien-/Klauserei-Sachen (Verein "Chläus")
- INBOX/Kurszugänge: Kursplattform-Notifications (nur Hoststar)
- INBOX/Zeitschriften: Zeitschriften (nur Hoststar)

STANDARD-KATEGORIEN:
- WICHTIG (bleibt INBOX, ungelesen, +PUSH):
  * Direkte Anfragen, Termine, eilige doTERRA, echte Kunden-Mails, Behoerden
- LEARNING (-> INBOX/Learnings, gelesen, kein PUSH):
  * Inspiration-Newsletter, Mentor-Mails (z.B. Julia Trost), Fachartikel
- RECHNUNGEN (-> INBOX/Rechnungen, gelesen):
  * Zahlungsbestaetigungen, Belege, Rechnungen (Cembra, Visa, Hoster)
- WERBUNG (-> INBOX/Werbung, gelesen):
  * Promo-Mails, Sales, Newsletter von Shops (Galaxus, Fleurop)
- SPAM (-> Spam-Ordner, gelesen):
  * Phishing, Lottery-Scams
- INFO (kein Move, gelesen):
  * Paket-Tracking, Standard-Bestaetigungen
- IGNORED (kein Move, kein Read-Flag):
  * Auto-Replies, System-Notifications

Regeln:
- Reine Newsletter NIE WICHTIG (max LEARNING/WERBUNG)
- noreply@/newsletter@/info@-Sender sind selten WICHTIG
- doTERRA (doterra.com/doterraservice) meist WICHTIG
- Persoenliche Anrede + Frage = WICHTIG

Antworte als reines JSON:
{
  "category": "wichtig"|"learning"|"rechnung"|"werbung"|"spam"|"info"|"ignored",
  "targetFolder": "INBOX"|"INBOX/Wichtig"|"INBOX/Learnings"|"INBOX/Rechnungen"|"INBOX/Werbung"|"INBOX/Business"|"INBOX/Garteninfos"|"INBOX/Backen"|"INBOX/Kreuzfahrt"|"INBOX/Niklaus"|"INBOX/Kurszugaenge"|"INBOX/Zeitschriften"|"Spam",
  "markAsRead": true|false,
  "notify": true|false,
  "summary": "1-2 Saetze auf Deutsch",
  "reasoning": "kurzer Grund"
}`;

export async function classifyMail(ctx: MailContext): Promise<MailClassification> {
  const body = (ctx.body || "").slice(0, 1500);
  const userMsg = `Mailbox: ${ctx.mailbox}
Von: ${ctx.fromName || "?"} <${ctx.fromAddress || "?"}>
Datum: ${ctx.date?.toISOString().slice(0, 16) || "?"}
Betreff: ${ctx.subject || "(kein Betreff)"}
Anhaenge: ${ctx.hasAttachments ? "ja" : "nein"}

Body (gekuerzt):
"""
${body}
"""`;

  try {
    const response = await anthropic().messages.create({
      model: "claude-haiku-4-5-20251001",
      max_tokens: 500,
      system: SYSTEM_PROMPT,
      messages: [{ role: "user", content: userMsg }],
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
      category: result.category || "ignored",
      targetFolder: (result.targetFolder as MailFolder) || "INBOX",
      markAsRead: Boolean(result.markAsRead),
      notify: Boolean(result.notify),
      summary: result.summary || "",
      reasoning: result.reasoning || "",
    };
  } catch (err) {
    console.error("Mail classification error:", err);
    return {
      category: "ignored",
      targetFolder: "INBOX",
      markAsRead: false,
      notify: false,
      summary: "",
      reasoning: "Fehler bei Klassifizierung",
    };
  }
}
