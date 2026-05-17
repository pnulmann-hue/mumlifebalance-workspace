/**
 * Dry-Run-Test: holt 10 ungelesene Mails pro Mailbox,
 * klassifiziert sie, aber verschiebt/markiert NICHTS.
 *
 * Run: npx tsx src/test-mail-dryrun.ts
 */

import * as dotenv from "dotenv";
dotenv.config({ override: true });
import { ImapFlow, FetchMessageObject } from "imapflow";
import { simpleParser } from "mailparser";
import { classifyMail, MailContext } from "./mail-classifier";

const LIMIT = 10;

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

async function dryRunMailbox(cfg: MailboxConfig): Promise<void> {
  console.log(`\n${"=".repeat(70)}`);
  console.log(`📧 DRY-RUN: ${cfg.name}`);
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
    await client.mailboxOpen("INBOX");

    const status = await client.status("INBOX", { messages: true, unseen: true });
    const totalMessages = status.messages || 0;
    if (totalMessages === 0) {
      console.log("INBOX ist leer.");
      return;
    }
    console.log(`INBOX: ${totalMessages} total, ${status.unseen || 0} ungelesen`);
    console.log(`Hole ${LIMIT} neueste Mails (Sequence-IDs)...\n`);

    // Hole die letzten N Mails per Sequence-ID
    const startSeq = Math.max(1, totalMessages - LIMIT + 1);
    const range = `${startSeq}:${totalMessages}`;
    const msgs: FetchMessageObject[] = [];
    for await (const m of client.fetch(range, { envelope: true, source: true, internalDate: true, flags: true })) {
      msgs.push(m);
    }
    // Sortiere absteigend nach Datum
    msgs.sort((a, b) => {
      const da = a.envelope?.date ? new Date(a.envelope.date).getTime() : 0;
      const db = b.envelope?.date ? new Date(b.envelope.date).getTime() : 0;
      return db - da;
    });

    let i = 0;
    {
      for (const msg of msgs) {
        i++;

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

        const dateStr = ctx.date?.toISOString().slice(5, 16).replace("T", " ") || "?";
        const fromShort = (ctx.fromAddress || "?").slice(0, 35);
        const subjShort = (ctx.subject || "(kein Betreff)").slice(0, 50);
        const moveStr = cls.targetFolder === "INBOX" ? "(bleibt INBOX)" : `→ ${cls.targetFolder}`;
        const flags = `${cls.markAsRead ? "✓gelesen " : ""}${cls.notify ? "📬PUSH" : ""}`.trim();

        const seenFlag = msg.flags?.has("\\Seen") ? "✓gelesen" : "🆕ungelesen";
        console.log(`[${i}] ${dateStr} | ${seenFlag} | ${fromShort.padEnd(35)} | ${subjShort}`);
        console.log(`    🏷️  ${cls.category.toUpperCase()} ${moveStr} ${flags}`);
        console.log(`    💭 ${cls.reasoning}`);
        console.log();
      }
    }
  } catch (err) {
    console.error(`❌ Fehler:`, err instanceof Error ? err.message : err);
  } finally {
    try {
      await client.logout();
    } catch {}
  }
}

async function main() {
  console.log("🔍 Mail-Dry-Run (kein Move, keine Read-Flags, kein DB-Insert)");
  for (const cfg of MAILBOX_CONFIGS) {
    await dryRunMailbox(cfg);
  }
  console.log(`\n${"=".repeat(70)}`);
  console.log("Dry-Run fertig.");
}

main().catch(console.error);
