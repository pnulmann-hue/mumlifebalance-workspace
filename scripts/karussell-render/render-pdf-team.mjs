// Rendert ein Markdown-Dokument als gebrandetes PDF (doTERRA-Brand) via Puppeteer.
// Nutzung: node render-pdf-team.mjs --input="<pfad.md>" --output="<pfad.pdf>" --title="..."
import fs from "fs";
import path from "path";
import { marked } from "marked";
import puppeteer from "puppeteer";

const args = Object.fromEntries(
  process.argv.slice(2).map((a) => {
    const m = a.match(/^--([^=]+)=(.*)$/);
    return m ? [m[1], m[2]] : [a.replace(/^--/, ""), true];
  })
);

const inputPath = args.input;
const outputPath = args.output || inputPath.replace(/\.md$/, ".pdf");
const docTitle = args.title || "doTERRA";

const md = fs.readFileSync(inputPath, "utf-8");
let bodyHtml = marked.parse(md);

// Cover: ersten H1 + folgenden H2 + erste <em>-Zeile in einen Cover-Block packen
bodyHtml = bodyHtml.replace(
  /^\s*<h1[^>]*>([\s\S]*?)<\/h1>\s*<h2[^>]*>([\s\S]*?)<\/h2>\s*<p><em>([\s\S]*?)<\/em><\/p>/,
  '<div class="cover"><h1>$1</h1><h2>$2</h2><div class="sub">$3</div></div>'
);

const css = `
:root{
  --petrol:#12828c; --teal:#29556d; --creme:#f1ecdd; --orange:#dc822e;
  --ink:#2b2b2b; --soft:#5a5a5a;
}
*{box-sizing:border-box;}
body{
  font-family:'Source Sans 3', -apple-system, Segoe UI, sans-serif;
  color:var(--ink); font-size:11.5pt; line-height:1.55; margin:0;
}
h1,h2,h3,h4{font-family:'Philosopher', Georgia, serif; line-height:1.2; color:var(--teal);}
h1{font-size:30pt; color:var(--petrol); margin:0 0 4pt;}
h1 + h2{font-size:15pt; color:var(--orange); font-weight:400; margin:0 0 2pt; border:none; padding:0;}
h2{font-size:18pt; color:#fff; background:var(--petrol); padding:7pt 12pt; border-radius:6pt; margin:26pt 0 12pt; page-break-after:avoid;}
h3{font-size:13.5pt; color:var(--orange); margin:16pt 0 5pt; page-break-after:avoid;}
h4{font-size:12pt; color:var(--teal); margin:12pt 0 4pt;}
p{margin:0 0 8pt;}
ul{margin:0 0 9pt; padding-left:18pt;}
li{margin:0 0 4pt;}
strong{color:var(--teal);}
hr{border:none; border-top:1.5pt solid var(--creme); margin:18pt 0;}
em{color:var(--soft);}
a{color:var(--petrol);}
code{background:var(--creme); padding:1pt 4pt; border-radius:3pt; font-size:10.5pt;}
blockquote{
  background:var(--creme); border-left:5pt solid var(--orange);
  padding:12pt 16pt; border-radius:0 8pt 8pt 0; margin:0 0 16pt;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;
}
blockquote p:last-child{margin-bottom:0;}
blockquote strong{color:var(--orange);}

/* Titel-Block */
.cover{
  background:linear-gradient(135deg, var(--petrol), var(--teal));
  color:#fff; padding:34pt 30pt; border-radius:12pt; margin-bottom:22pt;
}
.cover h1{color:#fff;}
.cover h2{background:none; color:#ffe6cf; padding:0; font-size:15pt; margin:6pt 0 0;}
.cover .sub{color:#dceef0; font-size:10.5pt; margin-top:10pt;}

/* Hinweis-Box (erste blockquote) */
blockquote.note, .note{
  background:var(--creme); border-left:5pt solid var(--orange);
  padding:12pt 16pt; border-radius:0 8pt 8pt 0; margin:0 0 14pt;
}
.note strong{color:var(--orange);}

/* erste Produkt-Liste als Karte */
.intro-list{background:#fbf9f2; border:1pt solid var(--creme); border-radius:8pt; padding:10pt 14pt;}

h2, h3{ -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.cover, .note{ -webkit-print-color-adjust:exact; print-color-adjust:exact;}
`;

const html = `<!doctype html><html lang="de"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>${css}</style></head>
<body><div class="content">${bodyHtml}</div></body></html>`;

const browser = await puppeteer.launch({ headless: "new", args: ["--no-sandbox"] });
const page = await browser.newPage();
await page.setContent(html, { waitUntil: "networkidle0" });
try { await page.evaluateHandle("document.fonts.ready"); } catch {}

await page.pdf({
  path: outputPath,
  format: "A4",
  printBackground: true,
  margin: { top: "16mm", bottom: "18mm", left: "15mm", right: "15mm" },
  displayHeaderFooter: true,
  headerTemplate: `<div></div>`,
  footerTemplate: `<div style="width:100%; font-size:8pt; color:#9a9a9a; font-family:sans-serif; padding:0 15mm; display:flex; justify-content:space-between;">
    <span>${docTitle}</span>
    <span>Seite <span class="pageNumber"></span> / <span class="totalPages"></span></span>
  </div>`,
});

await browser.close();
console.log("PDF erstellt:", outputPath);
