/**
 * Einmalige Anmeldung für den Telegram-Abgleich (13.10.2026).
 *
 *   cd scripts/telegram-userbot && npm run abgleich-anmelden
 *
 * 🚨 Eine EIGENE Anmeldung (TELEGRAM_SESSION_ABGLEICH), nicht die des Userbots. Läuft dieselbe
 *    Anmeldung gleichzeitig an zwei Orten (Railway + Rechner), kann Telegram sie sperren.
 *    So ist der Abgleich wie ein weiteres Gerät: in Telegram unter Einstellungen → Geräte sichtbar
 *    und dort jederzeit abmeldbar.
 *
 * Handynummer, Code und ggf. 2FA-Passwort tippt Patricia selbst ein — nie über den Chat.
 */
import { TelegramClient } from "telegram";
import { StringSession } from "telegram/sessions";
import * as dotenv from "dotenv";
import * as fs from "fs";
import * as path from "path";
import * as readline from "readline";

dotenv.config();
const apiId = parseInt(process.env.TELEGRAM_API_ID || "");
const apiHash = process.env.TELEGRAM_API_HASH || "";
if (!apiId || !apiHash) {
  console.error("❌ TELEGRAM_API_ID und TELEGRAM_API_HASH fehlen in .env");
  process.exit(1);
}

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q: string) => new Promise<string>((r) => rl.question(q, (a) => r(a.trim())));

async function main() {
  console.log("\n🔐 Telegram-Abgleich fürs Cockpit — einmalige Anmeldung");
  console.log("Das ist wie ein weiteres Gerät. Der Abgleich liest nur, er schreibt nichts in deine Chats.\n");
  const client = new TelegramClient(new StringSession(""), apiId, apiHash, { connectionRetries: 5 });
  await client.start({
    phoneNumber: async () => await ask("📱 Handynummer (+41…): "),
    password: async () => await ask("🔑 2FA-Passwort (falls aktiviert, sonst Enter): "),
    phoneCode: async () => await ask("📩 Code aus Telegram: "),
    onError: (err) => console.error("Fehler:", err),
  });
  const s = client.session.save() as unknown as string;
  const envPath = path.join(__dirname, "..", ".env");
  let env = fs.readFileSync(envPath, "utf-8");
  env = env.includes("TELEGRAM_SESSION_ABGLEICH=")
    ? env.replace(/TELEGRAM_SESSION_ABGLEICH=.*/, `TELEGRAM_SESSION_ABGLEICH=${s}`)
    : env.trimEnd() + `\n\n# Cockpit-Abgleich (nur lesen) · 2026-10-13\nTELEGRAM_SESSION_ABGLEICH=${s}\n`;
  fs.writeFileSync(envPath, env);
  const me = await client.getMe();
  console.log(`\n✅ Angemeldet als ${me.firstName}. Gespeichert in .env (TELEGRAM_SESSION_ABGLEICH).`);
  console.log("Du kannst das Fenster schliessen.\n");
  await client.disconnect();
  rl.close();
  process.exit(0);
}
main().catch((e) => { console.error("❌", e); process.exit(1); });
