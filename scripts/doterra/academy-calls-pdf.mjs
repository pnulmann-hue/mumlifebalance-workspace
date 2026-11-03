// Macht aus den Call-Notizen der Ölschule Academy je Call ein PDF zum Nachlesen.
// Quelle: context/doTERRA/academy-oel-schule/*-zusammenfassung.md, _INDEX.md
//         und der Juni-Call in context/doTERRA/Produktwissen/.
// Ziel:   context/doTERRA/academy-oel-schule/pdf/ (gitignored, wie der ganze Ordner)
//
//   node scripts/doterra/academy-calls-pdf.mjs

import { createRequire } from "node:module";
import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const hier = dirname(fileURLToPath(import.meta.url));
const wurzel = join(hier, "..", "..");
const require = createRequire(join(wurzel, "scripts", "karussell-render", "package.json"));
const puppeteer = require("puppeteer");
const { marked } = require("marked");

const ordner = join(wurzel, "context", "doTERRA", "academy-oel-schule");
const ziel = join(ordner, "pdf");
mkdirSync(ziel, { recursive: true });

const quellen = [
  [join(ordner, "_INDEX.md"), "00-uebersicht-alle-calls.pdf"],
  // Gibt es zum Call ein Wissensdokument (<datum>-wissen.md, alles vermittelte Wissen,
  // Patricia 03.11.), nimmt es Vorrang vor den kürzeren Learnings.
  ...readdirSync(ordner)
    .filter((n) => n.endsWith("-zusammenfassung.md"))
    .sort()
    .map((n) => {
      const wissen = n.replace("-zusammenfassung.md", "-wissen.md");
      const quelle = existsSync(join(ordner, wissen)) ? wissen : n;
      return [join(ordner, quelle), n.replace("-zusammenfassung.md", "-call.pdf")];
    }),
];

// Patricia 03.11.: „volltext transkript bitte nicht in das PDF. ich brauche nur die learnings“
// Deshalb fliegen Wortlaut, Zeitablauf und Transkript-Notizen raus; es bleiben die Learnings.
const WEG = [/^Volltext/, /Volltext$/, /^Ablauf des Calls/, /^Unklar im Transkript/];

function nurLearnings(md) {
  const teile = md.split(/\n(?=## )/);
  return teile
    .filter((t) => {
      const kopf = t.match(/^## (.+)/);
      return !kopf || !WEG.some((m) => m.test(kopf[1].trim()));
    })
    .join("\n");
}

function aufbereiten(md) {
  return nurLearnings(md.replace(/\r\n/g, "\n"))
    .replace(/^---\n[\s\S]*?\n---\n/, "")                 // Frontmatter
    .replace(/^\*\*(Quelle|Erfasst am):\*\*.*\n/gm, "")    // Herkunftszeilen
    .replace(/^Referent ist .*\n/gm, "")                   // Hinweise zum Verhören im Transkript
    .replace(/ ?\(\d\d:\d\d[^)]*\)/g, "")                  // Zeitmarken in Klammern
    .replace(/^(#{2,4} )\d\d:\d\d(?:[–-]\d\d:\d\d)?\s*[·:–-]\s*/gm, "$1") // Zeitmarke vor dem Titel
    .replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, "$2")         // [[ziel|text]]
    .replace(/\[\[([^\]]+)\]\]/g, "$1")                    // [[ziel]]
    .replace(/\r\n/g, "\n");
}

const css = `
@import url('https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap');
@page { size: A4; margin: 18mm 17mm 20mm 17mm; }
body { font-family: 'Source Sans 3', sans-serif; font-size: 10.5pt; line-height: 1.5; color: #0c1c30; }
h1 { font-family: Philosopher, serif; font-size: 21pt; color: #29556d; line-height: 1.2; margin: 0 0 10pt;
     padding-bottom: 8pt; border-bottom: 3px solid #e9873b; }
h2 { font-family: Philosopher, serif; font-size: 15pt; color: #29556d; margin: 20pt 0 6pt; break-after: avoid; }
h3 { font-family: Philosopher, serif; font-size: 12.5pt; color: #0c1c30; margin: 14pt 0 4pt; break-after: avoid; }
p, li { orphans: 3; widows: 3; }
ul, ol { padding-left: 16pt; } li { margin: 2pt 0; }
strong { color: #0c1c30; }
blockquote { margin: 8pt 0; padding: 6pt 10pt; background: #f1ecdd; border-left: 3px solid #e9873b; }
blockquote p { margin: 2pt 0; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 9.5pt; break-inside: auto; }
th, td { border: 1px solid #d9d2bf; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { background: #29556d; color: #fff; font-weight: 600; }
tr { break-inside: avoid; }
hr { border: none; border-top: 1px solid #d9d2bf; margin: 14pt 0; }
code { font-size: 9.5pt; }
`;

// Dieselben Learnings fürs Cockpit (doTERRA → Ölschule-Calls, Sammlung "academy").
const cockpit = join(wurzel, "outputs", "cockpit", "abgleich", "academy");
mkdirSync(cockpit, { recursive: true });
for (const [quelle] of quellen) {
  const m = quelle.match(/(\d{4})-(\d\d)-(\d\d)-(zusammenfassung|wissen)\.md$/);
  if (!m) continue;
  const md = aufbereiten(readFileSync(quelle, "utf8"));
  const titel = (md.match(/^# (.+)$/m) || [, ""])[1]
    .replace(/^Ölschule Academy\s*[—–-]\s*(Wissen aus dem )?Call vom [\d.]+:\s*/, "");
  writeFileSync(join(cockpit, `${m[1]}-${m[2]}-${m[3]}.json`), JSON.stringify({
    datum: `${m[1]}-${m[2]}-${m[3]}`, datumText: `${m[3]}.${m[2]}.${m[1]}`,
    titel, md: md.replace(/^# .+\n/m, "").trim(),
  }));
}

const browser = await puppeteer.launch();
const seite = await browser.newPage();
for (const [quelle, name] of quellen) {
  if (!existsSync(quelle)) { console.log("fehlt:", quelle); continue; }
  const html = `<!doctype html><html lang="de"><head><meta charset="utf-8"><style>${css}</style></head>
<body>${marked.parse(aufbereiten(readFileSync(quelle, "utf8")))}</body></html>`;
  await seite.setContent(html, { waitUntil: "networkidle0" });
  await seite.evaluate(() => document.fonts.ready);
  const pdf = await seite.pdf({
    format: "A4", printBackground: true, displayHeaderFooter: true,
    headerTemplate: "<span></span>",
    footerTemplate: `<div style="font-size:8pt;color:#888;width:100%;text-align:center;font-family:sans-serif">
      Ölschule Academy · zum Nachlesen · Seite <span class="pageNumber"></span> von <span class="totalPages"></span></div>`,
    margin: { top: "18mm", bottom: "20mm", left: "17mm", right: "17mm" },
  });
  writeFileSync(join(ziel, name), pdf);
  console.log("✓", name, Math.round(pdf.length / 1024), "KB");
}
await browser.close();
