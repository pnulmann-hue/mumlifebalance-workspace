/**
 * Mail-Poller: holt ungelesene Mails, klassifiziert + sortiert.
 * Wiederverwendbare Funktion fuer cron + manuellen Aufruf.
 */

import { ImapFlow, FetchMessageObject } from "imapflow";
import { simpleParser } from "mailparser";
import { classifyMail, MailContext, MailFolder } from "./mail-classifier";
import { sendMailDM, sendMailPlainDM } from "./mailassistant";

interface MailboxConfig {
  name: "GMX" | "Hoststar" | "Gmail";
  host: string;
  port: number;
  user: string;
  pass: string;
  secure: boolean;
}

function getMailboxConfigs(): MailboxConfig[] {
  return [
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
    {
      name: "Gmail",
      host: process.env.GMAIL_IMAP_HOST || "imap.gmail.com",
      port: parseInt(process.env.GMAIL_IMAP_PORT || "993"),
      user: process.env.GMAIL_IMAP_USER!,
      pass: process.env.GMAIL_IMAP_PASS!,
      secure: true,
    },
  ];
}

async function ensureFoldersExist(client: ImapFlow, mailbox: "GMX" | "Hoststar" | "Gmail"): Promise<void> {
  const required = ["INBOX/Wichtig", "INBOX/Learnings", "INBOX/Rechnungen", "INBOX/Werbung"];
  const existing = await client.list();
  const existingPaths = new Set(existing.map((f) => f.path));
  for (const path of required) {
    if (!existingPaths.has(path)) {
      try {
        await client.mailboxCreate(path);
        console.log(`   📁 [${mailbox}] Ordner erstellt: ${path}`);
      } catch (err) {
        console.warn(`   ⚠️ ${path}: ${err instanceof Error ? err.message : err}`);
      }
    }
  }
}

function resolveFolderName(target: MailFolder, mailbox: "GMX" | "Hoststar" | "Gmail"): string | null {
  if (target === "INBOX") return null;
  if (target === "Spam") {
    if (mailbox === "GMX") return "Spamverdacht";
    if (mailbox === "Gmail") return "[Gmail]/Spam";
    return "Junk-E-Mail";
  }
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

export interface SweepStats {
  total: number;
  classified: number;
  moved: number;
  pushed: number;
  errors: number;
  byCategory: Record<string, number>;
}

async function processMailbox(cfg: MailboxConfig, userId: number): Promise<SweepStats> {
  const stats: SweepStats = { total: 0, classified: 0, moved: 0, pushed: 0, errors: 0, byCategory: {} };

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
    if (!status.unseen || status.unseen === 0) {
      await client.logout();
      return stats;
    }

    console.log(`📧 [${cfg.name}] ${status.unseen} ungelesen von ${totalMessages}`);
    const range = `1:${totalMessages}`;
    const candidates: FetchMessageObject[] = [];
    for await (const m of client.fetch(range, { envelope: true, source: true, internalDate: true, flags: true, uid: true })) {
      if (!m.flags?.has("\\Seen")) candidates.push(m);
    }
    stats.total = candidates.length;

    for (const msg of candidates) {
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
        if (cls.markAsRead) {
          try { await client.messageFlagsAdd(String(msg.uid), ["\\Seen"], { uid: true }); } catch {}
        }
        if (folderName) {
          try { await client.messageMove(String(msg.uid), folderName, { uid: true }); stats.moved++; } catch {}
        }
        if (cls.notify && userId) {
          await sendMailDM(userId, {
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
        console.error(`  ❌ ${err instanceof Error ? err.message : err}`);
      }
    }
    await client.logout();
  } catch (err) {
    console.error(`❌ [${cfg.name}]`, err instanceof Error ? err.message : err);
  }
  return stats;
}

/**
 * Haupt-Funktion: läuft über beide Mailboxen, klassifiziert + sortiert.
 * @param userId  Patricia's Telegram User-ID für PUSH-DMs
 */
export async function runMailSweep(userId: number): Promise<void> {
  console.log(`📬 Mail-Sweep startet (${new Date().toLocaleString("de-CH")})`);

  const allStats: { name: string; stats: SweepStats }[] = [];
  for (const cfg of getMailboxConfigs()) {
    const stats = await processMailbox(cfg, userId);
    allStats.push({ name: cfg.name, stats });
  }

  const totals = {
    classified: allStats.reduce((s, x) => s + x.stats.classified, 0),
    moved: allStats.reduce((s, x) => s + x.stats.moved, 0),
    pushed: allStats.reduce((s, x) => s + x.stats.pushed, 0),
  };

  console.log(`✅ Mail-Sweep fertig: ${totals.classified} klassifiziert, ${totals.moved} verschoben, ${totals.pushed} PUSH`);

  if (userId && totals.classified > 0) {
    const summary = allStats
      .filter(({ stats }) => stats.classified > 0)
      .map(({ name, stats }) => {
        const cats = Object.entries(stats.byCategory).map(([k, v]) => `  ${k}: ${v}`).join("\n");
        return `*${name}:* ${stats.classified} verarbeitet, ${stats.moved} verschoben, ${stats.pushed} PUSH\n${cats}`;
      })
      .join("\n\n");
    await sendMailPlainDM(
      userId,
      `📧 *Mail-Sweep ${new Date().toLocaleDateString("de-CH")}*\n\n${summary}\n\nWichtige Mails wurden separat als DM versendet.`
    );
  } else if (userId && totals.classified === 0) {
    console.log("Keine neuen Mails — keine Zusammenfassungs-DM");
  }
}

/**
 * Soll der Mail-Sweep heute um diese Zeit laufen?
 * Trigger: 07:00-07:59
 */
export function isMailSweepTime(now: Date = new Date()): boolean {
  return now.getHours() === 7;
}
