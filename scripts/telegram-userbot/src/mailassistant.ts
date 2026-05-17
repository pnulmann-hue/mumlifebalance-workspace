/**
 * Mailassistant-Bot: separater Telegram-Bot fuer Mail-Notifications.
 * Token: MAILASSISTANT_BOT_TOKEN in .env
 *
 * Sendet PUSH-DMs an Patricia bei wichtigen Mails.
 */

const BOT_API = "https://api.telegram.org/bot";

interface MailNotification {
  fromAddress?: string;
  fromName?: string;
  subject?: string;
  date?: Date;
  category: string;
  summary: string;
  targetFolder: string;
  mailbox: "GMX" | "Hoststar" | "Gmail";
}

const categoryEmoji: Record<string, string> = {
  wichtig: "🚨",
  rechnung: "🧾",
  learning: "💡",
  werbung: "📢",
  spam: "🚫",
  info: "ℹ️",
  ignored: "🤐",
};

export async function sendMailDM(userId: number, mail: MailNotification): Promise<boolean> {
  const token = process.env.MAILASSISTANT_BOT_TOKEN;
  if (!token) {
    console.error("MAILASSISTANT_BOT_TOKEN nicht gesetzt");
    return false;
  }

  const emoji = categoryEmoji[mail.category] || "📧";
  const sender = mail.fromName ? `${mail.fromName} <${mail.fromAddress}>` : mail.fromAddress || "?";
  const dateStr = mail.date?.toLocaleString("de-CH", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }) || "?";

  const text = `${emoji} *${mail.category.toUpperCase()}* — ${mail.mailbox}

📨 *${escapeMd(mail.subject || "(kein Betreff)")}*
👤 ${escapeMd(sender)}
🕒 ${dateStr}

${escapeMd(mail.summary)}

📁 Verschoben nach: \`${mail.targetFolder}\``;

  try {
    const res = await fetch(`${BOT_API}${token}/sendMessage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: userId,
        text,
        parse_mode: "Markdown",
        disable_web_page_preview: true,
      }),
    });
    return res.ok;
  } catch (err) {
    console.error("Mailassistant sendMailDM error:", err);
    return false;
  }
}

export async function sendMailPlainDM(userId: number, text: string): Promise<boolean> {
  const token = process.env.MAILASSISTANT_BOT_TOKEN;
  if (!token) return false;
  try {
    const res = await fetch(`${BOT_API}${token}/sendMessage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: userId,
        text,
        parse_mode: "Markdown",
        disable_web_page_preview: true,
      }),
    });
    return res.ok;
  } catch {
    return false;
  }
}

function escapeMd(s: string): string {
  return String(s || "").replace(/([_*`[\]])/g, "\\$1");
}
