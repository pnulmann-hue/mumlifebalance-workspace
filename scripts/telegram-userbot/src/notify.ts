/**
 * Sendet DM-Benachrichtigungen an Patricia via den normalen Bot (nicht Userbot).
 * Mit Inline-Buttons: Speichern / Skip / Mehr zeigen.
 */

const BOT_API = "https://api.telegram.org/bot";

interface NotifyParams {
  userId: number;
  chatTitle: string;
  senderName: string;
  category: string;
  summary: string;
  originalText: string;
  messageRef: string; // Referenz um später die Speichern-Aktion zu matchen
}

const categoryEmoji: Record<string, string> = {
  announcement: "📢",
  strategy: "💡",
  event: "📅",
  learning: "🎯",
  file: "📎",
  noise: "💬",
};

const categoryLabel: Record<string, string> = {
  announcement: "Ankündigung",
  strategy: "Strategie/Tipp",
  event: "Event",
  learning: "Learning",
  file: "Datei",
  noise: "Nachricht",
};

export async function sendImportantNotification(
  params: NotifyParams
): Promise<boolean> {
  const token = process.env.NOTIFICATION_BOT_TOKEN;
  if (!token) return false;

  const emoji = categoryEmoji[params.category] || "💬";
  const label = categoryLabel[params.category] || "Nachricht";

  // Kürze Original-Text wenn zu lang
  const preview =
    params.originalText.length > 500
      ? params.originalText.slice(0, 500) + "..."
      : params.originalText;

  const text = `${emoji} *${label}* in "${params.chatTitle}"

👤 ${params.senderName}

_${params.summary}_

─────────
${preview}`;

  try {
    const res = await fetch(`${BOT_API}${token}/sendMessage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: params.userId,
        text,
        parse_mode: "Markdown",
        disable_web_page_preview: true,
        reply_markup: {
          inline_keyboard: [
            [
              {
                text: "💾 Speichern",
                callback_data: `save:${params.messageRef}`,
              },
              {
                text: "❌ Skip",
                callback_data: `skip:${params.messageRef}`,
              },
            ],
          ],
        },
      }),
    });

    if (!res.ok) {
      const errBody = await res.text();
      console.error("Notification failed:", res.status, errBody);
      return false;
    }
    return true;
  } catch (err) {
    console.error("Notification error:", err);
    return false;
  }
}

/**
 * Sendet eine einfache Text-DM (ohne Buttons) — für Status-Infos.
 */
export async function sendPlainDM(
  userId: number,
  text: string
): Promise<boolean> {
  const token = process.env.NOTIFICATION_BOT_TOKEN;
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
