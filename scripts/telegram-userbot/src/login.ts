/**
 * Einmaliger Login-Script — generiert die TELEGRAM_SESSION.
 *
 * Führe aus mit: npm run login
 *
 * Fragt nach deiner Handynummer und dem Bestätigungscode,
 * speichert dann die Session in .env (TELEGRAM_SESSION=...)
 *
 * Sobald das läuft brauchst du das nicht mehr — die Session bleibt gültig
 * solange du dich nicht ausloggst oder Telegram sie invalidiert.
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
  console.error("❌ TELEGRAM_API_ID und TELEGRAM_API_HASH müssen in .env gesetzt sein");
  process.exit(1);
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

function ask(q: string): Promise<string> {
  return new Promise((resolve) => rl.question(q, (answer) => resolve(answer.trim())));
}

async function main() {
  console.log("\n🔐 Telegram Login — einmalige Einrichtung\n");
  console.log("Das ist wie ein zweites Gerät für dein Telegram.");
  console.log("Du bekommst einen Bestätigungscode per Telegram (auf einem anderen Gerät).\n");

  const session = new StringSession("");
  const client = new TelegramClient(session, apiId, apiHash, {
    connectionRetries: 5,
  });

  await client.start({
    phoneNumber: async () => await ask("📱 Handynummer (mit +41... für Schweiz): "),
    password: async () => await ask("🔑 2FA-Passwort (falls aktiviert, sonst Enter): "),
    phoneCode: async () => await ask("📩 Code aus Telegram: "),
    onError: (err) => console.error("Error:", err),
  });

  const sessionString = client.session.save() as unknown as string;
  console.log("\n✅ Erfolgreich eingeloggt!\n");

  // Speichere Session in .env
  const envPath = path.join(__dirname, "..", ".env");
  let envContent = fs.readFileSync(envPath, "utf-8");

  if (envContent.includes("TELEGRAM_SESSION=")) {
    envContent = envContent.replace(
      /TELEGRAM_SESSION=.*/,
      `TELEGRAM_SESSION=${sessionString}`
    );
  } else {
    envContent += `\nTELEGRAM_SESSION=${sessionString}\n`;
  }

  fs.writeFileSync(envPath, envContent);
  console.log("💾 Session gespeichert in .env");

  // Hole User-Info
  const me = await client.getMe();
  console.log(`\n👤 Eingeloggt als: ${me.firstName} ${me.lastName || ""} (@${me.username || "n/a"})`);
  console.log(`🆔 User ID: ${me.id.toString()}`);

  // Speichere auch die User-ID
  if (envContent.includes("PATRICIA_TELEGRAM_USER_ID=")) {
    envContent = envContent.replace(
      /PATRICIA_TELEGRAM_USER_ID=.*/,
      `PATRICIA_TELEGRAM_USER_ID=${me.id.toString()}`
    );
    fs.writeFileSync(envPath, envContent);
  }

  console.log("\n🎉 Setup fertig! Du kannst jetzt 'npm start' ausführen.");
  console.log("Oder den Userbot auf Railway deployen.\n");

  await client.disconnect();
  rl.close();
  process.exit(0);
}

main().catch((err) => {
  console.error("❌ Fehler:", err);
  process.exit(1);
});
