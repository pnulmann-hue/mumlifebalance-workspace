/**
 * Patricia's Telegram Userbot — hört in allen Gruppen mit und benachrichtigt
 * über wichtige Nachrichten via DM mit Inline-Buttons.
 */

import { TelegramClient, Api } from "telegram";
import { StringSession } from "telegram/sessions";
import { NewMessage, NewMessageEvent } from "telegram/events";
import * as dotenv from "dotenv";
import { createClient } from "@supabase/supabase-js";

import { classifyMessage } from "./classifier";
import { trackMessage } from "./knowledge";
import { sendImportantNotification, sendPlainDM } from "./notify";
import {
  checkAllReminders,
  isTeamcallReminderToday,
  getSeasonReminderToday,
  isMonthlyNewsletterReminderToday,
} from "./reminders";
import { processPendingPosts } from "./auto-poster";

dotenv.config();

const apiId = parseInt(process.env.TELEGRAM_API_ID || "");
const apiHash = process.env.TELEGRAM_API_HASH || "";
const sessionString = process.env.TELEGRAM_SESSION || "";
const patriciaUserId = parseInt(process.env.PATRICIA_TELEGRAM_USER_ID || "0");

if (!apiId || !apiHash) {
  console.error("❌ TELEGRAM_API_ID oder TELEGRAM_API_HASH fehlt");
  process.exit(1);
}

if (!sessionString) {
  console.error("❌ TELEGRAM_SESSION fehlt. Führe zuerst 'npm run login' aus.");
  process.exit(1);
}

if (!patriciaUserId) {
  console.error("❌ PATRICIA_TELEGRAM_USER_ID fehlt. Führe zuerst 'npm run login' aus.");
  process.exit(1);
}

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

// Whitelist: welche Gruppen werden monitort?
// Leer = alle. Wird dynamisch aus Supabase geladen.
let monitoredChatIds: Set<string> = new Set();

async function loadMonitoredChats() {
  const { data } = await supabase
    .from("telegram_monitored_chats")
    .select("telegram_chat_id")
    .eq("enabled", true);

  monitoredChatIds = new Set(
    (data || []).map((r) => String(r.telegram_chat_id))
  );

  console.log(
    `📋 Whitelist geladen: ${monitoredChatIds.size} Chats${
      monitoredChatIds.size === 0 ? " (Fallback: alle Gruppen)" : ""
    }`
  );
}

async function handleMessage(event: NewMessageEvent) {
  const message = event.message;

  // Nur Gruppen/Channels, keine privaten Chats
  if (!message.isGroup && !message.isChannel) return;

  // Nur Text-Nachrichten (Dateien kommen später)
  const text = message.text?.trim();
  if (!text || text.length < 15) return;

  // Ignoriere Commands
  if (text.startsWith("/")) return;

  const chatId = message.chatId?.toString();
  if (!chatId) return;

  // Whitelist-Check (wenn Whitelist leer = alle erlaubt)
  if (monitoredChatIds.size > 0 && !monitoredChatIds.has(chatId)) {
    return;
  }

  // Hole Chat-Info und Absender
  const chat = await message.getChat();
  const sender = await message.getSender();

  const chatTitle =
    (chat as unknown as { title?: string; firstName?: string })?.title ||
    (chat as unknown as { title?: string; firstName?: string })?.firstName ||
    "Unbekannte Gruppe";
  const senderName = sender
    ? `${(sender as unknown as { firstName?: string }).firstName || ""} ${
        (sender as unknown as { lastName?: string }).lastName || ""
      }`.trim() || "Unbekannt"
    : "Unbekannt";

  console.log(`📨 [${chatTitle}] ${senderName}: ${text.slice(0, 80)}...`);

  // Klassifizieren mit Claude
  const classification = await classifyMessage(text, chatTitle, senderName);

  console.log(
    `   → ${classification.isImportant ? "✅ WICHTIG" : "⏭️ skip"} (${classification.category}): ${classification.reasoning}`
  );

  // Tracke alle wichtigen Nachrichten in DB
  if (classification.isImportant) {
    const msgDate = new Date((message.date || Date.now() / 1000) * 1000);

    await trackMessage({
      chatId: Number(chatId),
      chatTitle,
      messageId: message.id,
      senderName,
      text,
      date: msgDate,
      isImportant: true,
      category: classification.category,
      summary: classification.summary,
      hasFiles: false,
    });

    // Sende DM mit Inline-Buttons
    // messageRef = chatId:messageId (zum späteren Matchen beim Speichern-Klick)
    const messageRef = `${chatId}_${message.id}`;

    const sent = await sendImportantNotification({
      userId: patriciaUserId,
      chatTitle,
      senderName,
      category: classification.category,
      summary: classification.summary,
      originalText: text,
      messageRef,
    });

    if (sent) {
      console.log(`   📬 DM gesendet`);
    } else {
      console.log(`   ⚠️ DM-Versand fehlgeschlagen`);
    }
  }
}

async function handlePrivateCommand(event: NewMessageEvent) {
  const message = event.message;

  // Nur private Chats mit Patricia selbst
  if (message.isGroup || message.isChannel) return;

  const sender = await message.getSender();
  const senderId = Number(
    (sender as unknown as { id?: unknown })?.id?.toString() || "0"
  );
  if (senderId !== patriciaUserId) return;

  const text = message.text?.trim();
  if (!text) return;

  if (text.startsWith("/add_chat")) {
    // Patricia muss das Command aus der Gruppe forwarden die sie adden will
    // Oder: zeigt Liste ihrer Gruppen zum Auswählen
    await sendPlainDM(
      patriciaUserId,
      "Um eine Gruppe zu monitoren:\n1. Forward eine Nachricht aus der Gruppe an mich\n2. Oder nutze /list_chats um deine aktuellen Gruppen zu sehen"
    );
  } else if (text.startsWith("/list_chats")) {
    const { data } = await supabase
      .from("telegram_monitored_chats")
      .select("telegram_chat_id, chat_title, enabled");

    const list = (data || [])
      .map(
        (c) =>
          `${c.enabled ? "✅" : "⏸️"} ${c.chat_title} (${c.telegram_chat_id})`
      )
      .join("\n");

    await sendPlainDM(
      patriciaUserId,
      `*Monitored Chats:*\n${list || "(Keine — alle Gruppen werden überwacht)"}`
    );
  } else if (text.startsWith("/status")) {
    await sendPlainDM(
      patriciaUserId,
      `✅ Userbot läuft\n📋 Monitored chats: ${monitoredChatIds.size || "alle"}`
    );
  }

  // Forward-Handling: wenn eine Nachricht forwarded wurde, füge den Chat hinzu
  if (message.fwdFrom) {
    const fwdChatId = message.fwdFrom.fromId as unknown as { channelId?: { toString(): string }; chatId?: { toString(): string }; userId?: { toString(): string } } | undefined;
    const chatIdStr =
      fwdChatId?.channelId?.toString() ||
      fwdChatId?.chatId?.toString() ||
      fwdChatId?.userId?.toString();

    if (chatIdStr) {
      await supabase
        .from("telegram_monitored_chats")
        .upsert(
          {
            telegram_chat_id: Number(chatIdStr),
            chat_title: "(aus Forward — ändere mich im Supabase)",
            enabled: true,
          },
          { onConflict: "telegram_chat_id" }
        );

      await loadMonitoredChats();
      await sendPlainDM(
        patriciaUserId,
        `✅ Chat ${chatIdStr} hinzugefügt zur Whitelist`
      );
    }
  }
}

async function main() {
  console.log("🚀 Telegram Userbot startet...\n");

  const session = new StringSession(sessionString);
  const client = new TelegramClient(session, apiId, apiHash, {
    connectionRetries: 5,
  });

  await client.connect();

  const me = await client.getMe();
  console.log(`✅ Eingeloggt als ${(me as unknown as { firstName?: string }).firstName} (ID: ${me.id.toString()})\n`);

  await loadMonitoredChats();

  // Listener für neue Nachrichten
  client.addEventHandler(async (event: NewMessageEvent) => {
    try {
      await handleMessage(event);
      await handlePrivateCommand(event);
    } catch (err) {
      console.error("Event handler error:", err);
    }
  }, new NewMessage({}));

  console.log("👂 Höre auf neue Nachrichten...\n");
  console.log("Befehle (in privatem Chat mit dem Notification-Bot):");
  console.log("  /status       — Status prüfen");
  console.log("  /list_chats   — Whitelist anzeigen");
  console.log("  /add_chat     — Chat hinzufügen (forward Nachricht)");
  console.log("");
  const now = new Date();
  const season = getSeasonReminderToday(now);
  console.log(`📅 Reminder-Status heute:
    - Teamcall: ${isTeamcallReminderToday(now) ? "JA" : "nein"}
    - Saison: ${season ? season.name : "nein"}
    - Monatsaktionen/Newsletter: ${isMonthlyNewsletterReminderToday(now) ? "JA" : "nein"}`);

  // Alle Reminder: prüfe täglich um 9:00 Uhr
  let lastReminderCheck = "";
  setInterval(async () => {
    const n = new Date();
    const today = n.toISOString().slice(0, 10);
    if (n.getHours() >= 9 && lastReminderCheck !== today) {
      lastReminderCheck = today;
      try {
        await checkAllReminders(patriciaUserId);
      } catch (err) {
        console.error("Reminder check error:", err);
      }
    }
  }, 60 * 60 * 1000); // jede Stunde prüfen

  // Auto-Poster: prüft stündlich fällige Posts und postet sie
  console.log("📤 Auto-Poster aktiv (stündliche Prüfung)");
  setInterval(async () => {
    try {
      await processPendingPosts(client, patriciaUserId);
    } catch (err) {
      console.error("Auto-Poster error:", err);
    }
  }, 60 * 60 * 1000); // stündlich
  // Direkt einmal nach Start laufen lassen (nach 30s, damit Initialisierung fertig ist)
  setTimeout(() => processPendingPosts(client, patriciaUserId).catch(() => {}), 30_000);

  // Halte den Prozess am Leben
  await new Promise(() => {});
}

main().catch((err) => {
  console.error("❌ Fatal error:", err);
  process.exit(1);
});
