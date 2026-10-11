/**
 * Rendert die vier Design-Vorlagen zu Vorschau-Bildern.
 *
 * Zweck: Sicht-Pruefung nach dem Umfaerben (Visual-QA-Pflicht aus CLAUDE.md) —
 * stimmen die Farben, bricht keine Ueberschrift unschoen um, ist irgendwo
 * noch Pink oder Gold uebrig?
 *
 * Aufruf (aus dem Projekt-Stammverzeichnis):
 *   node scripts/salespage-design/vorschau-rendern.mjs
 *
 * Ergebnis: outputs/salespage-designs/vorschau/<design>-01.png … (Seiten-
 * Abschnitte von oben nach unten) — der Ordner ist gitignored.
 *
 * Puppeteer kommt aus scripts/karussell-render/node_modules, damit hier keine
 * zweite Installation noetig ist.
 */

import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs";

const hier = path.dirname(fileURLToPath(import.meta.url));
const wurzel = path.resolve(hier, "..", "..");
const require = createRequire(
  path.join(wurzel, "scripts", "karussell-render", "package.json"),
);
const puppeteer = require("puppeteer");

const DESIGNS = [
  "minikurs-salespage",
  "signature-kurs-salespage",
  "skill-salespage",
  "ki-salespage",
];

const BREITE = 1280;
const HOEHE = 900;
const MAX_BILDER = 8; // reicht, um jeden Abschnitt einmal gesehen zu haben

const ausgabe = path.join(wurzel, "outputs", "salespage-designs", "vorschau");
fs.mkdirSync(ausgabe, { recursive: true });

const browser = await puppeteer.launch({
  headless: "new",
  args: ["--allow-file-access-from-files"],
});

for (const design of DESIGNS) {
  const datei = path.join(
    wurzel,
    ".claude",
    "skills",
    design,
    "references",
    "reference-page.html",
  );
  if (!fs.existsSync(datei)) {
    console.log(`  fehlt: ${datei}`);
    continue;
  }

  const seite = await browser.newPage();
  await seite.setViewport({ width: BREITE, height: HOEHE });
  await seite.goto(`file://${datei.replace(/\\/g, "/")}`, {
    waitUntil: "networkidle0",
    timeout: 60000,
  });
  // Schriften abwarten, sonst steht im Bild noch die Ersatz-Schrift
  await seite.evaluate(() => document.fonts.ready);

  // Einblend-Animationen scharfschalten: Die Vorlagen blenden Abschnitte per
  // IntersectionObserver ein (.rev -> .in). Beim sprunghaften Scrollen fuer die
  // Bilder loest das nicht zuverlaessig aus, und der Abschnitt bliebe leer.
  await seite.evaluate(() => {
    document.querySelectorAll(".rev, [class*='rev']").forEach((el) => el.classList.add("in"));
    document.querySelectorAll("*").forEach((el) => {
      const s = getComputedStyle(el);
      if (s.opacity === "0" && s.transitionProperty.includes("opacity")) {
        el.style.opacity = "1";
        el.style.transform = "none";
      }
    });
  });

  const gesamt = await seite.evaluate(() => document.body.scrollHeight);
  const schritte = Math.min(MAX_BILDER, Math.ceil(gesamt / HOEHE));

  for (let i = 0; i < schritte; i++) {
    const y = Math.round((i * (gesamt - HOEHE)) / Math.max(1, schritte - 1));
    await seite.evaluate((pos) => window.scrollTo(0, pos), y);
    await new Promise((r) => setTimeout(r, 450)); // Parallax/Reveals nachziehen lassen
    const name = `${design}-${String(i + 1).padStart(2, "0")}.png`;
    await seite.screenshot({ path: path.join(ausgabe, name) });
  }

  console.log(`${design.padEnd(26)} ${schritte} Bilder (Seite ${gesamt}px hoch)`);
  await seite.close();
}

await browser.close();
console.log(`\nVorschau liegt in ${path.relative(wurzel, ausgabe)}`);
