/**
 * Baut die Meta-Creatives für die Stimm-Check-Anzeige.
 *
 *   node scripts/ads/creatives-bauen.mjs
 *
 * Ausgabe: outputs/ads/creatives/stimm-check/<name>-<format>.png
 *
 * Zwei Creatives, je drei Formate:
 *   1  "Ugly Ad"  — reine Petrol-Fläche mit Typo. Text-Ads sind der schnellste
 *                   Weg, einen Hook zu testen, und stoppen den Daumen besser
 *                   als Hochglanz.
 *   2  Foto       — Shootingbild mit Hook daneben. Gesicht schafft Vertrauen
 *                   bei kaltem Traffic.
 *
 * 🚨 Keine KI-generierten Menschen. Die Fotos kommen aus den Shootings.
 * 🚨 Safe Zones: im 9:16 und 16:9 legt Meta oben und unten Bedienelemente
 *    drüber. Der Hook gehört in die Mitte, darum SICHER_OBEN/UNTEN.
 * 🚨 Creative und Primärtext dürfen nie denselben Satz tragen — welcher Text
 *    zu welchem Bild gehört, steht in der Anzeigen-Datei.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import puppeteer from "../karussell-render/node_modules/puppeteer/lib/esm/puppeteer/puppeteer.js";

const HIER = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HIER, "../..");
const ZIEL = path.join(ROOT, "outputs/ads/creatives/stimm-check");

// --- Marke ----------------------------------------------------------------
const PETROL = "#12828c", TINTE = "#0c1c30", CREME = "#f1ecdd", ORANGE = "#dc822e";
const SERIF = "'Philosopher', Georgia, serif";
const SANS = "'Source Sans 3', 'Source Sans Pro', Helvetica, Arial, sans-serif";

// 🔁 Foto für Creative 2. s01–s12 sind die fürs Cover ausgewählten Shootingbilder.
const FOTO = path.join(ROOT, "outputs/_bild-editor/assets/s04.jpg");

// bildpos = Ausschnitt des Fotos. Im Breitformat sitzt sie sonst mittig und
// der Hook läuft ihr über Kinn und Hals — darum dort nach rechts schieben,
// damit links freier Grund für den Text bleibt.
const FORMATE = [
  // name       breite  hoehe  sicher oben  sicher unten  bildpos
  ["1x1",        1080,  1080,   0.06,        0.06,        "center 22%"],
  ["9x16",       1080,  1920,   0.14,        0.20,        "center 20%"],  // Meta legt oben+unten drüber
  ["16x9",       1200,   628,   0.08,        0.08,        "72% 18%"],
];

const CREATIVES = [
  {
    name: "c1-text",
    hook: "Es liegt nicht an deinem Prompt.",
    unter: "Deiner KI fehlt, wer du bist.",
    fuss: "Der Stimm-Check · kostenlos, 15 Minuten",
    foto: null,
  },
  {
    name: "c2-foto",
    hook: "Ich habe ein Jahr gebraucht.",
    unter: "Bis meine KI endlich geklungen hat wie ich.",
    fuss: "Der Stimm-Check · kostenlos, 15 Minuten",
    foto: FOTO,
  },
];

function alsDataUri(p) {
  if (!p) return null;
  if (!fs.existsSync(p)) throw new Error(`Foto fehlt: ${p}`);
  const art = p.endsWith(".png") ? "png" : "jpeg";
  return `data:image/${art};base64,${fs.readFileSync(p).toString("base64")}`;
}

function seite(c, [, breite, hoehe, oben, unten, bildpos]) {
  const bild = alsDataUri(c.foto);
  // Schriftgrösse an der kürzeren Kante, damit sie in allen drei Formaten trägt
  const basis = Math.min(breite, hoehe);
  const hookPx = Math.round(basis * (c.foto ? 0.085 : 0.105));
  const unterPx = Math.round(basis * 0.042);
  const fussPx = Math.round(basis * 0.030);
  const rand = Math.round(breite * 0.085);

  // Auf dem Foto liegt ein Verlauf von unten, damit der Text trägt und das
  // Gesicht oben frei bleibt. Radius bewusst unter 50 %, sonst entsteht an der
  // Boxkante ein harter Strich (gelernt 19.09.2026).
  const grund = bild
    ? `background:${TINTE} url('${bild}') ${bildpos || "center 22%"} / cover no-repeat;`
    : `background:${PETROL};`;

  const schleier = bild
    ? `<div style="position:absolute; inset:0;
         background:linear-gradient(to top,
           rgba(12,28,48,.94) 0%, rgba(12,28,48,.88) 34%,
           rgba(12,28,48,.42) 58%, rgba(12,28,48,0) 78%);"></div>`
    : "";

  return `<!doctype html><html lang="de"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:${breite}px;height:${hoehe}px;overflow:hidden}
  .buehne{position:relative;width:${breite}px;height:${hoehe}px;${grund}}
  /* Auf dem Foto sitzt das Gesicht oben, darum rutscht der Text nach unten.
     Ohne Foto gehört er in die Mitte — sonst steht im 9:16 zwei Drittel
     leere Fläche und der Hook klebt am unteren Rand. */
  .inhalt{position:absolute;left:${rand}px;right:${rand}px;
    top:${Math.round(hoehe * oben)}px;bottom:${Math.round(hoehe * unten)}px;
    display:flex;flex-direction:column;
    justify-content:${bild ? "flex-end" : "center"};gap:${Math.round(basis * 0.028)}px}
  .hook{font-family:${SERIF};font-size:${hookPx}px;line-height:1.12;color:${CREME};
    font-weight:700;letter-spacing:-.5px}
  .unter{font-family:${SANS};font-size:${unterPx}px;line-height:1.35;color:${ORANGE};font-weight:600}
  .fuss{font-family:${SANS};font-size:${fussPx}px;color:rgba(241,236,221,.82);
    font-weight:600;letter-spacing:1.5px;text-transform:uppercase;
    margin-top:${Math.round(basis * 0.02)}px}
  .strich{width:${Math.round(basis * 0.16)}px;height:${Math.max(3, Math.round(basis * 0.007))}px;
    background:${ORANGE};border-radius:99px}
</style></head><body>
<div class="buehne">
  ${schleier}
  <div class="inhalt">
    <div class="strich"></div>
    <div class="hook">${c.hook}</div>
    <div class="unter">${c.unter}</div>
    <div class="fuss">${c.fuss}</div>
  </div>
</div></body></html>`;
}

const browser = await puppeteer.launch({ headless: "new", args: ["--no-sandbox"] });
fs.mkdirSync(ZIEL, { recursive: true });
let n = 0;

for (const c of CREATIVES) {
  for (const f of FORMATE) {
    const [name, breite, hoehe] = f;
    const p = await browser.newPage();
    await p.setViewport({ width: breite, height: hoehe, deviceScaleFactor: 1 });
    await p.setContent(seite(c, f), { waitUntil: "networkidle0" });
    await p.evaluate(() => document.fonts.ready);   // sonst misst der Browser mit Ersatzschrift
    const datei = path.join(ZIEL, `${c.name}-${name}.png`);
    await p.screenshot({ path: datei, type: "png" });
    await p.close();
    console.log(`  ${path.basename(datei).padEnd(22)} ${breite}×${hoehe}`);
    n++;
  }
}

await browser.close();
console.log(`\n${n} Creatives in ${path.relative(ROOT, ZIEL)}`);
console.log("🚨 Jetzt anschauen: Gesicht frei? Text in der Mitte? Keine Kante im Verlauf?");
