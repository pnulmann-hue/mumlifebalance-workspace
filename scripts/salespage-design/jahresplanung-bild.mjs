// Hero-Bild für die Anmeldeseite „Neustart 2027 · Jahresplanungs-Workshop“ (Do 17.12.2026):
// Geräte-Collage wie beim Tool-Workshop (tool-workshop-bild.mjs), Thema Neujahr und Neustart:
// Laptop mit dem Jahresplan 2027, Tablet „Leben zuerst“, Tablet „Dein Januar“, Handy mit dem
// Kalenderblatt 1. Januar, dazu Funken. Beispieldaten von Sandra (Energie für Mamas ab 35), der
// erfundenen Beispiel-Person aus der Startklar-Werkstatt und dem Jahresplaner. Keine KI-Bilder.
//
//   node scripts/salespage-design/jahresplanung-bild.mjs
// -> outputs/salespages/jahresplanung/bild/hero.png (1500x900, durchsichtiger Hintergrund)
import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const require = createRequire(new URL('../karussell-render/package.json', import.meta.url));
const puppeteer = require('puppeteer');
const ZIEL = fileURLToPath(new URL('../../outputs/salespages/jahresplanung/bild/', import.meta.url));
mkdirSync(ZIEL, { recursive: true });

const F = { tinte: '#0c1c30', blau: '#29556d', petrol: '#12828c', orange: '#dc822e', creme: '#f1ecdd', weiss: '#fffdf8', linie: '#e3dac4', grau: '#cfc8b8' };

// Monatsraster: [Monat, Art, Text] — Art: f = Familie/Ferien, a = Fokus-Angebot, g = Gratis-Angebot, r = ruhig
const MONATE = [
  ['Jan', 'g', 'Gratis-Check'], ['Feb', 'f', 'Sportferien'], ['Mär', 'a', 'Minikurs'], ['Apr', 'f', 'Frühlingsferien'],
  ['Mai', 'a', 'Kurs-Launch'], ['Jun', 'g', 'Challenge'], ['Jul', 'f', 'Sommerferien'], ['Aug', 'r', 'ruhig starten'],
  ['Sep', 'a', 'Kurs-Launch'], ['Okt', 'f', 'Herbstferien'], ['Nov', 'g', 'Workshop'], ['Dez', 'r', 'Familienzeit'],
];
const monatHtml = MONATE.map(([m, a, t]) => `<div class="mo ${a}"><b>${m}</b><span>${t}</span></div>`).join('');

// Funken: feste Positionen, damit das Bild bei jedem Lauf gleich aussieht
const FUNKEN = [[120, 90, 10], [260, 40, 6], [1180, 70, 9], [1390, 160, 6], [1440, 300, 11], [60, 560, 7], [330, 840, 8],
  [1000, 860, 6], [1420, 600, 7], [900, 30, 8], [610, 60, 5], [1300, 820, 9], [200, 700, 5], [760, 880, 7]];
const funkenHtml = FUNKEN.map(([x, y, s]) => `<i class="fu" style="left:${x}px;top:${y}px;width:${s}px;height:${s}px"></i>`).join('');

const html = `<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Philosopher:wght@700&family=Source+Sans+3:wght@400;600;700;800&display=swap">
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:transparent}
.b{position:relative;width:1500px;height:900px;font-family:'Source Sans 3',sans-serif;color:${F.tinte}}
.ser{font-family:'Philosopher',serif}
.schatten{box-shadow:0 30px 70px rgba(12,28,48,.45),0 8px 20px rgba(12,28,48,.25)}
/* Laptop: Jahresplan 2027 */
.lap{position:absolute;left:400px;top:90px;width:700px;z-index:2}
.lap .deckel{background:${F.tinte};border-radius:26px 26px 10px 10px;padding:20px 20px 26px}
.lap .bs{background:${F.weiss};border-radius:8px;height:410px;padding:22px 28px;overflow:hidden}
.lap .fuss{height:26px;margin:0 -54px;background:linear-gradient(#d9d2c0,#a59e90);border-radius:0 0 28px 28px}
.kopf{display:flex;justify-content:space-between;align-items:center}
.marke{font-size:18px;font-weight:800;color:${F.blau};letter-spacing:.06em}
.pill{background:${F.creme};border:1.5px solid ${F.linie};border-radius:999px;padding:5px 13px;font-size:14px;font-weight:700;color:${F.petrol}}
.titel{font-size:34px;line-height:1.05;margin:12px 0 4px;color:${F.blau}}
.titel em{font-style:normal;color:${F.orange}}
.unter{font-size:15px;color:#4f5d68;font-weight:600;margin-bottom:14px}
.raster{display:grid;grid-template-columns:repeat(6,1fr);gap:9px}
.mo{border-radius:12px;padding:9px 8px 10px;min-height:76px;border:1.5px solid ${F.linie};background:#fff}
.mo b{display:block;font-size:15px;color:${F.tinte}}
.mo span{display:block;font-size:13px;font-weight:700;margin-top:6px;line-height:1.15}
.mo.a{background:#fdf1e6;border-color:${F.orange}} .mo.a span{color:${F.orange}}
.mo.g{background:#e6f3f3;border-color:${F.petrol}} .mo.g span{color:${F.petrol}}
.mo.f{background:#f3f0e8} .mo.f span{color:#7a7366}
.mo.r span{color:#8a96a0}
.legende{display:flex;gap:16px;margin-top:14px;font-size:13px;font-weight:700;color:#4f5d68}
.legende i{display:inline-block;width:12px;height:12px;border-radius:4px;margin-right:6px;vertical-align:-1px}
/* Tablets */
.tab{position:absolute;background:${F.tinte};border-radius:30px;padding:16px;z-index:3}
.tab .bs{background:${F.weiss};border-radius:18px;height:100%;padding:22px 22px;overflow:hidden}
.links{left:60px;top:300px;width:370px;height:500px;transform:rotate(-6deg)}
.rechts{left:1050px;top:390px;width:410px;height:350px;transform:rotate(5deg)}
.th{font-size:28px;line-height:1.08;color:${F.blau};margin-bottom:14px}
.th em{font-style:normal;color:${F.orange}}
.zeile{display:flex;gap:12px;align-items:center;background:#fff;border:1.5px solid ${F.linie};border-radius:14px;padding:10px 12px;margin-bottom:9px}
.zeile .i{flex:none;width:36px;height:36px;border-radius:10px;background:${F.creme};display:grid;place-items:center;font-size:19px}
.zeile b{display:block;font-size:17px}
.zeile span{font-size:14px;color:#4f5d68}
.haken{display:flex;gap:12px;align-items:flex-start;margin-bottom:12px;font-size:17px;font-weight:600;line-height:1.25}
.haken .k{flex:none;width:26px;height:26px;border-radius:8px;border:2px solid ${F.petrol};display:grid;place-items:center;color:#fff;font-size:15px;font-weight:800}
.haken .k.an{background:${F.petrol}}
.fokus{margin-top:6px;background:${F.creme};border-radius:12px;padding:10px 12px;font-size:15px;font-weight:700;color:${F.blau}}
.fokus em{font-style:normal;color:${F.orange}}
/* Handy: Kalenderblatt 1. Januar */
.handy{position:absolute;left:665px;top:470px;width:205px;height:400px;background:${F.tinte};border-radius:36px;padding:11px;transform:rotate(3deg);z-index:4}
.handy .bs{background:${F.creme};border-radius:27px;height:100%;padding:28px 16px 16px;display:flex;flex-direction:column;align-items:center;text-align:center}
.blatt{width:150px;border-radius:16px;overflow:hidden;background:#fff;box-shadow:0 8px 18px rgba(12,28,48,.18);position:relative}
.blatt .ring{position:absolute;top:-7px;width:12px;height:18px;border-radius:6px;background:${F.blau}}
.blatt .oben{background:${F.orange};color:#fff;font-weight:800;font-size:15px;letter-spacing:.14em;padding:12px 0 8px}
.blatt .tag{font-family:'Philosopher',serif;font-size:76px;line-height:1;color:${F.blau};padding:10px 0 2px}
.blatt .jahr{font-weight:800;font-size:17px;color:${F.petrol};padding-bottom:12px;letter-spacing:.08em}
.handy .t{font-size:26px;line-height:1.05;color:${F.blau};margin-top:18px}
.handy .t em{font-style:normal;color:${F.orange}}
.handy .klein{font-size:13px;font-weight:700;color:${F.petrol};margin-top:10px}
/* Aufkleber */
.kl{position:absolute;display:grid;place-items:center;text-align:center;border-radius:50%;z-index:5;font-weight:800}
.k1{left:290px;top:50px;width:160px;height:160px;background:${F.orange};color:#fff;transform:rotate(-10deg)}
.k2{left:1080px;top:140px;width:150px;height:150px;background:${F.petrol};color:#fff;transform:rotate(9deg)}
.kl .g{font-family:'Philosopher',serif;font-size:56px;line-height:.9}
.k2 .g{font-size:46px}
/* heller Rand, damit die dunklen Geräte auf der dunklen Seite sichtbar bleiben */
.lap .deckel,.tab,.handy{outline:2px solid rgba(241,236,221,.28);outline-offset:0}
.kl .s{font-size:16px;letter-spacing:.06em;text-transform:uppercase;line-height:1.15}
.preis{position:absolute;left:1165px;top:775px;z-index:6;background:${F.orange};color:#fff;border-radius:18px;padding:14px 26px;transform:rotate(-4deg);font-family:'Philosopher',serif;font-size:38px;font-weight:700;white-space:nowrap}
.preis small{font-family:'Source Sans 3';font-size:17px;font-weight:800;display:block;letter-spacing:.06em;text-transform:uppercase;opacity:.92}
/* Funken: Kern plus weicher Schein, dazu zwei Sternstrahlen */
.fu{position:absolute;border-radius:50%;background:radial-gradient(circle,#fff3e0 0,#ffc98a 35%,rgba(220,130,46,.35) 60%,rgba(220,130,46,0) 72%);transform:scale(2.6);z-index:1}
.stern{position:absolute;z-index:5;width:34px;height:34px}
.stern:before,.stern:after{content:"";position:absolute;left:50%;top:50%;background:#ffe2bd;border-radius:3px;box-shadow:0 0 10px rgba(220,130,46,.9)}
.stern:before{width:4px;height:34px;transform:translate(-50%,-50%)}
.stern:after{width:34px;height:4px;transform:translate(-50%,-50%)}
</style></head><body><div class="b">
${funkenHtml}

<div class="lap"><div class="deckel schatten"><div class="bs">
  <div class="kopf"><span class="marke">MEIN JAHRESPLAN</span><span class="pill">Leben zuerst eingetragen</span></div>
  <div class="titel ser">Sandras Jahr <em>2027</em></div>
  <div class="unter">Energie für Mamas ab 35 · ein Fokus pro Monat</div>
  <div class="raster">${monatHtml}</div>
  <div class="legende"><span><i style="background:${F.orange}"></i>Fokus-Angebot</span><span><i style="background:${F.petrol}"></i>Gratis-Angebot</span><span><i style="background:${F.grau}"></i>Familie und Ferien</span></div>
</div></div><div class="fuss"></div></div>

<div class="tab links schatten"><div class="bs">
  <div class="th ser">Was schon <em>feststeht</em></div>
  <div class="zeile"><span class="i">🏖️</span><div><b>Alle Schulferien</b><span>zuerst rein, dann das Business</span></div></div>
  <div class="zeile"><span class="i">🎂</span><div><b>Geburtstage und Feste</b><span>daran wird nicht gelauncht</span></div></div>
  <div class="zeile"><span class="i">☕</span><div><b>Deine Zeit für dich</b><span>jeden Mittwochmorgen</span></div></div>
  <div class="zeile"><span class="i">💛</span><div><b>Familienzeit im Dezember</b><span>ohne Verkauf</span></div></div>
</div></div>

<div class="tab rechts schatten"><div class="bs">
  <div class="th ser" style="font-size:26px">Dein <em>Januar</em>, Woche 1</div>
  <div class="haken"><span class="k an">✓</span>Gratis-Check fertig machen</div>
  <div class="haken"><span class="k an">✓</span>Montag, Mittwoch, Freitag posten</div>
  <div class="haken"><span class="k"></span>Ersten Monat im Kalender blocken</div>
  <div class="fokus">Fokus des Monats: <em>Gratis-Check</em></div>
</div></div>

<div class="handy schatten"><div class="bs">
  <div class="blatt"><i class="ring" style="left:38px"></i><i class="ring" style="right:38px"></i>
    <div class="oben">JANUAR</div><div class="tag">1</div><div class="jahr">2027</div></div>
  <div class="t ser">Dein <em>Neustart</em></div>
  <div class="klein">mit Plan statt mit Vorsätzen</div>
</div></div>

<div class="kl k1 schatten"><div><div class="s">Live am</div><div class="g">17.</div><div class="s">Dezember</div></div></div>
<div class="kl k2 schatten"><div><div class="g">2027</div><div class="s">auf einem<br>Blatt</div></div></div>
<div class="preis schatten"><small>Live-Workshop</small>gratis</div>
<span class="stern" style="left:240px;top:250px"></span>
<span class="stern" style="left:1260px;top:320px;transform:scale(.8)"></span>
<span class="stern" style="left:950px;top:20px;transform:scale(.7)"></span>
<span class="stern" style="left:560px;top:600px;transform:scale(.6)"></span>
</div></body></html>`;

writeFileSync(ZIEL + 'hero.html', html);
const browser = await puppeteer.launch({ headless: 'new' });
const seite = await browser.newPage();
await seite.setViewport({ width: 1500, height: 900, deviceScaleFactor: 1 });
await seite.goto('file:///' + ZIEL.replace(/\\/g, '/') + 'hero.html', { waitUntil: 'networkidle0' });
await seite.evaluate(() => document.fonts.ready);
await seite.screenshot({ path: ZIEL + 'hero.png', omitBackground: true, clip: { x: 0, y: 0, width: 1500, height: 900 } });
await browser.close();
console.log('→', ZIEL + 'hero.png');
