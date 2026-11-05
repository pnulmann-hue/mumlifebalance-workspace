/**
 * Zeigt die neuesten Nachrichten einer Gruppe, nur lesend (Anmeldung TELEGRAM_SESSION_ABGLEICH).
 *   npx tsx src/gruppe-neueste.ts "<namensteil>" [--tage 14]
 */
import "dotenv/config";
import { TelegramClient } from "telegram";
import { StringSession } from "telegram/sessions";

async function main() {
  const client = new TelegramClient(
    new StringSession(process.env.TELEGRAM_SESSION_ABGLEICH || ""),
    parseInt(process.env.TELEGRAM_API_ID || "", 10),
    process.env.TELEGRAM_API_HASH || "",
    { connectionRetries: 3 }
  );
  client.setLogLevel("error" as any);
  await client.connect();
  const muster = process.argv[2].toLowerCase();
  const i = process.argv.indexOf("--tage");
  const seit = Date.now() / 1000 - parseInt(i > 0 ? process.argv[i + 1] : "14", 10) * 86400;
  const dialoge = await client.getDialogs({ limit: 400 });
  for (const d of dialoge.filter((x) => (x.title || "").toLowerCase().includes(muster))) {
    console.log("==", d.title);
    for (const m of await client.getMessages(d.entity, { limit: 80 })) {
      if (m.date < seit) break;
      const datei = m.file?.name || (m.media ? "[Medien " + (m.file?.mimeType || "Foto") + "]" : "");
      console.log(new Date(m.date * 1000).toISOString().slice(0, 16), m.id, datei, "|", (m.message || "").replace(/\s+/g, " ").slice(0, process.argv.includes("--voll") ? 3000 : 220));
    }
  }
  await client.disconnect();
  process.exit(0);
}
main().catch((e) => { console.error(e); process.exit(1); });
