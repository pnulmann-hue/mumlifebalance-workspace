/**
 * Einmaliger Poster-Lauf für GitHub Actions.
 *
 * Verbindet die Userbot-Session, postet alle fälligen scheduled_posts
 * (status='scheduled' && scheduled_for <= now) via processPendingPosts und
 * beendet sich. Wird stündlich vom Workflow .github/workflows/telegram-poster.yml
 * aufgerufen — ersetzt den (kaputten) Railway-Dauer-Worker fürs Auto-Posting.
 */

import "dotenv/config";
import { TelegramClient } from "telegram";
import { StringSession } from "telegram/sessions";
import { processPendingPosts } from "./auto-poster";

async function main() {
  const apiId = parseInt(process.env.TELEGRAM_API_ID || "", 10);
  const apiHash = process.env.TELEGRAM_API_HASH || "";
  const sessionString = process.env.TELEGRAM_SESSION || "";
  const userId = parseInt(
    process.env.PATRICIA_TELEGRAM_USER_ID || process.env.TELEGRAM_ADMIN_USER_ID || "0",
    10
  );

  if (!apiId || !apiHash || !sessionString) {
    console.error("❌ Fehlende Telegram-Credentials (API_ID / API_HASH / SESSION)");
    process.exit(1);
  }

  const client = new TelegramClient(new StringSession(sessionString), apiId, apiHash, {
    connectionRetries: 3,
  });
  await client.connect();
  console.log("✅ Userbot verbunden");

  // Dialoge laden → cached alle Gruppen/Channel-Entities (verhindert PEER_ID_INVALID)
  await client.getDialogs({ limit: 300 });

  await processPendingPosts(client, userId);
  console.log("✅ Poster-Lauf abgeschlossen");

  await client.disconnect();
  process.exit(0);
}

main().catch((e) => {
  console.error("❌ Poster-Fehler:", e);
  process.exit(1);
});
