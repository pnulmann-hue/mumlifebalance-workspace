// Sicht-Pruefung der Startklar-Verkaufsseite: volle Breite, in Abschnitten.
// Puppeteer kommt aus scripts/karussell-render/node_modules.
import { createRequire } from "node:module";
import { mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

// Node loest Pakete relativ zur SKRIPTDATEI auf, nicht zum Arbeitsverzeichnis.
// Deshalb zeigt der require ausdruecklich auf die Installation nebenan.
const hier = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const puppeteer = require(path.join(hier, "..", "karussell-render", "node_modules", "puppeteer"));
const WURZEL = path.join(hier, "..", "..");

const ZIEL = path.join(WURZEL, "outputs", "salespages", "startklar", "vorschau");
mkdirSync(ZIEL, { recursive: true });

const b = await puppeteer.launch({ headless: "new" });
const p = await b.newPage();
await p.setViewport({ width: 1440, height: 1000 });
await p.goto("http://localhost:4384", { waitUntil: "networkidle0" });
// Die Einblend-Animationen scharf schalten, sonst sind gefuellte Abschnitte leer
await p.evaluate(() => document.querySelectorAll(".rev").forEach((e) => e.classList.add("in")));
await new Promise((r) => setTimeout(r, 1200));

const h = await p.evaluate(() => document.body.scrollHeight);
const teile = Math.ceil(h / 1000);
for (let i = 0; i < teile; i++) {
  await p.evaluate((y) => window.scrollTo(0, y), i * 1000);
  await new Promise((r) => setTimeout(r, 400));
  await p.screenshot({ path: path.join(ZIEL, `teil-${String(i).padStart(2, "0")}.png`) });
}
console.log(`Seitenhoehe ${h}px -> ${teile} Bilder in ${ZIEL}`);
await b.close();
