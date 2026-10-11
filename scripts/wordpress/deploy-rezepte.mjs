/**
 * Deployt die Rezeptseite nach WordPress.
 *
 * 🚨 **Ohne Customizer.** Der frühere Weg (HTML per REST + CSS gescopt in den
 * Customizer, siehe reference_wordpress-waf-lp-deploy) ist am 22.09.2026 auf halbem
 * Weg steckengeblieben: Das Markup stand live, das CSS nie — der Customizer braucht
 * einen eingeloggten Browser, und NinjaFirewall verlangt dafür ein Login. Ergebnis
 * war eine Seite mit null CSS-Regeln. Deshalb liefert `scripts/rezepte/inline.py`
 * jetzt eine Fassung, die ihr Aussehen selbst trägt.
 *
 * Aufruf:  node --env-file=.env deploy-rezepte.mjs [freebie|vollstaendig]
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createOrUpdatePage, updatePage, findPageBySlug } from "./wp-api.js";

const HIER = path.dirname(fileURLToPath(import.meta.url));
const WELCHE = (process.argv[2] || "freebie").toLowerCase();

const VARIANTEN = {
  freebie: {
    datei: "freebie-inline.html",
    slug: "fruehstuecke",
    titel: "Frühstücke, nach denen du um zehn keinen Hunger hast",
  },
  vollstaendig: {
    datei: "vollstaendig-inline.html",
    slug: "fruehstuecke-alle",
    titel: "Meine 30 Frühstücke",
  },
};
const V = VARIANTEN[WELCHE];
if (!V) throw new Error(`Unbekannt: ${WELCHE} — erlaubt: ${Object.keys(VARIANTEN).join(", ")}`);

const QUELLE = path.join(HIER, "../../outputs/produkte/doterra-mama-energie/rezepte", V.datei);
if (!fs.existsSync(QUELLE))
  throw new Error(`${V.datei} fehlt — zuerst: python scripts/rezepte/inline.py`);

const roh = fs.readFileSync(QUELLE, "utf8");
const bodyStart = roh.indexOf("<body");
const markup = roh.slice(roh.indexOf(">", bodyStart) + 1, roh.lastIndexOf("</body>")).trim();

const inhalt = `<!-- wp:html -->\n<div class="rzp">\n${markup}\n</div>\n<!-- /wp:html -->`;

// Die WAF (Imunify360) wirft jeden REST-POST mit diesen Stellen zurueck — 510.
for (const v of ["<style", "<script", '<link rel="stylesheet"', "@import"]) {
  if (inhalt.includes(v)) throw new Error(`ABBRUCH: "${v}" im Markup — das blockt die WAF.`);
}

const kb = inhalt.length / 1024;
console.log(`${V.datei}: ${kb.toFixed(1)} KB Markup, kein externes CSS nötig`);
if (kb > 40) console.log("⚠️  über 40 KB — wenn die WAF mit 510 antwortet, ist das der Verdacht");

// 🚨 Status NICHT mitschicken, wenn die Seite schon existiert. `status: "draft"`
// hat am 22.09. eine bereits veroeffentlichte Seite wieder auf Entwurf gezogen —
// sie war damit offline, und das Skript meldete trotzdem Erfolg. Neue Seiten legt
// createOrUpdatePage ohnehin als Entwurf an.
const vorhanden = await findPageBySlug(V.slug);
const seite = vorhanden
  ? await updatePage(vorhanden.id, { title: V.titel, content: inhalt })
  : await createOrUpdatePage({ title: V.titel, slug: V.slug, content: inhalt, status: "draft" });
console.log(`✅ Seite ${seite.id} · /${V.slug} · ${seite.status}${vorhanden ? " (Status unangetastet)" : ""}`);
await updatePage(seite.id, { template: "elementor_canvas" });
console.log("✅ Template elementor_canvas gesetzt");
