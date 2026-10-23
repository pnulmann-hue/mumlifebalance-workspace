/**
 * Öl-App (22.10.2026) — holt die GANZE Geschichte der doTERRA-Gruppen und -Kanäle für die private Öl-App.
 *
 *   cd scripts/telegram-userbot && npx tsx src/oel-gruppen-holen.ts --liste   # nur zeigen, welche Chats
 *   cd scripts/telegram-userbot && npx tsx src/oel-gruppen-holen.ts           # holen (Text + Fotos)
 *
 * Patricia: „ein umfassendes Sammelsurium auch mit den Tipps und Rezepten aus den Telegramgruppen".
 * Anders als abgleich.ts (nur neue Nachrichten, alle Gruppen) holt das hier nur die Öl-Gruppen, dafür alles.
 * Fotos werden mitgeladen, weil viele Rezepte als Bildkarte gepostet sind (Texterkennung danach über
 * scripts/doterra/ocr-windows.ps1).
 *
 * Ausgabe: outputs/oel-app/roh/telegram/<chatId>.json + bilder/<chatId>-<msgId>.jpg
 * 🚨 gitignored — Nachrichten anderer Menschen, Repo ist public. Nur lesend, markiert nichts als gelesen.
 * Nutzt dieselbe Anmeldung wie abgleich.ts — nie gleichzeitig mit dem Abgleich laufen lassen.
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
if (!apiId || !apiHash || !sessionString) {
  console.error("❌ TELEGRAM_API_ID / TELEGRAM_API_HASH / TELEGRAM_SESSION_ABGLEICH fehlen in .env");
  process.exit(1);
}

const WS = path.resolve(__dirname, "..", "..", "..");
// Auch für andere Gruppen: --muster "rise to lead|exchange" --ziel outputs/doterra-business/roh/telegram
// (seit 23.10.2026 für die Business-Mentoring-Gruppen; ohne Angaben wie bisher die Öl-Gruppen)
const arg = (n: string) => { const i = process.argv.indexOf(n); return i > 0 ? process.argv[i + 1] : ""; };
const MUSTER = arg("--muster") ? new RegExp(arg("--muster"), "i") : null;
const ZIEL = arg("--ziel") ? path.resolve(WS, arg("--ziel")) : path.join(WS, "outputs", "oel-app", "roh", "telegram");
const BILDER = path.join(ZIEL, "bilder");

// Öl-Gruppen über den Titel. Business-, KI- und Instagram-Gruppen bleiben draussen.
const REIN = /d[oō]terra|ō |bogo|deep dive|detox|darm|frankincense|melissa|kids ?collection|kosmetik|supplement|essential emotion|prevent|hormonic|well-?being|wellness|gesund|cleanse|alpine|metapwr|spring|energetic|kundengruppe|fragegruppe|convention|live a cause|gubi|diy|zeit für die seele|iss dies|wendepunkt|herbst/i;
const RAUS = /business|mentoring|teamaufbau|verkauf|instagram|social media|leads?|massive action|ki\b|claude|produktwelt|produkterstellung|podcast|moneytalk|umsetzerinnen|content|meta|mum life|mama-ceo|backstage|story-challenge|familien|gamili|automatisiere|julia|mitgliedschaft|meisterkurs|easy ki|blick hinter|31 verkaufs|august challenge|ne'na'na/i;

async function main() {
  const nurListe = process.argv.includes("--liste");
  fs.mkdirSync(BILDER, { recursive: true });

  const client = new TelegramClient(new StringSession(sessionString), apiId, apiHash,
    { connectionRetries: 5, floodSleepThreshold: 300 });  // Wartezeiten von Telegram bis 5 Min. abwarten
  client.setLogLevel("error" as any);
  await client.connect();

  const dialogs = await client.getDialogs({ limit: 500 });
  const chats = dialogs.filter((d) => (d.isGroup || d.isChannel) &&
    (MUSTER ? MUSTER.test(d.title || "") : REIN.test(d.title || "") && !RAUS.test(d.title || "")));
  console.log(`${chats.length} Gruppen und Kanäle`);
  for (const d of chats) console.log(" ·", d.title);
  if (nurListe) { await client.disconnect(); return; }

  let summe = 0, fotos = 0;
  for (const d of chats) {
    const id = d.id?.toString() || "";
    const datei = path.join(ZIEL, `${id}.json`);
    const bisher: any[] = fs.existsSync(datei) ? JSON.parse(fs.readFileSync(datei, "utf-8")) : [];
    let hoechste = bisher.reduce((m, x) => Math.max(m, x.id), 0);
    const neu: any[] = [];
    // 🚨 Bei grossen Gruppen bremst Telegram nach ein paar hundert Nachrichten („Request was unsuccessful
    //    5 time(s)“). In „dōTERRA Mama & Kind“ (33'000 Nachrichten) kamen deshalb nur die ersten 2'422.
    //    Darum seitenweise lesen, nach jeder Seite sichern, bei einem Fehler warten und an der letzten
    //    Nachricht weitermachen — erst nach mehreren Fehlern hintereinander aufgeben.
    let fehler = 0;
    while (true) {
      let seite: any[];
      try {
        seite = await client.getMessages(d.entity, { limit: 100, minId: hoechste, reverse: true });
        fehler = 0;
      } catch (e: any) {
        // 🚨 In „Mama & Kind“ scheitert jede Seite ab #3242 — immer dieselbe Stelle, also eine einzelne
        //    Nachricht, die sich nicht lesen lässt. Nach zwei Fehlern die nächsten 100 Nummern einzeln
        //    abfragen und nur die kaputten überspringen.
        if (++fehler < 3) { await new Promise((r) => setTimeout(r, 20_000)); continue; }
        if (fehler > 8) { console.log(`  ⚠️  aufgegeben in ${d.title} nach #${hoechste}: ${e?.message || e}`); break; }
        seite = [];
        const kaputt: number[] = [];
        for (let i = hoechste + 1; i <= hoechste + 100; i++) {
          try { const [m] = await client.getMessages(d.entity, { ids: [i] }); if (m && (m as any).date) seite.push(m); }
          catch { kaputt.push(i); }
        }
        console.log(`  … einzeln gelesen in ${d.title} ab #${hoechste + 1}: ${seite.length} da, übersprungen ${kaputt.join(", ") || "keine"}`);
        if (!seite.length) { hoechste += 100; continue; }  // Lücke in der Nummerierung: weiter
      }
      if (!seite.length) break;
      for (const m of seite) {
      hoechste = Math.max(hoechste, m.id);
      const text = (m.message || "").trim();
      let bild = "";
      if (m.media instanceof Api.MessageMediaPhoto && !process.argv.includes("--ohne-fotos")) {
        bild = `${id}-${m.id}.jpg`;
        const ziel = path.join(BILDER, bild);
        if (!fs.existsSync(ziel)) {
          try {
            const buf = await client.downloadMedia(m, {});
            if (buf) { fs.writeFileSync(ziel, buf as Buffer); fotos++; } else bild = "";
          } catch { bild = ""; }
        }
      }
      if (!text && !bild) continue;
      // Wer schreibt: in Kanälen der Autorenname, in Gruppen die Absenderin — trennt Mentorinnen von der Gruppe
      const s: any = (m as any).sender;
      const von = (m as any).postAuthor || [s?.firstName, s?.lastName].filter(Boolean).join(" ") || s?.title || "";
      neu.push({
        chat: d.title, chatId: id, id: m.id, datum: new Date(m.date * 1000).toISOString(),
        von, text, bild, antwortAuf: m.replyTo?.replyToMsgId || null,
      });
      }
      fs.writeFileSync(datei, JSON.stringify(bisher.concat(neu), null, 1));  // nach jeder Seite sichern
      await new Promise((r) => setTimeout(r, 700));
    }
    summe += neu.length;
    console.log(`  ${neu.length.toString().padStart(5)}  ${d.title}`);
  }
  await client.disconnect();
  console.log(`→ ${summe} Nachrichten, ${fotos} Fotos in ${path.relative(WS, ZIEL)}`);
}
main().catch((e) => { console.error("❌", e?.message || e); process.exit(1); });
