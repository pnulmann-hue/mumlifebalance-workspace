/**
 * Rendert Karussell-Folien mit der ECHTEN Zeichenroutine des Cockpits.
 *
 * Wozu: Beim Freigeben rendert das Cockpit jede Folie selbst und legt sie in
 * `freigaben/<id>/bilder` ab — daraus baut Blotato den Post. Wenn diese
 * Schleife im Browser haengenbleibt, steht die Karte auf gruen, aber es
 * liegt kein einziges Bild da, und der 20:00-Lauf findet nichts.
 * (Genau das ist am 21.09.2026 passiert.) Dieses Skript macht denselben
 * Schritt ausserhalb des Browsers, damit eine Freigabe nicht daran haengt.
 *
 * Die Zeichenroutine wird NICHT nachgebaut, sondern aus der Live-Fassung
 * herausgeschnitten (BRANDS, wrap, fitLines, drawCover, getImageObj,
 * renderSlide). Nachbauen hiesse, dass die Folien beim naechsten Umbau
 * anders aussehen als im Cockpit.
 *
 *   node scripts/cockpit/freigabe-folien.mjs <cockpit.html> <daten.json> <zielordner>
 *
 * daten.json: [{ id, brand, handle, slides:[{layout,headline,body}] }]
 * Ergebnis:   <zielordner>/<id>/slide-NN.json  mit { dataUrl, nr }
 */
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL, fileURLToPath } from "node:url";
import { createRequire } from "node:module";

// 🚨 fileURLToPath, nicht .pathname — sonst steht "Mein%20Business" im Pfad
// und require findet nichts.
const HIER = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HIER, "..", "..");
const require = createRequire(pathToFileURL(path.join(REPO, "scripts", "karussell-render", "x.js")));
const puppeteer = require("puppeteer");

// 🚨 Die Artifact-Datenbank nimmt hoechstens 256 KB je Dokument. Das Cockpit
// selbst drueckt nur auf 700'000 Zeichen herunter — das liegt darueber.
const MAX = 240000;

function schnipsel(html, von, bis) {
  return html.split("\n").slice(von - 1, bis).join("\n");
}

function seiteBauen(cockpitHtml, ziel) {
  const h = fs.readFileSync(cockpitHtml, "utf8");
  const teil = (marke, ende) => {
    const von = h.split("\n").findIndex((l) => l.includes(marke)) + 1;
    if (!von) throw new Error("nicht gefunden: " + marke);
    const zeilen = h.split("\n");
    let bis = von;
    while (bis < zeilen.length && zeilen[bis].trimEnd() !== ende) bis++;
    return schnipsel(h, von, bis + 1);
  };
  const js = [
    "var images = {}, imageObjs = {};",
    teil("var BRANDS = {", "  };"),
    teil("function getImageObj(", "  }"),
    "var W = 1080, H = 1350;",
    teil("function wrap(ctx, text, maxW)", "  }"),
    teil("function fitLines(", "  }"),
    teil("function drawCover(", "  }"),
    teil("function renderSlide(", "  }"),
    `window.folieAlsJpeg = function (car, i) {
       var cv = document.createElement("canvas");
       renderSlide(cv, car.slides[i], car, i, car.slides.length);

       // 🚨 Randpruefung. wrap() bricht ein einzelnes langes Wort NIE um, und
       // fitLines() prueft nur die Hoehe — nie die Breite. Ein Wort wie
       // "KINDERBETREUUNG" laeuft deshalb rechts aus dem Bild, ohne dass
       // irgendetwas warnt. Gefunden am 22.09.2026 per Sichtpruefung; seitdem
       // misst das Skript die aeusseren 40 px gegen die Hintergrundfarbe.
       var ctx = cv.getContext("2d"), R = 40, treffer = 0;
       var grund = ctx.getImageData(4, Math.round(cv.height * 0.5), 1, 1).data;
       [ctx.getImageData(0, 0, R, cv.height), ctx.getImageData(cv.width - R, 0, R, cv.height)]
         .forEach(function (d) {
           for (var k = 0; k < d.data.length; k += 4) {
             if (Math.abs(d.data[k] - grund[0]) + Math.abs(d.data[k+1] - grund[1])
                 + Math.abs(d.data[k+2] - grund[2]) > 60) treffer++;
           }
         });

       var q = 0.92, out = cv.toDataURL("image/jpeg", q);
       while (out.length > ${MAX} && q > 0.4) { q -= 0.06; out = cv.toDataURL("image/jpeg", q); }
       return { url: out, rand: treffer };
     };`,
  ].join("\n\n");
  fs.writeFileSync(ziel, '<!doctype html><meta charset="utf-8"><body><script>\n' + js + "\n</script>");
  return ziel;
}

const [cockpit, daten, zielOrdner] = process.argv.slice(2);
if (!cockpit || !daten || !zielOrdner) {
  console.error("Aufruf: node freigabe-folien.mjs <cockpit.html> <daten.json> <zielordner>");
  process.exit(2);
}
const seite = seiteBauen(cockpit, path.join(path.dirname(daten), "_rendern.html"));
const karussells = JSON.parse(fs.readFileSync(daten, "utf8"));

const browser = await puppeteer.launch({ headless: "new" });
const page = await browser.newPage();
let fehler = 0;
page.on("pageerror", (e) => { console.error("SEITENFEHLER:", e.message); fehler++; });
await page.goto(pathToFileURL(seite).href);
await page.evaluateHandle("document.fonts.ready");

for (const car of karussells) {
  const ordner = path.join(zielOrdner, car.id);
  fs.mkdirSync(ordner, { recursive: true });
  for (let i = 0; i < car.slides.length; i++) {
    const r = await page.evaluate((c, k) => window.folieAlsJpeg(c, k), car, i);
    const url = r && r.url;
    if (!url || !url.startsWith("data:image/jpeg")) throw new Error(`${car.id} Folie ${i + 1}: kein Bild`);
    const nr = String(i + 1).padStart(2, "0");
    fs.writeFileSync(path.join(ordner, `slide-${nr}.json`), JSON.stringify({ dataUrl: url, nr: i + 1 }));
    const kb = (url.length / 1024).toFixed(0);
    const zuGross = url.length > 256000;
    // Ein paar Pixel sind Rauschen; ab 200 liegt wirklich Text im Rand.
    const randRaus = r.rand > 200;
    if (zuGross || randRaus) fehler++;
    console.log(`${car.id}  slide-${nr}  ${kb} KB`
      + (zuGross ? "   ZU GROSS FUER DIE DATENBANK" : "")
      + (randRaus ? `   TEXT LAEUFT AUS DEM BILD (${r.rand} Randpixel)` : ""));
  }
}
await browser.close();
if (fehler) { console.error(`\n${fehler} Problem(e) — nichts hochladen, bevor das geklaert ist.`); process.exit(1); }
console.log("\nAlle Folien gerendert, alle unter der 256-KB-Grenze.");
