/**
 * Deployt die Seite nach dem Bestätigungsklick des Energie-Kickstarts:
 *   /energie-kickstart-bestaetigt/  (Ziel der Opt-in-Bestätigung im AC-Formular 64)
 *
 * Inhalt: outputs/produkte/doterra-mama-energie/bestaetigt/inhalt.html
 * Die Abschnitte „vier Bausteine“ und „Preis“ kommen unverändert aus der
 * Verkaufsseite /energieroutine/ — Preis und Leistungen stehen nur dort.
 * Gestaltung: dasselbe .enr-CSS wie /energieroutine/, liegt schon im Customizer.
 *
 * Neue Seite als Entwurf (Patricia publiziert selbst), bestehende behält ihren Status.
 *
 *   cd scripts/wordpress && node --env-file=.env deploy-energie-bestaetigt.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createOrUpdatePage, updatePage, findPageBySlug } from "./wp-api.js";

const HIER = path.dirname(fileURLToPath(import.meta.url));
const BASIS = path.join(HIER, "../../outputs/produkte/doterra-mama-energie");
const SLUG = "energie-kickstart-bestaetigt";
const TITEL = "Bestätigt – Energie-Kickstart";

const lp = fs.readFileSync(path.join(BASIS, "landingpage/index.html"), "utf8");
let inhalt = fs.readFileSync(path.join(BASIS, "bestaetigt/inhalt.html"), "utf8");

// Abschnitt ab Kommentarmarke bis zum nächsten </section> — über Indizes, nicht per Regex
function abschnitt(marke) {
  const a = lp.indexOf(marke);
  if (a < 0) throw new Error(`Marke fehlt in der Verkaufsseite: ${marke}`);
  if (lp.indexOf(marke, a + 1) >= 0) throw new Error(`Marke doppelt: ${marke}`);
  const e = lp.indexOf("</section>", a);
  return lp.slice(a, e + "</section>".length);
}
// Kopfkommentar zuerst weg — er nennt die Platzhalter selbst und gehört nicht nach WordPress
inhalt = inhalt.replace(/^<!--[\s\S]*?-->\s*/, "");
inhalt = inhalt
  .replace("{{SYSTEM}}", abschnitt("<!-- SYSTEM: die vier Bausteine -->"))
  .replace("{{PREIS}}", abschnitt("<!-- PRICING -->"));

for (const rest of ["{{", "assets/"]) {
  if (inhalt.includes(rest)) throw new Error(`ABBRUCH: "${rest}" steckt noch im Markup`);
}
const block = `<!-- wp:html -->\n<div class="enr">\n${inhalt.trim()}\n</div>\n<!-- /wp:html -->`;
for (const verboten of ["<style", "<script", '<link rel="stylesheet"', "@import"]) {
  if (block.includes(verboten)) throw new Error(`ABBRUCH: "${verboten}" im Markup — das blockt die WAF.`);
}

if (process.argv.includes("--vorschau")) {
  // Lokale Ansicht mit dem Customizer-CSS der Verkaufsseite
  const css = fs.readFileSync(path.join(BASIS, "landingpage/customizer-css.txt"), "utf8");
  const datei = path.join(BASIS, "bestaetigt/vorschau.html");
  fs.writeFileSync(datei, `<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>body{margin:0}${css}</style></head><body><div class="enr">${inhalt}</div></body></html>`, "utf8");
  console.log("Vorschau:", datei);
  process.exit(0);
}

const bestehend = await findPageBySlug(SLUG);
const seite = await createOrUpdatePage({
  title: TITEL, slug: SLUG, content: block,
  ...(bestehend ? {} : { status: "draft" }),
});
console.log(`✅ Seite ${seite.id} · /${SLUG} · Status ${seite.status}`);
await updatePage(seite.id, { template: "elementor_canvas" });
console.log("✅ Template elementor_canvas");
