// HTML → A4-PDF (und PNG zur Sichtprüfung). Puppeteer kommt aus scripts/karussell-render.
import { createRequire } from "module";
import path from "path";
import { pathToFileURL } from "url";

const require = createRequire(path.resolve("scripts/karussell-render/package.json"));
const puppeteer = require("puppeteer");

const [quelle, ziel] = process.argv.slice(2);
const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.setViewport({ width: 794, height: 1123, deviceScaleFactor: 2 });
await page.goto(pathToFileURL(path.resolve(quelle)).href, { waitUntil: "networkidle0" });
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: ziel, format: "A4", printBackground: true, pageRanges: "1" });
await page.screenshot({ path: ziel.replace(/\.pdf$/, ".png"), fullPage: true });
const ueberlauf = await page.evaluate(() => document.querySelector(".seite").scrollHeight > document.querySelector(".seite").clientHeight);
if (ueberlauf) console.log("⚠️ Inhalt ist länger als eine Seite");
await browser.close();
