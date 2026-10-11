/**
 * Deployt die 30-Tage-Energie-Routine-Verkaufsseite nach WordPress.
 *
 * Weg nach reference_wordpress-waf-lp-deploy:
 *  1. HTML OHNE <style>/<script>/<link rel=stylesheet> per REST (Imunify360 blockt das sonst mit 510)
 *  2. alles in einen Wrapper .enr, CSS darauf gescopt -> Customizer „Zusaetzliches CSS"
 *  3. KEIN @import (die dichte Google-Fonts-URL ist der eigentliche 510-Ausloeser)
 *  4. Gutenberg-Wrapper <!-- wp:html -->, sonst zerlegt wpautop die divs
 *  5. Bildpfade auf Mediathek-URLs, in Markup UND CSS
 *  6. Neue Seite als draft (Patricia publiziert selbst); bestehende behaelt ihren Status
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createOrUpdatePage, updatePage, findPageBySlug } from "./wp-api.js";

const HIER = path.dirname(fileURLToPath(import.meta.url));
const QUELLE = path.join(HIER, "../../outputs/produkte/doterra-mama-energie/landingpage/index.html");
const CSS_RAUS = path.join(HIER, "../../outputs/produkte/doterra-mama-energie/landingpage/customizer-css.txt");

const WRAP = "enr";
const SLUG = "energieroutine";
const TITEL = "30 Tage Energie-Routine";

// Mediathek-URLs (hochgeladen 21.09.2026)
const BILDER = {
  "assets/hero.jpg":  "https://mumlifebalance.ch/wp-content/uploads/2026/09/energieroutine-hero.jpg",
  "assets/pain.jpg":  "https://mumlifebalance.ch/wp-content/uploads/2026/09/pain.jpg",
  "assets/about.jpg": "https://mumlifebalance.ch/wp-content/uploads/2026/09/about.jpg",
  "assets/ende.jpg":  "https://mumlifebalance.ch/wp-content/uploads/2026/09/ende.jpg",
};

const roh = fs.readFileSync(QUELLE, "utf8");

// --- Blöcke über Indizes schneiden, nicht per Regex (Fallstrick vom 05.08.) ---
const cssStart = roh.lastIndexOf("<style>");
const cssEnde = roh.indexOf("</style>", cssStart);
if (cssStart < 0 || cssEnde < 0) throw new Error("Kein <style>-Block gefunden");
let css = roh.slice(cssStart + "<style>".length, cssEnde);

const bodyStart = roh.indexOf("<body>");
const bodyEnde = roh.lastIndexOf("</body>");
if (bodyStart < 0 || bodyEnde < 0) throw new Error("Kein <body> gefunden");
let markup = roh.slice(bodyStart + "<body>".length, bodyEnde);

// --- Bildpfade auf Mediathek ---
for (const [alt, neu] of Object.entries(BILDER)) {
  markup = markup.split(alt).join(neu);
  css = css.split(alt).join(neu);
}

// --- CSS auf .enr scopen ---
function scope(cssText) {
  // Kommentare raus (verduennt die Dichte zusaetzlich)
  cssText = cssText.replace(/\/\*[\s\S]*?\*\//g, "");
  const aus = [];
  let i = 0;
  while (i < cssText.length) {
    const auf = cssText.indexOf("{", i);
    if (auf < 0) break;
    const selektor = cssText.slice(i, auf).trim();
    // Block-Ende finden (verschachtelt bei @media)
    let tiefe = 0, j = auf;
    for (; j < cssText.length; j++) {
      if (cssText[j] === "{") tiefe++;
      else if (cssText[j] === "}") { tiefe--; if (tiefe === 0) break; }
    }
    const koerper = cssText.slice(auf + 1, j);

    if (selektor.startsWith("@media") || selektor.startsWith("@supports")) {
      aus.push(`${selektor} {\n${scope(koerper)}\n}`);
    } else if (selektor.startsWith("@")) {
      aus.push(`${selektor} {${koerper}}`); // @keyframes: Inhalt nicht scopen
    } else {
      const sel = selektor.split(",").map((s) => {
        s = s.trim();
        if (!s) return s;
        if (s === ":root" || s === "html" || s === "body") return `.${WRAP}`;
        if (s.startsWith(".") && s.slice(1).split(/[\s.:>]/)[0] === WRAP) return s;
        return `.${WRAP} ${s}`;
      }).join(", ");
      aus.push(`${sel} {${koerper}}`);
    }
    i = j + 1;
  }
  return aus.join("\n");
}

const cssGescopt = scope(css);
fs.writeFileSync(CSS_RAUS, cssGescopt, "utf8");

// --- Markup in Wrapper + Gutenberg-Block ---
const inhalt = `<!-- wp:html -->\n<div class="${WRAP}">\n${markup.trim()}\n</div>\n<!-- /wp:html -->`;

// Sicherheitsnetze gegen die WAF
for (const verboten of ["<style", "<script", "<link rel=\"stylesheet\"", "@import"]) {
  if (inhalt.includes(verboten)) throw new Error(`ABBRUCH: "${verboten}" steckt noch im Markup — das blockt die WAF.`);
}
console.log(`Markup ${(inhalt.length / 1024).toFixed(1)} KB · CSS ${(cssGescopt.length / 1024).toFixed(1)} KB (-> Customizer)`);

// Nur eine NEUE Seite startet als Entwurf. Eine bestehende behaelt ihren Status —
// sonst nimmt jedes Nachziehen die Live-Seite vom Netz (gefunden 24.09.2026).
const bestehend = await findPageBySlug(SLUG);
const seite = await createOrUpdatePage({
  title: TITEL,
  slug: SLUG,
  content: inhalt,
  ...(bestehend ? {} : { status: "draft" }),
});
console.log(`✅ Seite ${seite.id} · /${SLUG} · Status ${seite.status}`);

await updatePage(seite.id, { template: "elementor_canvas" });
console.log("✅ Template elementor_canvas gesetzt (kein Theme-Header, volle Breite)");
console.log(`\nCSS fuer den Customizer liegt in:\n  ${CSS_RAUS}`);
