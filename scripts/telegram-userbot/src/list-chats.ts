/**
 * Einmaliges Helper-Script: Listet alle Gruppen/Channels auf in denen Patricia Mitglied ist.
 * Nutzt die Userbot-Session um via Telegram API alle Dialoge abzufragen.
 */

import { TelegramClient } from "telegram";
import { StringSession } from "telegram/sessions";
import * as dotenv from "dotenv";

dotenv.config();

const apiId = parseInt(process.env.TELEGRAM_API_ID || "");
const apiHash = process.env.TELEGRAM_API_HASH || "";
const sessionString = process.env.TELEGRAM_SESSION || "";

async function main() {
  const session = new StringSession(sessionString);
  const client = new TelegramClient(session, apiId, apiHash, {
    connectionRetries: 3,
  });
  await client.connect();

  console.log("📋 Deine Gruppen & Channels:\n");

  const dialogs = await client.getDialogs({ limit: 200 });
  const groups = dialogs.filter(
    (d) => d.isGroup || d.isChannel
  );

  // Sortiere so dass "gesund" etc. oben
  const priority = (title: string) => {
    const t = title.toLowerCase();
    if (t.includes("gesund") || t.includes("ganze jahr") || t.includes("öl")) return 0;
    return 1;
  };
  groups.sort((a, b) => priority(a.title || "") - priority(b.title || ""));

  for (const d of groups) {
    const id = d.id?.toString() || "?";
    const title = d.title || "(ohne Titel)";
    const type = d.isChannel ? "📢 Channel" : "👥 Gruppe";
    console.log(`${type}  ID: ${id}  — ${title}`);
  }

  await client.disconnect();
  process.exit(0);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
