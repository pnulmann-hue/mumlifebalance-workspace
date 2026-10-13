/**
 * Telegram-Abgleich fürs Cockpit (13.10.2026) — holt neue Nachrichten aus allen Gruppen und Kanälen.
 *
 *   cd scripts/telegram-userbot && npm run abgleich            # neue Nachrichten seit dem letzten Lauf
 *   cd scripts/telegram-userbot && npm run abgleich -- --liste # nur zeigen, welche Chats gelesen würden
 *
 * Patricia: „alle :-D" — gemeint sind alle Gruppen und Kanäle. 🚨 Einzelchats (Freundinnen, Familie,
 * Kundinnen) bleiben bewusst draussen.
 *
 * Ausgabe: outputs/cockpit/abgleich/telegram/<JJJJ-MM-TT>.json (gitignored — Nachrichten anderer Menschen,
 * Repo ist public) + telegram/stand.json (letzte gelesene Nachricht je Chat).
 * Danach sortiert Claude im täglichen Abgleich: Produkt-Tipp → Öl-Wissen · Auftrag → Rising Leaders ·
 * Training → Business-Wege — alles nur als Vorschlag im Eingang, nie direkt.
 *
 * Nur lesend: getMessages markiert nichts als gelesen und schreibt nichts in die Chats.
 */
import { TelegramClient, Api } from "telegram";
import { StringSession } from "telegram/sessions";
import * as dotenv from "dotenv";
import * as fs from "fs";
import * as path from "path";

dotenv.config();
const apiId = parseInt(process.env.TELEGRAM_API_ID || "");
const apiHash = process.env.TELEGRAM_API_HASH || "";
const sessionString = process.env.TELEGRAM_SESSION_ABGLEICH || "";
if (!apiId || !apiHash) { console.error("❌ TELEGRAM_API_ID / TELEGRAM_API_HASH fehlen in .env"); process.exit(1); }
if (!sessionString) {
  console.error("❌ Noch keine Anmeldung für den Abgleich. Einmalig: npm run abgleich-anmelden");
  process.exit(2);
}

const WS = path.resolve(__dirname, "..", "..", "..");
const ZIEL = path.join(WS, "outputs", "cockpit", "abgleich", "telegram");
const STAND = path.join(ZIEL, "stand.json");
const ERSTER_LAUF_TAGE = 30;     // beim ersten Mal so weit zurück
const MAX_JE_CHAT = 400;

type Stand = { [chatId: string]: { letzteId: number; titel: string } };

async function main() {
  const nurListe = process.argv.includes("--liste");
  fs.mkdirSync(ZIEL, { recursive: true });
  const stand: Stand = fs.existsSync(STAND) ? JSON.parse(fs.readFileSync(STAND, "utf-8")) : {};

  const client = new TelegramClient(new StringSession(sessionString), apiId, apiHash, { connectionRetries: 3 });
  client.setLogLevel("error" as any);
  await client.connect();

  const dialogs = await client.getDialogs({ limit: 500 });
  const chats = dialogs.filter((d) => d.isGroup || d.isChannel);
  console.log(`${chats.length} Gruppen und Kanäle (Einzelchats ausgelassen: ${dialogs.length - chats.length})`);
  if (nurListe) {
    for (const d of chats) console.log(" ·", d.title, d.isChannel && !d.isGroup ? "(Kanal)" : "(Gruppe)");
    await client.disconnect();
    return;
  }

  const grenze = Math.floor(Date.now() / 1000) - ERSTER_LAUF_TAGE * 86400;
  const neu: any[] = [];
  for (const d of chats) {
    const id = d.id?.toString() || "";
    const vorher = stand[id]?.letzteId || 0;
    let hoechste = vorher;
    let n = 0;
    for await (const m of client.iterMessages(d.entity, { limit: MAX_JE_CHAT, minId: vorher })) {
      if (!vorher && m.date < grenze) break;
      hoechste = Math.max(hoechste, m.id);
      const text = (m.message || "").trim();
      if (!text) continue;                    // reine Bilder/Sticker ohne Text
      let von = "";
      try {
        const s: any = await m.getSender();
        von = s?.firstName ? [s.firstName, s.lastName].filter(Boolean).join(" ") : (s?.title || "");
      } catch { /* Kanal ohne Absender */ }
      neu.push({
        chat: d.title, chatId: id, art: d.isChannel && !d.isGroup ? "kanal" : "gruppe",
        id: m.id, datum: new Date(m.date * 1000).toISOString(), von, text,
        medien: m.media ? (m.media instanceof Api.MessageMediaDocument ? "datei" : "bild") : "",
      });
      n++;
    }
    stand[id] = { letzteId: hoechste, titel: d.title || "" };
    if (n) console.log(`  ${n.toString().padStart(4)}  ${d.title}`);
  }
  await client.disconnect();

  const heute = new Date().toISOString().slice(0, 10);
  const datei = path.join(ZIEL, `${heute}.json`);
  const bisher = fs.existsSync(datei) ? JSON.parse(fs.readFileSync(datei, "utf-8")) : [];
  fs.writeFileSync(datei, JSON.stringify(bisher.concat(neu), null, 1));
  fs.writeFileSync(STAND, JSON.stringify(stand, null, 1));
  console.log(`→ ${neu.length} neue Nachrichten in ${path.relative(WS, datei)}`);
}
main().catch((e) => { console.error("❌", e?.message || e); process.exit(1); });
