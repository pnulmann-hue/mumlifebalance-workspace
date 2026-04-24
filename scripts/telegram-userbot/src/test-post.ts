/**
 * Test-Script: versucht eine Nachricht in die Zielgruppe zu senden
 * und protokolliert jede Zwischenstufe, um PEER_ID_INVALID zu diagnostizieren.
 */

import { TelegramClient } from "telegram";
import { StringSession } from "telegram/sessions";
import * as dotenv from "dotenv";

dotenv.config();

const CHAT_ID = -1002221396127;
const DELETE_TEST = true;
const apiId = parseInt(process.env.TELEGRAM_API_ID || "");
const apiHash = process.env.TELEGRAM_API_HASH || "";
const sessionString = process.env.TELEGRAM_SESSION || "";

async function main() {
  const session = new StringSession(sessionString);
  const client = new TelegramClient(session, apiId, apiHash, { connectionRetries: 3 });
  await client.connect();
  console.log("✅ eingeloggt");

  // Dialogs laden zum cachen
  console.log("🔍 Lade Dialogs...");
  const dialogs = await client.getDialogs({ limit: 500 });
  console.log(`   ${dialogs.length} dialogs gecacht`);

  // Entity suchen
  console.log(`🔍 Suche Entity für ${CHAT_ID}...`);
  try {
    const entity = await client.getInputEntity(CHAT_ID);
    console.log("   ✅ Entity gefunden:", entity.className);

    // Sende Test-Nachricht
    console.log("📤 Sende Test-Nachricht...");
    await client.sendMessage(entity, {
      message: "🧪 Test-Nachricht vom Auto-Poster — wird gleich wieder gelöscht.",
    });
    console.log("   ✅ Gesendet!");
  } catch (err) {
    console.error("❌ Fehler:", err instanceof Error ? err.message : err);

    // Dialogs anzeigen wo die Gruppe auftaucht
    const target = dialogs.find((d) => d.id?.toString() === CHAT_ID.toString());
    if (target) {
      console.log("   Info aus Dialog:", { title: target.title, isGroup: target.isGroup, isChannel: target.isChannel });
    } else {
      console.log("   Chat nicht in Dialogs gefunden!");
    }
  }

  await client.disconnect();
  process.exit(0);
}

main().catch(console.error);
