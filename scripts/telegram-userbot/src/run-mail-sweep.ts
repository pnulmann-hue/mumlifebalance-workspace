/**
 * Echter Mail-Lauf: holt alle ungelesenen Mails, klassifiziert,
 * markiert als gelesen und verschiebt in passende Ordner.
 *
 * Idempotenz via IMAP-Seen-Flag: nach diesem Lauf sind alle Mails als gelesen
 * markiert + ggf. verschoben — ein zweiter Lauf findet sie nicht mehr.
 *
 * WICHTIGE Mails: Telegram-DM an Patricia via Mailassistant-Bot.
 *
 * Run: npx tsx src/run-mail-sweep.ts
 */

import * as dotenv from "dotenv";
dotenv.config({ override: true });

import { ImapFlow, FetchMessageObject } from "imapflow";
import { simpleParser } from "mailparser";
import { classifyMail, MailContext, MailFolder } from "./mail-classifier";
import { sendMailDM, sendMailPlainDM } from "./mailassistant";

interface MailboxConfig {
  name: "GMX" | "Hoststar";
  host: string;
  port: number;
  user: string;
  pass: string;
  secure: boolean;
}

const MAILBOX_CONFIGS: MailboxConfig[] = [
  {
    name: "GMX",
    host: process.env.GMX_IMAP_HOST!,
    port: parseInt(process.env.GMX_IMAP_PORT || "993"),
    user: process.env.GMX_IMAP_USER!,
    pass: process.env.GMX_IMAP_PASS!,
    secure: true,
  },
  {
    name: "Hoststar",
    host: process.env.HOSTSTAR_IMAP_HOST!,
    port: parseInt(process.env.HOSTSTAR_IMAP_PORT || "143"),
    user: process.env.HOSTSTAR_IMAP_USER!,
    pass: process.env.HOSTSTAR_IMAP_PASS!,
    secure: false,
  },
];

const PATRICIA_USER_ID = parseInt(process.env.PATRICIA_TELEGRAM_USER_ID || "0");

async function ensureFoldersExist(client: ImapFlow, mailbox: "GMX" | "Hoststar"): Promise<void> {
  const required = ["INBOX/Wichtig", "INBOX/Learnings", "INBOX/Rechnungen", "INBOX/Werbung"];
  const existing = await client.list();
  const existingPaths = new Set(existing.map((f) => f.path));

  for (const path of required) {
    if (!existingPaths.has(path)) {
      try {
        await client.mailboxCreate(path);
        console.log(`   📁 [${mailbox}] Ordner erstellt: ${path}`);
      } catch (err) {
        console.warn(`   ⚠️ Ordner ${path} konnte nicht erstellt werden: ${err instanceof Error ? err.message : err}`);
      }
    }
  }
}

function resolveFolderName(target: MailFolder, mailbox: "GMX" | "Hoststar"): string | null {
  if (target === "INBOX") return null;
  if (target === "Spam") return mailbox === "GMX" ? "Spamverdacht" : "Junk-E-Mail";
  return target;
}

async function getBody(message: FetchMessageObject) {
  if (!message.source) return { text: "", hasAttachments: false };
  try {
    const parsed = await simpleParser(message.source);
    const text = (parsed.text || (parsed.html ? String(parsed.html).replace(/<[^>]+>/g, " ") : "")).toString();
    return { text, hasAttachments: (parsed.attachments?.length || 0) > 0 };
  } catch {
    return { text: "", hasAttachments: false };
  }
}

interface RunStats {
  total: number;
  classified: number;
  moved: number;
  pushed: number;
  errors: number;
  byCategory: Record<string, number>;
}

async function processMailbox(cfg: MailboxConfig): Promise<RunStats> {
  const stats: RunStats = {
    total: 0,
    classified: 0,
    moved: 0,
    pushed: 0,
    errors: 0,
    byCategory: {},
  };

  console.log(`\n${"=".repeat(70)}`);
  console.log(`📧 ECHTER LAUF: ${cfg.name}`);
  console.log("=".repeat(70));

  const client = new ImapFlow({
    host: cfg.host,
    port: cfg.port,
    secure: cfg.secure,
    auth: { user: cfg.user, pass: cfg.pass },
    logger: false,
  });

  try {
    await client.connect();
    await ensureFoldersExist(client, cfg.name);
    await client.mailboxOpen("INBOX");

    const status = await client.status("INBOX", { messages: true, unseen: true });
    const totalMessages = status.messages || 0;
    const unseenCount = status.unseen || 0;

    if (unseenCount === 0) {
      console.log("Keine ungelesenen Mails.");
      await client.logout();
      return stats;
    }

    console.log(`INBOX: ${totalMessages} total, ${unseenCount} ungelesen`);

    // Hole alle Mails (Sequence-Range), filter dann ungelesene
    const range = `1:${totalMessages}`;
    const candidates: FetchMessageObject[] = [];
    for await (const m of client.fetch(range, { envelope: true, source: true, internalDate: true, flags: true, uid: true })) {
      if (!m.flags?.has("\\Seen")) {
        candidates.push(m);
      }
    }

    console.log(`Verarbeite ${candidates.length} ungelesene Mails...\n`);
    stats.total = candidates.length;

    let i = 0;
    for (const msg of candidates) {
      i++;
      try {
        const { text, hasAttachments } = await getBody(msg);
        const ctx: MailContext = {
          fromName: msg.envelope?.from?.[0]?.name,
          fromAddress: msg.envelope?.from?.[0]?.address,
          subject: msg.envelope?.subject,
          body: text,
          date: msg.envelope?.date ? new Date(msg.envelope.date) : (msg.internalDate ? new Date(msg.internalDate) : undefined),
          hasAttachments,
          mailbox: cfg.name,
        };

        const cls = await classifyMail(ctx);
        stats.classified++;
        stats.byCategory[cls.category] = (stats.byCategory[cls.category] || 0) + 1;

        const folderName = resolveFolderName(cls.targetFolder, cfg.name);

        const fromShort = (ctx.fromAddress || "?").slice(0, 30);
        const subjShort = (ctx.subject || "").slice(0, 50);
        console.log(`[${i}/${stats.total}] ${cls.category.toUpperCase().padEnd(10)} | ${fromShort.padEnd(30)} | ${subjShort}`);

        // Mark as read
        if (cls.markAsRead) {
          try {
            await client.messageFlagsAdd(String(msg.uid), ["\\Seen"], { uid: true });
          } catch (e) {
            console.warn(`     ⚠ markAsRead failed: ${e instanceof Error ? e.message : e}`);
          }
        }

        // Move
        if (folderName) {
          try {
            await client.messageMove(String(msg.uid), folderName, { uid: true });
            stats.moved++;
          } catch (e) {
            console.warn(`     ⚠ move to ${folderName} failed: ${e instanceof Error ? e.message : e}`);
          }
        }

        // PUSH
        if (cls.notify && PATRICIA_USER_ID) {
          await sendMailDM(PATRICIA_USER_ID, {
            fromAddress: ctx.fromAddress,
            fromName: ctx.fromName,
            subject: ctx.subject,
            date: ctx.date,
            category: cls.category,
            summary: cls.summary,
            targetFolder: cls.targetFolder,
            mailbox: cfg.name,
          });
          stats.pushed++;
        }
      } catch (err) {
        stats.errors++;
        console.error(`  ❌ uid=${msg.uid}: ${err instanceof Error ? err.message : err}`);
      }
    }

    await client.logout();
  } catch (err) {
    console.error(`❌ [${cfg.name}] Fehler:`, err instanceof Error ? err.message : err);
  }

  return stats;
}

async function main() {
  console.log("🚀 Mail-Sweep startet — echter Lauf mit Move + Read-Flag\n");
  const allStats: { name: string; stats: RunStats }[] = [];

  for (const cfg of MAILBOX_CONFIGS) {
    const stats = await processMailbox(cfg);
    allStats.push({ name: cfg.name, stats });
  }

  console.log(`\n${"=".repeat(70)}`);
  console.log("📊 ZUSAMMENFASSUNG");
  console.log("=".repeat(70));
  for (const { name, stats } of allStats) {
    console.log(`\n${name}:`);
    console.log(`  Klassifiziert: ${stats.classified}/${stats.total}`);
    console.log(`  Verschoben:    ${stats.moved}`);
    console.log(`  PUSH-DMs:      ${stats.pushed}`);
    console.log(`  Fehler:        ${stats.errors}`);
    console.log(`  Nach Kategorie:`, stats.byCategory);
  }

  // Final-DM an Patricia
  if (PATRICIA_USER_ID) {
    const summary = allStats
      .map(({ name, stats }) => {
        const cats = Object.entries(stats.byCategory)
          .map(([k, v]) => `  ${k}: ${v}`)
          .join("\n");
        return `*${name}:* ${stats.classified} verarbeitet, ${stats.moved} verschoben, ${stats.pushed} PUSH\n${cats}`;
      })
      .join("\n\n");

    await sendMailPlainDM(
      PATRICIA_USER_ID,
      `📧 *Mail-Sweep abgeschlossen*\n\n${summary}\n\nWichtige Mails wurden separat als DM versendet.`
    );
  }

  console.log("\n✅ Fertig.");
}

main().catch(console.error);
