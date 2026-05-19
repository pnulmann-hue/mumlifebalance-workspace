// Testet campaign_create mit verschiedenen list-Feldern (Message 494 ist schon angelegt)
import { readFileSync } from "fs";

const mcpConfig = JSON.parse(readFileSync(new URL("../../.mcp.json", import.meta.url), "utf8"));
const env = mcpConfig.mcpServers.activecampaign.env;
const AC_BASE_URL = env.AC_API_URL.replace(/\/$/, "");
const AC_API_KEY = env.AC_API_KEY;

const MSG_ID = 494; // Aus message_add Test

const variants = [
  { name: "list[0]=2", extras: { "list[0]": 2 } },
  { name: "p[0]=2", extras: { "p[0]": 2 } },
  { name: "list[0]=2 + m[MSG]=100", extras: { "list[0]": 2, [`m[${MSG_ID}]`]: 100 } },
  { name: "p[0]=2 + m[MSG]=100", extras: { "p[0]": 2, [`m[${MSG_ID}]`]: 100 } },
];

const baseParams = {
  type: "single",
  name: "Debug Campaign Test",
  sdate: "",
  status: 0,
  public: 0,
  tracklinks: "all",
  subject: "Debug",
  fromname: "Patricia Ulmann",
  fromemail: "patricia@mumlifebalance.ch",
  reply2: "patricia@mumlifebalance.ch",
};

for (const variant of variants) {
  const url = `${AC_BASE_URL}/admin/api.php?api_action=campaign_create&api_key=${AC_API_KEY}&api_output=json`;
  const parts = [];
  const allParams = { ...baseParams, ...variant.extras };
  for (const [k, v] of Object.entries(allParams)) {
    parts.push(`${k}=${encodeURIComponent(String(v))}`);
  }
  const body = parts.join("&");

  console.log(`\n=== ${variant.name} ===`);
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });
    const text = await res.text();
    try {
      const json = JSON.parse(text);
      console.log(`Status: ${res.status} · result_code: ${json.result_code} · msg: ${(json.result_message || "").slice(0, 120)}`);
      if (json.result_code === 1) console.log(`✅ CAMPAIGN-ID: ${json.id}`);
    } catch {
      console.log(`Status: ${res.status} · Body: ${text.slice(0, 200)}`);
    }
  } catch (e) {
    console.log(`Error: ${e.message}`);
  }
}
