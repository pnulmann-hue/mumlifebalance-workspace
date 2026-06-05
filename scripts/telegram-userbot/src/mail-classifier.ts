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
  | "INBOX/Buchhaltung"
  | "INBOX/Zu löschen"
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
  category: "wichtig" | "learning" | "rechnung" | "werbung" | "loeschen" | "spam" | "info" | "ignored";
  summary: string;
  reasoning: string;
  /**
   * Soll der Inhalt zusätzlich in einen Bot eingespeist werden?
   * "garten" → Notion-Wissensarchiv · "kochbot" → Rezept-RAG.
   * Nur setzen wenn die Mail SUBSTANZ hat (echter Garten-Tipp / echtes Rezept),
   * nicht bei reiner Werbung. null = keine Einspeisung.
   */
  feedTo: "garten" | "kochbot" | null;
  /**
   * Sauber extrahierter, einspeisbarer Inhalt (nur gesetzt wenn feedTo != null):
   * das eigentliche Rezept bzw. der Garten-Wissensinhalt, ohne Werbe-Ballast.
   */
  feedContent?: string;
  /** Kurzer Titel für den Bot-Eintrag (nur wenn feedTo != null). */
  feedTitle?: string;
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
  * Inspiration-Newsletter, Mentor-Mails, Fachartikel
- RECHNUNG (-> INBOX/Buchhaltung, gelesen):
  * Zahlungsbestaetigungen, Belege, Rechnungen, Quittungen (Cembra, Visa, Hoster, Stripe, Railway, PayPal)
  * ALLES was Buchhaltung/Steuern betrifft
- WERBUNG (-> INBOX/Zu löschen, gelesen):
  * Promo-Mails, Sales, Shop-Newsletter (Galaxus, Fleurop, Mode, Supplements)
- LOESCHEN (-> INBOX/Zu löschen, gelesen, NIE PUSH):
  * Automatische System-/Tool-Benachrichtigungen ohne bleibenden Wert:
    GitHub-Workflow-/CI-/Build-Mails, "Run failed", Notion-Login-Hinweise,
    App-Installations-Meldungen (Family Link), Deploy-Notifications
  * Alles was du bedenkenlos wegwerfen wuerdest, aber Patricia soll drueberschauen koennen
- SPAM (-> Spam-Ordner, gelesen):
  * Phishing, Lottery-Scams, klarer Betrug
- INFO (kein Move, gelesen):
  * Paket-Tracking, Standard-Bestaetigungen
- IGNORED (kein Move, kein Read-Flag):
  * Auto-Replies

Regeln:
- Reine Newsletter NIE WICHTIG (max LEARNING/WERBUNG)
- noreply@/newsletter@/info@-Sender sind selten WICHTIG
- doTERRA (doterra.com/doterraservice) meist WICHTIG
- Persoenliche Anrede + Frage = WICHTIG
- GitHub/CI/Workflow-Mails (notifications@github.com, "Run failed", "workflow run") IMMER LOESCHEN
- Rechnungen/Belege/Quittungen IMMER RECHNUNG -> INBOX/Buchhaltung

BOT-EINSPEISUNG (feedTo) — nur bei ECHTER Substanz:
- "kochbot": Mail enthaelt ein KONKRETES, nachkochbares Rezept (Zutaten + Zubereitung).
  Reine Rezept-WERBUNG ohne vollstaendiges Rezept => feedTo null lassen.
- "garten": Mail enthaelt konkretes Garten-/Permakultur-WISSEN (Anbau-Tipp, Pflege,
  Sorteninfo, Aussaat-Kalender). Reine Shop-Werbung fuer Gartenprodukte => feedTo null.
- Wenn feedTo gesetzt: feedContent = der SAUBER extrahierte Inhalt (nur das Rezept bzw.
  den Wissensteil, ohne Werbe-Ballast/Footer/Abmelde-Links), feedTitle = kurzer Titel.
- Sonst: feedTo null, feedContent/feedTitle weglassen.
- WICHTIG: Wenn feedTo="kochbot" gesetzt ist, gehoert die Mail in INBOX/Backen
  (nicht Werbung/Zu löschen). Wenn feedTo="garten", gehoert sie in INBOX/Garteninfos.
  Die wertvolle Mail mit echtem Inhalt wird so erhalten, nicht weggeworfen.

Antworte als reines JSON:
{
  "category": "wichtig"|"learning"|"rechnung"|"werbung"|"loeschen"|"spam"|"info"|"ignored",
  "targetFolder": "INBOX"|"INBOX/Wichtig"|"INBOX/Learnings"|"INBOX/Buchhaltung"|"INBOX/Zu löschen"|"INBOX/Werbung"|"INBOX/Business"|"INBOX/Garteninfos"|"INBOX/Backen"|"INBOX/Kreuzfahrt"|"INBOX/Niklaus"|"INBOX/Kurszugänge"|"INBOX/Zeitschriften"|"Spam",
  "markAsRead": true|false,
  "notify": true|false,
  "summary": "1-2 Saetze auf Deutsch",
  "reasoning": "kurzer Grund",
  "feedTo": "garten"|"kochbot"|null,
  "feedContent": "nur wenn feedTo gesetzt — sauber extrahierter Inhalt",
  "feedTitle": "nur wenn feedTo gesetzt — kurzer Titel"
}`;

/** Robuste JSON-Extraktion: Code-Fences weg + nur den {...}-Block nehmen. */
function extractJson(text: string): string {
  let t = text
    .replace(/^```json\s*/i, "")
    .replace(/^```\s*/, "")
    .replace(/\s*```$/, "")
    .trim();
  const first = t.indexOf("{");
  const last = t.lastIndexOf("}");
  if (first >= 0 && last > first) t = t.slice(first, last + 1);
  return t;
}

function toClassification(result: Record<string, unknown>): MailClassification {
  const feedTo = result.feedTo === "garten" || result.feedTo === "kochbot" ? result.feedTo : null;
  return {
    category: (result.category as MailClassification["category"]) || "ignored",
    targetFolder: (result.targetFolder as MailFolder) || "INBOX",
    markAsRead: Boolean(result.markAsRead),
    notify: Boolean(result.notify),
    summary: (result.summary as string) || "",
    reasoning: (result.reasoning as string) || "",
    feedTo,
    feedContent: feedTo ? String(result.feedContent || "").trim() || undefined : undefined,
    feedTitle: feedTo ? String(result.feedTitle || "").trim() || undefined : undefined,
  };
}

export async function classifyMail(ctx: MailContext): Promise<MailClassification> {
  const body = (ctx.body || "").slice(0, 1500);
  const baseMsg = `Mailbox: ${ctx.mailbox}
Von: ${ctx.fromName || "?"} <${ctx.fromAddress || "?"}>
Datum: ${ctx.date?.toISOString().slice(0, 16) || "?"}
Betreff: ${ctx.subject || "(kein Betreff)"}
Anhaenge: ${ctx.hasAttachments ? "ja" : "nein"}

Body (gekuerzt):
"""
${body}
"""`;

  const MAX_ATTEMPTS = 2;
  let lastErr: unknown = null;

  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
    const userMsg =
      attempt === 1
        ? baseMsg
        : `${baseMsg}\n\nWICHTIG: Antworte AUSSCHLIESSLICH mit einem einzigen validen JSON-Objekt. ` +
          `Alle Anfuehrungszeichen und Zeilenumbrueche INNERHALB von Strings muessen korrekt escaped sein (\\" und \\n). Kein Text davor/danach.`;
    try {
      const response = await anthropic().messages.create({
        model: "claude-haiku-4-5-20251001",
        max_tokens: 1500,
        system: SYSTEM_PROMPT,
        messages: [{ role: "user", content: userMsg }],
      });

      const content = response.content[0];
      if (content.type !== "text") throw new Error("Unexpected response");

      const result = JSON.parse(extractJson(content.text));
      return toClassification(result);
    } catch (err) {
      lastErr = err;
      if (attempt < MAX_ATTEMPTS) {
        console.warn(`  ⚠️ Klassifikation Versuch ${attempt} fehlgeschlagen (${err instanceof Error ? err.message : err}) — Retry`);
      }
    }
  }

  console.error("Mail classification error (nach Retries):", lastErr);
  return {
    category: "ignored",
    targetFolder: "INBOX",
    markAsRead: false,
    notify: false,
    summary: "",
    reasoning: "Fehler bei Klassifizierung",
    feedTo: null,
  };
}
