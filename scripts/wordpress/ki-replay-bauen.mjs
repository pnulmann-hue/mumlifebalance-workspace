/**
 * Baut und deployt die Replay-Seite der KI-Masterclass.
 *
 *   cd scripts/wordpress
 *   node --env-file=.env ki-replay-bauen.mjs                      # trocken
 *   node --env-file=.env ki-replay-bauen.mjs --los                # anlegen/aktualisieren
 *
 * Gebaut nach dem Muster von /mba-webinar-replay/ (Seite 4025) — dieselbe
 * Struktur, dieselben Farben, derselbe Aufbau: Augenbraue · Überschrift ·
 * Einordnungssatz · Video · Angebotskasten.
 *
 * 🚨 Der Inhalt liegt in `post_content` (wp:html), NICHT in Elementor. Die
 *    Seite 4025 ist genauso gebaut und läuft — deshalb greift hier die
 *    Firewall-Grenze nicht, an der /mba/ gescheitert ist.
 *
 * 🚨 Eine bestehende Seite behält ihren Status. Ein Skript, das ungefragt auf
 *    `draft` setzt, nimmt eine Live-Seite vom Netz.
 */
import fs from "node:fs";

// ── Hier eintragen ────────────────────────────────────────────────────────
// Vimeo-Adresse der Aufzeichnung. Bei einem nicht gelisteten Video gehört der
// Privacy-Hash dazu: https://vimeo.com/<ID>/<HASH> → VIMEO_ID + VIMEO_HASH.
const VIMEO_ID = process.env.VIMEO_ID || "";
const VIMEO_HASH = process.env.VIMEO_HASH || "";   // der Teil nach dem /, bei unlisted
const SLUG = "ki-masterclass-replay";
const TITEL = "KI-Masterclass — Aufzeichnung";

// Preis-Phase: bis Do 15.10. gilt 277, ab Fr 16.10. dann 333.
const FRUEH_BIS = new Date("2026-10-15T23:59:59+02:00");
const frueh = new Date() <= FRUEH_BIS;
const PREIS = frueh ? "277" : "333";
// ──────────────────────────────────────────────────────────────────────────

if (!VIMEO_ID) {
  console.error("VIMEO_ID fehlt.\n" +
    "  node --env-file=.env ki-replay-bauen.mjs            (nach VIMEO_ID=… im Aufruf)\n" +
    "  Beispiel: VIMEO_ID=1234567890 VIMEO_HASH=abc123 node --env-file=.env ki-replay-bauen.mjs --los\n" +
    "  Die Adresse steht auf Vimeo unter Teilen; bei einem nicht gelisteten\n" +
    "  Video sieht sie so aus: vimeo.com/1234567890/abc123");
  process.exit(1);
}

const src = `https://player.vimeo.com/video/${VIMEO_ID}`
  + `?${VIMEO_HASH ? "h=" + VIMEO_HASH + "&" : ""}title=0&byline=0&portrait=0`;

const fristZeile = frueh
  ? `<p style="font-size:14px;color:#b56a24;font-weight:bold;text-transform:uppercase;letter-spacing:1px;margin:0 0 22px;">Zum Frühbucherpreis noch bis Donnerstag, 15. Oktober</p>`
  : `<p style="font-size:14px;color:#b56a24;font-weight:bold;text-transform:uppercase;letter-spacing:1px;margin:0 0 22px;">Die Kasse schliesst am 23. Oktober</p>`;

const preisZeile = frueh
  ? `<p style="font-size:17px;line-height:1.6;color:#0c1c30;font-weight:bold;margin:0 0 8px;">Easy KI für Networkerinnen: ${PREIS} statt 333 Franken. Start ist der 1. November.</p>`
  : `<p style="font-size:17px;line-height:1.6;color:#0c1c30;font-weight:bold;margin:0 0 8px;">Easy KI für Networkerinnen: ${PREIS} Franken. Start ist der 1. November.</p>`;

const INHALT = `<!-- wp:html -->
<div class="mlb-replay" style="max-width:820px;margin:0 auto;padding:40px 20px;font-family:'Source Sans 3',Arial,sans-serif;color:#0c1c30;">
<p style="text-transform:uppercase;letter-spacing:2px;font-size:13px;color:#12828c;font-weight:bold;margin:0 0 12px;">KI-Masterclass · Aufzeichnung</p>
<h1 style="font-family:'Philosopher',Georgia,serif;font-size:34px;line-height:1.2;margin:0 0 14px;color:#0c1c30;">Einmal erklären, wer du bist — und deine KI behält es</h1>
<p style="font-size:18px;line-height:1.6;color:#4a5868;margin:0 0 28px;">Nimm dir eine ruhige Stunde. Danach weisst du, warum deine KI-Texte bisher nach niemandem geklungen haben und wie du das änderst.</p>
<div style="padding:56.25% 0 0 0;position:relative;border-radius:14px;overflow:hidden;">
<iframe src="${src}" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" style="position:absolute;top:0;left:0;width:100%;height:100%;" title="KI-Masterclass Aufzeichnung"></iframe>
</div>
<div style="background:#f1ecdd;border-radius:14px;padding:30px 24px;margin:34px 0 0;text-align:center;">
<h2 style="font-family:'Philosopher',Georgia,serif;font-size:24px;margin:0 0 10px;color:#0c1c30;">Bereit, es selbst aufzubauen?</h2>
<p style="font-size:16px;line-height:1.6;color:#4a5868;margin:0 0 18px;">Im Kurs baust du genau diesen Arbeitsplatz — deine Assistenten, deine festen Aufträge, deine eigenen Werkzeuge. Zehn Kapitel, zwei Live-Calls, und die Gruppe bleibt auch danach.</p>
${preisZeile}
${fristZeile}
<a href="https://mumlifebalance.ch/ki-kurs/" style="display:inline-block;background:#dc822e;color:#ffffff;text-decoration:none;font-weight:bold;font-size:17px;padding:15px 34px;border-radius:12px;">Alles zum Kurs ansehen</a>
</div>
</div>
<!-- /wp:html -->`;

// ── Deploy ────────────────────────────────────────────────────────────────
const { WP_URL, WP_USER, WP_APP_PASSWORD } = process.env;
if (!WP_URL || !WP_USER || !WP_APP_PASSWORD) {
  console.error("Fehlende ENV — WP_URL, WP_USER, WP_APP_PASSWORD");
  process.exit(1);
}
const basis = WP_URL.replace(/\/$/, "") + "/wp-json/wp/v2";
const auth = "Basic " + Buffer.from(`${WP_USER}:${WP_APP_PASSWORD}`).toString("base64");

fs.writeFileSync("../../outputs/produkte/ki-treppe/ki-replay-inhalt.html", INHALT, "utf8");
console.log(`Preis-Phase : ${frueh ? "früh" : "regulär"} → ${PREIS}`);
console.log(`Video       : ${src}`);
console.log(`Inhalt      : ${INHALT.length} Zeichen → outputs/produkte/ki-treppe/ki-replay-inhalt.html`);

const such = await fetch(`${basis}/pages?slug=${SLUG}&status=any&context=edit`, { headers: { Authorization: auth } });
const treffer = await such.json();
const da = Array.isArray(treffer) && treffer[0];
console.log(`Seite       : ${da ? `${da.id} (${da.status}) — wird aktualisiert` : "gibt es noch nicht — wird angelegt"}`);

if (!process.argv.includes("--los")) {
  console.log("\nTrockenlauf. Mit --los wird geschrieben.");
  process.exit(0);
}

// 🚨 NinjaFirewall blockt jedes Schreiben mit `status: "publish"` (403,
//    gemessen 08.10.2026: draft 201 · publish 403, unabhängig vom Inhalt).
//    Deshalb wird nie ein Status mitgeschickt: eine neue Seite entsteht als
//    Entwurf und Patricia veröffentlicht mit einem Klick, eine bestehende
//    behält den Status, den sie hat.
const rumpf = { title: TITEL, slug: SLUG, content: INHALT, template: "elementor_canvas" };

const r = await fetch(da ? `${basis}/pages/${da.id}` : `${basis}/pages`, {
  method: "POST",
  headers: { Authorization: auth, "Content-Type": "application/json" },
  body: JSON.stringify(rumpf),
});
if (!r.ok) {
  console.error("FEHLER", r.status, (await r.text()).slice(0, 300));
  process.exit(1);
}
const res = await r.json();
console.log(`\nOK — Seite ${res.id}, status=${res.status}`);
console.log(res.link);

// Gegenprobe: ist das Video wirklich drin?
const nach = await fetch(`${basis}/pages/${res.id}?context=edit`, { headers: { Authorization: auth } });
const d2 = await nach.json();
const drin = (d2.content.raw || "").includes(VIMEO_ID);
console.log(`Gegenprobe  : Video-ID in der Seite: ${drin ? "ja ✓" : "NEIN ✗"}`);
if (!drin) process.exit(1);
