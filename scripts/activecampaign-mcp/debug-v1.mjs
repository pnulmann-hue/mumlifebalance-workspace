// Quick V1 debug — testet message_add mit verschiedenen list-Formaten
import { readFileSync } from "fs";

const mcpConfig = JSON.parse(readFileSync(new URL("../../.mcp.json", import.meta.url), "utf8"));
const env = mcpConfig.mcpServers.activecampaign.env;
const AC_BASE_URL = env.AC_API_URL.replace(/\/$/, "");
const AC_API_KEY = env.AC_API_KEY;

const variants = [
  { name: "Variante A — list[0] literal", listKey: "list[0]" },
  { name: "Variante B — list[0] URL-encoded", listKey: encodeURIComponent("list[0]") },
  { name: "Variante C — list[] (PHP shortcut)", listKey: "list[]" },
  { name: "Variante D — p[0] (alternativer Feldname)", listKey: "p[0]" },
];

const baseParams = {
  format: "html",
  htmlconstructor: "external",
  textconstructor: "external",
  subject: "Debug Test",
  fromname: "Patricia Ulmann",
  fromemail: "patricia@mumlifebalance.ch",
  reply2: "patricia@mumlifebalance.ch",
  html: "<p>Test</p>",
  text: "Test",
};

for (const variant of variants) {
  const url = `${AC_BASE_URL}/admin/api.php?api_action=message_add&api_key=${AC_API_KEY}&api_output=json`;
  const parts = [];
  for (const [k, v] of Object.entries(baseParams)) {
    parts.push(`${k}=${encodeURIComponent(String(v))}`);
  }
  parts.push(`${variant.listKey}=2`);
  const body = parts.join("&");

  console.log(`\n=== ${variant.name} ===`);
  console.log(`Body sample: ...&${variant.listKey}=2`);

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });
    const text = await res.text();
    try {
      const json = JSON.parse(text);
      console.log(`Status: ${res.status} · result_code: ${json.result_code} · message: ${json.result_message?.slice(0, 100)}`);
      if (json.result_code === 1) {
        console.log(`✅ MESSAGE-ID erhalten: ${json.id}`);
      }
    } catch {
      console.log(`Status: ${res.status} · Body (first 200 chars): ${text.slice(0, 200)}`);
    }
  } catch (e) {
    console.log(`Error: ${e.message}`);
  }
}
