/**
 * Lädt das geänderte MBA-Widget zurück auf WP-Seite 3857.
 *
 *   cd scripts/wordpress
 *   node --env-file=.env mba-hochladen.mjs            # trocken, zeigt nur was käme
 *   node --env-file=.env mba-hochladen.mjs --los      # schreibt
 *
 * 🚨 Die Seite ist eine Elementor-Seite. Der Inhalt liegt in `_elementor_data`
 *    (Pfad 0/0, ein text-editor-Widget), NICHT in post_content. Wer nur
 *    `content` setzt, ändert nichts Sichtbares.
 *
 * 🚨 `status` wird bewusst NICHT mitgeschickt. Ein Skript, das ungefragt auf
 *    `draft` setzt, nimmt eine Live-Seite vom Netz — genau das ist bei der
 *    Energie-Routine-Seite schon passiert.
 *
 * 🚨 Nach dem Schreiben wird zurückgelesen und verglichen. Eine Erfolgsmeldung
 *    ohne Gegenprobe sagt nur, dass die Anfrage angekommen ist.
 */
import fs from "node:fs";
import path from "node:path";

const LOS = process.argv.includes("--los");
const SEITE = 3857;
const NEU = "../../outputs/produkte/mba-launch/_sicherung/mba-widget-neu.html";

const { WP_URL, WP_USER, WP_APP_PASSWORD } = process.env;
if (!WP_URL || !WP_USER || !WP_APP_PASSWORD) {
  console.error("Fehlende ENV — benötigt WP_URL, WP_USER, WP_APP_PASSWORD in .env");
  process.exit(1);
}
const basis = WP_URL.replace(/\/$/, "") + "/wp-json/wp/v2";
const auth = "Basic " + Buffer.from(`${WP_USER}:${WP_APP_PASSWORD}`).toString("base64");

async function hole() {
  const r = await fetch(`${basis}/pages/${SEITE}?context=edit`, { headers: { Authorization: auth } });
  if (!r.ok) throw new Error(`GET ${r.status}`);
  return r.json();
}

const neuHtml = fs.readFileSync(path.resolve(NEU), "utf8");
const d = await hole();
const el = JSON.parse(d.meta._elementor_data);
const widget = el[0].elements[0];
const alt = widget.settings.editor;

console.log(`Seite ${SEITE} · ${d.slug} · status=${d.status} · template=${d.template}`);
console.log(`Widget alt: ${alt.length} Zeichen`);
console.log(`Widget neu: ${neuHtml.length} Zeichen  (${neuHtml.length - alt.length >= 0 ? "+" : ""}${neuHtml.length - alt.length})`);
console.log(`"Easy KI" alt: ${(alt.match(/Easy KI/g) || []).length}x · neu: ${(neuHtml.match(/Easy KI/g) || []).length}x`);

if (!LOS) {
  console.log("\nTrockenlauf. Mit --los wird geschrieben.");
  process.exit(0);
}

widget.settings.editor = neuHtml;

const r = await fetch(`${basis}/pages/${SEITE}`, {
  method: "POST",
  headers: { Authorization: auth, "Content-Type": "application/json" },
  // kein status, kein template — die bleiben, wie sie sind
  body: JSON.stringify({ meta: { _elementor_data: JSON.stringify(el) } }),
});
if (!r.ok) {
  console.error("FEHLER", r.status, (await r.text()).slice(0, 400));
  process.exit(1);
}

// --- Gegenprobe: zurücklesen -------------------------------------------
const nach = await hole();
const drin = JSON.parse(nach.meta._elementor_data)[0].elements[0].settings.editor;
const ok = drin === neuHtml;
console.log(`\nZurückgelesen: ${drin.length} Zeichen · identisch: ${ok ? "ja ✓" : "NEIN ✗"}`);
console.log(`status danach: ${nach.status} (vorher ${d.status})`);
if (!ok) {
  console.error("🚨 Der gespeicherte Stand weicht ab — im Browser nachsehen.");
  process.exit(1);
}
console.log("\nLive prüfen: https://mumlifebalance.ch/mba/");
