/**
 * Call-Aufzeichnungen aus einer Telegram-Gruppe holen (21.10.2026) — zum Transkribieren.
 *
 *   npx tsx src/calls-holen.ts --chat "oel" --liste          # Video/Audio ab 10 Min. auflisten
 *   npx tsx src/calls-holen.ts --chat "oel" --holen 123,456  # diese Nachrichten herunterladen
 *
 * Nutzt die nur-lesende Abgleich-Anmeldung. Ablage: video/telegram-calls/ (gitignored —
 * fremde Stimmen und Namen, Repo ist public).
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
if (!apiId || !apiHash || !sessionString) { console.error("❌ Zugang fehlt in .env"); process.exit(1); }

const WS = path.resolve(__dirname, "..", "..", "..");
const ZIEL = path.join(WS, "video", "telegram-calls");
const MIN_SEK = 600;

function arg(name: string) { const i = process.argv.indexOf(name); return i > 0 ? process.argv[i + 1] : ""; }

function dauer(doc: Api.Document) {
  for (const a of doc.attributes) {
    if (a instanceof Api.DocumentAttributeVideo || a instanceof Api.DocumentAttributeAudio) return Number(a.duration);
  }
  return 0;
}

async function main() {
  const muster = new RegExp(arg("--chat") || "oel|öl|schule|academy", "i");
  const client = new TelegramClient(new StringSession(sessionString), apiId, apiHash, { connectionRetries: 3 });
  client.setLogLevel("error" as any);
  await client.connect();

  const dialogs = (await client.getDialogs({ limit: 500 })).filter((d) => (d.isGroup || d.isChannel) && muster.test(d.title || ""));
  if (!dialogs.length) { console.log("Keine Gruppe passt zu", muster); await client.disconnect(); return; }

  const holen = (arg("--holen") || "").split(",").filter(Boolean).map(Number);
  for (const d of dialogs) {
    console.log(`\n== ${d.title} (${d.id})`);
    if (holen.length) {
      fs.mkdirSync(ZIEL, { recursive: true });
      const msgs = await client.getMessages(d.entity, { ids: holen });
      for (const m of msgs) {
        if (!m || !(m.media instanceof Api.MessageMediaDocument)) continue;
        const doc = m.media.document as Api.Document;
        const endung = (doc.mimeType || "").includes("audio") ? "m4a" : "mp4";
        const datei = path.join(ZIEL, `${new Date(m.date * 1000).toISOString().slice(0, 10)}-${m.id}.${endung}`);
        if (fs.existsSync(datei)) { console.log("schon da:", datei); continue; }
        console.log("lade", m.id, Math.round(Number(doc.size) / 1e6), "MB …");
        await client.downloadMedia(m, { outputFile: datei } as any);
        console.log("✓", datei);
      }
      continue;
    }
    for await (const m of client.iterMessages(d.entity, { limit: 3000 })) {
      if (!(m.media instanceof Api.MessageMediaDocument)) continue;
      const doc = m.media.document as Api.Document;
      const sek = dauer(doc);
      if (sek < MIN_SEK) continue;
      const text = (m.message || "").replace(/\s+/g, " ").slice(0, 90);
      console.log(`${new Date(m.date * 1000).toISOString().slice(0, 10)} · id ${m.id} · ${Math.round(sek / 60)} Min · ${Math.round(Number(doc.size) / 1e6)} MB · ${text}`);
    }
  }
  await client.disconnect();
}
main().catch((e) => { console.error(e); process.exit(1); });
