/**
 * Liest Telegram-Einladungslinks aus einer Textdatei (ein Hash je Zeile, ohne „https://t.me/+“)
 * und fragt je Link nur den Gruppennamen ab (messages.CheckChatInvite). Tritt keiner Gruppe bei.
 *
 *   npx tsx src/einladungen-pruefen.ts <links.txt>
 *
 * Nutzt die Lese-Anmeldung TELEGRAM_SESSION_ABGLEICH (wie abgleich.ts).
 */
import "dotenv/config";
import { readFileSync } from "node:fs";
import { TelegramClient, Api } from "telegram";
import { StringSession } from "telegram/sessions";

const apiId = parseInt(process.env.TELEGRAM_API_ID || "");
const apiHash = process.env.TELEGRAM_API_HASH || "";
const sessionString = process.env.TELEGRAM_SESSION_ABGLEICH || "";
if (!apiId || !apiHash || !sessionString) { console.error("❌ TELEGRAM_API_ID / _HASH / _SESSION_ABGLEICH fehlen"); process.exit(1); }

const datei = process.argv[2];
const hashes = readFileSync(datei, "utf8").split(/\r?\n/).map((z) => z.trim()).filter(Boolean);
async function main() {
const client = new TelegramClient(new StringSession(sessionString), apiId, apiHash, { connectionRetries: 3 });
await client.connect();
for (const hash of hashes) {
  try {
    const r: any = await client.invoke(new Api.messages.CheckChatInvite({ hash }));
    const titel = r.title ?? r.chat?.title ?? "?";
    console.log(`${hash}\t${titel}`);
  } catch (e: any) {
    console.log(`${hash}\t(ungültig: ${e.errorMessage || e.message})`);
    if (String(e.errorMessage || "").startsWith("FLOOD_WAIT")) break;
  }
  await new Promise((r) => setTimeout(r, 1500));
}
await client.disconnect();
process.exit(0);
}
main();
