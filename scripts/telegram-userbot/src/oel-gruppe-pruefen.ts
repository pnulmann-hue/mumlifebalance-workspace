/**
 * Öl-App — Prüfhilfe: zeigt für jede Öl-Gruppe, wie viel Telegram hat und wie viel geholt ist,
 * und testet bei einer Gruppe, ob sich die Nachrichten von der neuesten her lesen lassen.
 *
 *   cd scripts/telegram-userbot && npx tsx src/oel-gruppe-pruefen.ts            # Übersicht
 *   cd scripts/telegram-userbot && npx tsx src/oel-gruppe-pruefen.ts "Mama"     # eine Gruppe testen
 * Nur lesend.
 */
import { TelegramClient } from "telegram";
import { StringSession } from "telegram/sessions";
import * as dotenv from "dotenv";
import * as fs from "fs";
import * as path from "path";

dotenv.config();
const WS = path.resolve(__dirname, "..", "..", "..");
const ROH = path.join(WS, "outputs", "oel-app", "roh", "telegram");

async function main() {
  const client = new TelegramClient(new StringSession(process.env.TELEGRAM_SESSION_ABGLEICH || ""),
    parseInt(process.env.TELEGRAM_API_ID || ""), process.env.TELEGRAM_API_HASH || "", { connectionRetries: 3 });
  client.setLogLevel("error" as any);
  await client.connect();
  const suche = process.argv[2];
  const dialogs = await client.getDialogs({ limit: 500 });
  for (const d of dialogs) {
    if (!(d.isGroup || d.isChannel)) continue;
    const id = d.id?.toString() || "";
    const datei = path.join(ROH, `${id}.json`);
    if (!suche && !fs.existsSync(datei)) continue;
    if (suche && !(d.title || "").includes(suche)) continue;
    const geholt = fs.existsSync(datei) ? JSON.parse(fs.readFileSync(datei, "utf-8")) : [];
    const letzte = geholt.reduce((m: number, x: any) => Math.max(m, x.id), 0);
    const neueste = (d.message as any)?.id || 0;
    console.log(`${d.title}  ·  geholt ${geholt.length} bis #${letzte}  ·  neueste Nachricht #${neueste}`);
    if (!suche) continue;
    // von der neuesten her rückwärts bis zur letzten geholten — wo hakt es?
    let n = 0, tiefste = neueste;
    try {
      for await (const m of client.iterMessages(d.entity, { minId: letzte })) { n++; tiefste = m.id; }
      console.log(`  rückwärts lesbar: ${n} Nachrichten, bis hinunter zu #${tiefste}`);
    } catch (e: any) {
      console.log(`  rückwärts abgebrochen nach ${n} Nachrichten bei #${tiefste}: ${e?.message || e}`);
    }
  }
  await client.disconnect();
}
main().catch((e) => { console.error("❌", e?.message || e); process.exit(1); });
