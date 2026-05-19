// Lädt alle 14 Mama-CEO Webinar-Mails als Campaign-Drafts in AC hoch.
// Liste 2 · Absender Patricia Ulmann · patricia@mumlifebalance.ch
// Skip: 5 + 6 (wirst du als geplante Mass-Send selbst anlegen mit Schedule-Datum)
// Hochgeladen werden ALLE 14, du entscheidest in AC welche du wie nutzt.

import { readFileSync, readdirSync } from "fs";
import { resolve, join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

const mcpConfig = JSON.parse(readFileSync(resolve(__dirname, "../../.mcp.json"), "utf8"));
const env = mcpConfig.mcpServers.activecampaign.env;
const AC_BASE_URL = env.AC_API_URL.replace(/\/$/, "");
const AC_API_KEY = env.AC_API_KEY;

const MAILS_DIR = resolve(__dirname, "../../outputs/produkte/mama-ceo/08-funnel/webinar-mails");

const LIST_ID = 2;
const FROM_NAME = "Patricia Ulmann";
const FROM_EMAIL = "patricia@mumlifebalance.ch";

const mailMap = [
  { file: "01-bestaetigung.html",          name: `Mama-CEO 01 — Bestätigung`,            subject: `Du bist drin. Mittwoch 20.5. 09:00 — wir sehen uns.` },
  { file: "02-1woche-vorher.html",         name: `Mama-CEO 02 — 1Woche vorher`,         subject: `„Heute mach ich endlich Content" — und am Abend nichts gepostet?` },
  { file: "03-reminder-24h.html",          name: `Mama-CEO 03 — Reminder 24h`,          subject: `Morgen 09:00 — und noch eine kleine Bitte` },
  { file: "04-reminder-1h.html",           name: `Mama-CEO 04 — Reminder 1h`,           subject: `In 1 Stunde — hier ist dein Zoom-Link` },
  { file: "05-cliffhanger-live.html",      name: `Mama-CEO 05 — Cliffhanger LIVE`,      subject: `🔴 LIVE — komm rein, ich zeige in 5 Min meinen Kochassistenten` },
  { file: "06-cart-open.html",             name: `Mama-CEO 06 — Cart Open`,             subject: `Es ist soweit. Mama-CEO ist offen — Earlybird CHF 249 (nur bis Sa 23.5.)` },
  { file: "07-painpoint.html",             name: `Mama-CEO 07 — Painpoint`,             subject: `„Heute schaff ich's wirklich" — und am Abend?` },
  { file: "08-earlybird-end-morgens.html", name: `Mama-CEO 08 — Earlybird-End Morgens`, subject: `Heute 23:59 endet der Earlybird. 16 Stunden zu CHF 249.` },
  { file: "09-earlybird-end-last2h.html",  name: `Mama-CEO 09 — Earlybird-End Last 2h`, subject: `Letzte 2 Stunden Earlybird (CHF 249 → 333).` },
  { file: "10-earlybird-vorbei.html",      name: `Mama-CEO 10 — Earlybird vorbei`,      subject: `Earlybird vorbei — Cart bleibt offen bis 31.5.` },
  { file: "11-midweek-antikunden.html",    name: `Mama-CEO 11 — Antikunden`,            subject: `Für wen Mama-CEO NICHT ist (ehrlich)` },
  { file: "12-letzte-tage.html",           name: `Mama-CEO 12 — Letzte Tage`,           subject: `3 Tage noch — und warum ich diesen Kurs unbedingt mit dir machen will` },
  { file: "13-close-morgens.html",         name: `Mama-CEO 13 — Close Morgens`,         subject: `Heute 23:59 schliesst Mama-CEO endgültig. 16h noch.` },
  { file: "14-close-letzte2h.html",        name: `Mama-CEO 14 — Close Last 2h`,         subject: `Letzte 2 Stunden. Cart-Close 23:59.` },
];

async function acV1(action, params) {
  const url = `${AC_BASE_URL}/admin/api.php?api_action=${action}&api_key=${AC_API_KEY}&api_output=json`;
  const parts = [];
  for (const [k, v] of Object.entries(params)) {
    if (v !== null && v !== undefined) parts.push(`${k}=${encodeURIComponent(String(v))}`);
  }
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: parts.join("&"),
  });
  const json = await res.json();
  if (json.result_code !== 1) throw new Error(`AC V1 ${action}: ${json.result_message}`);
  return json;
}

function stripHtml(html) {
  return html
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "")
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, "")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

const results = [];

for (const mail of mailMap) {
  const filePath = join(MAILS_DIR, mail.file);
  const html = readFileSync(filePath, "utf8");
  const text = stripHtml(html);

  process.stdout.write(`[${mail.file.padEnd(34)}] `);

  try {
    // Step 1: Message anlegen
    const msgResp = await acV1("message_add", {
      format: "html",
      htmlconstructor: "external",
      textconstructor: "external",
      subject: mail.subject,
      fromname: FROM_NAME,
      fromemail: FROM_EMAIL,
      reply2: FROM_EMAIL,
      html,
      text,
      "p[0]": LIST_ID,
    });
    const messageId = msgResp.id;

    // Step 2: Campaign anlegen
    const campResp = await acV1("campaign_create", {
      type: "single",
      name: mail.name,
      sdate: "",
      status: 0,
      public: 0,
      tracklinks: "all",
      subject: mail.subject,
      fromname: FROM_NAME,
      fromemail: FROM_EMAIL,
      reply2: FROM_EMAIL,
      "p[0]": LIST_ID,
      [`m[${messageId}]`]: 100,
    });

    console.log(`✅ Campaign #${campResp.id} · Message #${messageId}`);
    results.push({ file: mail.file, name: mail.name, campaign_id: campResp.id, message_id: messageId });
  } catch (e) {
    console.log(`❌ ${e.message}`);
    results.push({ file: mail.file, name: mail.name, error: e.message });
  }
}

console.log("\n\n=== ZUSAMMENFASSUNG ===");
const ok = results.filter(r => r.campaign_id).length;
const fail = results.filter(r => r.error).length;
console.log(`✅ ${ok}/14 erfolgreich · ❌ ${fail}/14 fehlgeschlagen`);
console.log("\nCampaign-IDs:");
for (const r of results) {
  if (r.campaign_id) console.log(`  ${r.file.padEnd(34)} → Campaign #${r.campaign_id}`);
  else console.log(`  ${r.file.padEnd(34)} → ERROR: ${r.error}`);
}
