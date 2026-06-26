// Lädt alle 14 MBA-Webinar-Mails als Campaign-Drafts in AC hoch.
// Liste 2 · Absender Patricia Ulmann · patricia@mumlifebalance.ch
// Webinar Mi 24.6.2026 · Pioneer 997 (bis Sa 27.6.) → Final 1347 (Cart-Close So 5.7.)
// Hochgeladen werden ALLE 14 als Draft (status 0) — du entscheidest in AC welche in welche Automation.

import { readFileSync } from "fs";
import { resolve, join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

const mcpConfig = JSON.parse(readFileSync(resolve(__dirname, "../../.mcp.json"), "utf8"));
const env = mcpConfig.mcpServers.activecampaign.env;
const AC_BASE_URL = env.AC_API_URL.replace(/\/$/, "");
const AC_API_KEY = env.AC_API_KEY;

const MAILS_DIR = resolve(__dirname, "../../outputs/produkte/mba-launch/webinar-mails");

const LIST_ID = 2;
const FROM_NAME = "Patricia Ulmann";
const FROM_EMAIL = "patricia@mumlifebalance.ch";

const mailMap = [
  { file: "01-bestaetigung.html",        name: `MBA 01 — Bestätigung`,            subject: `Du bist drin. Mittwoch 24.6. 09:00 — wir sehen uns.` },
  { file: "02-1woche-vorher.html",       name: `MBA 02 — Einladung 1 Woche`,      subject: `Abends halb zehn — und fürs Business hat der Tag wieder nicht gereicht?` },
  { file: "03-reminder-24h.html",        name: `MBA 03 — Reminder 24h`,           subject: `Morgen 09:00 — und eine kleine Bitte vorher` },
  { file: "04-reminder-1h.html",         name: `MBA 04 — Reminder 1h`,            subject: `In 1 Stunde live — hier ist dein Zoom-Link` },
  { file: "05-cliffhanger-live.html",    name: `MBA 05 — Cliffhanger LIVE`,       subject: `🔴 Wir sind live — komm rein` },
  { file: "06-cart-open.html",           name: `MBA 06 — Cart-Open`,              subject: `Es ist offen: die Mum Business Academy — Pioneer-Preis 997 (nur bis Sa 27.6.)` },
  { file: "07-painpoint.html",           name: `MBA 07 — Preis & Wert`,           subject: `Ich kann heute 25× essen gehen — und das hat einen Grund.` },
  { file: "08-pioneer-end-morgens.html", name: `MBA 08 — Pioneer-Ende Morgens`,   subject: `Heute 23:59 endet der Pioneer-Preis. 16 Stunden zu CHF 997.` },
  { file: "09-pioneer-end-abend.html",   name: `MBA 09 — Pioneer-Ende Abend 19h`, subject: `Heute Abend endet der Pioneer-Preis (CHF 997 → 1347).` },
  { file: "10-pioneer-vorbei.html",      name: `MBA 10 — Pioneer vorbei`,         subject: `Pioneer vorbei — die MBA bleibt offen bis So 5.7.` },
  { file: "11-antikunden.html",          name: `MBA 11 — Antikunden`,             subject: `Für wen die MBA NICHT ist (ehrlich)` },
  { file: "12-letzte-tage.html",         name: `MBA 12 — Letzte Tage`,            subject: `2 Tage noch — und warum ich diese Academy mit dir bauen will` },
  { file: "13-close-morgens.html",       name: `MBA 13 — Close Morgens`,          subject: `Heute 23:59 schliesst die MBA. 16 Stunden noch.` },
  { file: "14-close-abend.html",         name: `MBA 14 — Close Abend 19h`,        subject: `Heute Abend schliesst die MBA — letzter Aufruf.` },
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

  process.stdout.write(`[${mail.file.padEnd(28)}] `);

  try {
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
  if (r.campaign_id) console.log(`  ${r.file.padEnd(28)} → Campaign #${r.campaign_id}`);
  else console.log(`  ${r.file.padEnd(28)} → ERROR: ${r.error}`);
}
