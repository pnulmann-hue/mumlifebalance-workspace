/**
 * Sucht in einer Telegram-Gruppe den doTERRA-Newsletter des Monats, nur lesend.
 * Eigene Anmeldung TELEGRAM_SESSION_ABGLEICH (nie die Session des Posters).
 *
 *   npx tsx src/newsletter-suchen.ts --gruppen            # alle Gruppen mit Namen
 *   npx tsx src/newsletter-suchen.ts --chat "<muster>" --ziel <ordner> [--tage 45] [--wort newsletter]
 *
 * Legt Treffer.json und die angehängten Dateien (PDF, Bilder) im Zielordner ab.
 */
import "dotenv/config";
import fs from "fs";
import path from "path";
import { TelegramClient } from "telegram";
import { StringSession } from "telegram/sessions";

function arg(name: string, vorgabe = ""): string {
  const i = process.argv.indexOf("--" + name);
  return i >= 0 ? process.argv[i + 1] || "" : vorgabe;
}

async function main() {
  const client = new TelegramClient(
    new StringSession(process.env.TELEGRAM_SESSION_ABGLEICH || ""),
    parseInt(process.env.TELEGRAM_API_ID || "", 10),
    process.env.TELEGRAM_API_HASH || "",
    { connectionRetries: 3 }
  );
  await client.connect();
  const dialoge = (await client.getDialogs({ limit: 400 })).filter((d) => d.isGroup || d.isChannel);

  if (process.argv.includes("--gruppen")) {
    for (const d of dialoge) console.log(String(d.id), "|", d.title);
    await client.disconnect();
    process.exit(0);
  }

  const muster = arg("chat").toLowerCase();
  const ziel = arg("ziel");
  // Das Booklet heisst „Aktionen - November 2026 .pdf“, angekündigt mit „NOVEMBER AKTIONEN“. Das Wort Newsletter fällt nie.
  const worte = arg("wort", "aktionen,newsletter").toLowerCase().split(",");
  const seit = Date.now() / 1000 - parseInt(arg("tage", "45"), 10) * 86400;
  const treffer = dialoge.filter((d) => (d.title || "").toLowerCase().includes(muster));
  if (!treffer.length) throw new Error("Keine Gruppe passt zu: " + muster);
  fs.mkdirSync(ziel, { recursive: true });

  const ergebnis: unknown[] = [];
  for (const d of treffer) {
    // Datei-Nachrichten tragen das Wort oft nur im Dateinamen, deshalb die letzten 300 Nachrichten selbst prüfen.
    // Dazu kommen die Bilder rund um einen Treffer: Flyer und Booklet-Bild stehen als Nachrichten ohne Text daneben.
    const neueste = await client.getMessages(d.entity, { limit: 300 });
    const alle = new Map<number, (typeof neueste)[number]>();
    for (const m of neueste) {
      if (m.date < seit) continue;
      const roh = ((m.message || "") + " " + (m.file?.name || "")).toLowerCase();
      if (!worte.some((w) => roh.includes(w)) && !/flyer/.test(roh)) continue;
      alle.set(m.id, m);
      for (const n of neueste) {
        const naehe = Math.abs(n.date - m.date) <= 300;
        if (naehe && n.media && !(n.message || "").trim()) alle.set(n.id, n);
      }
    }
    for (const m of alle.values()) {
      let ablage = "";
      if (m.media) {
        const name = m.file?.name || `${m.id}${m.file?.ext || ".jpg"}`;
        ablage = path.join(ziel, `${m.id}-${name}`.replace(/[\\/:*?"<>|]/g, "_"));
        if (!fs.existsSync(ablage)) await client.downloadMedia(m, { outputFile: ablage });
      }
      ergebnis.push({
        gruppe: d.title,
        id: m.id,
        datum: new Date(m.date * 1000).toISOString().slice(0, 16),
        text: m.message || "",
        datei: ablage,
      });
    }
  }
  fs.writeFileSync(path.join(ziel, "treffer.json"), JSON.stringify(ergebnis, null, 1), "utf8");
  console.log(ergebnis.length, "Treffer ->", ziel);
  await client.disconnect();
  process.exit(0);
}
main().catch((e) => { console.error(e); process.exit(1); });
