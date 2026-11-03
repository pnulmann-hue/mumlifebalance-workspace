/**
 * Deployt die Danke-Seite nach dem Öl-Abend-Formular (AC-Formular 77): /oelabend-danke/
 *
 * Inhalt: outputs/doterra-strategie/oelabend/danke-inhalt.html
 * Gestaltung: dasselbe .enr-CSS wie /energieroutine/, liegt schon im Customizer.
 * Neue Seite als Entwurf (Patricia publiziert selbst), bestehende behält ihren Status.
 *
 *   cd scripts/wordpress && node --env-file=.env deploy-oelabend-danke.mjs [--vorschau]
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HIER = path.dirname(fileURLToPath(import.meta.url));
const ORDNER = path.join(HIER, "../../outputs/doterra-strategie/oelabend");
const SLUG = "oelabend-danke";
const TITEL = "Danke für den Öl-Abend";

const inhalt = fs.readFileSync(path.join(ORDNER, "danke-inhalt.html"), "utf8").replace(/^<!--[\s\S]*?-->\s*/, "");
const block = `<!-- wp:html -->\n<div class="enr">\n${inhalt.trim()}\n</div>\n<!-- /wp:html -->`;
for (const verboten of ["<style", "<script", '<link rel="stylesheet"', "@import"]) {
  if (block.includes(verboten)) throw new Error(`ABBRUCH: "${verboten}" im Markup — das blockt die WAF.`);
}

if (process.argv.includes("--vorschau")) {
  const css = fs.readFileSync(path.join(HIER, "../../outputs/produkte/doterra-mama-energie/landingpage/customizer-css.txt"), "utf8");
  const datei = path.join(ORDNER, "danke-vorschau.html");
  fs.writeFileSync(datei, `<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${TITEL}</title>
<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>body{margin:0}${css}</style></head><body><div class="enr">${inhalt}</div></body></html>`, "utf8");
  console.log("Vorschau:", datei);
  process.exit(0);
}

const { createOrUpdatePage, updatePage, findPageBySlug } = await import("./wp-api.js");
const bestehend = await findPageBySlug(SLUG);
const seite = await createOrUpdatePage({
  title: TITEL, slug: SLUG, content: block,
  ...(bestehend ? {} : { status: "draft" }),
});
console.log(`✅ Seite ${seite.id} · /${SLUG} · Status ${seite.status}`);
await updatePage(seite.id, { template: "elementor_canvas" });
console.log("✅ Template elementor_canvas");
