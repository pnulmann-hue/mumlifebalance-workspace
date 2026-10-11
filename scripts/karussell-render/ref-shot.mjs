import puppeteer from 'puppeteer';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname,'..','..');
const OUT = path.join(ROOT,'scripts','karussell-render','_ref');
import fs from 'node:fs';
fs.mkdirSync(OUT,{recursive:true});
const targets = [
  ['mlb-home','https://www.mumlifebalance.ch/'],
  ['mlb-mba','https://www.mumlifebalance.ch/mba'],
  ['mlb-bootcamp','https://www.mumlifebalance.ch/bootcamp/'],
  ['unikati','https://unikati-digital.de/'],
];
const b = await puppeteer.launch({headless:'new',args:['--no-sandbox']});
for (const [name,url] of targets){
  try {
    const p = await b.newPage();
    await p.setViewport({width:1280,height:900,deviceScaleFactor:1});
    await p.goto(url,{waitUntil:'networkidle2',timeout:45000});
    await new Promise(r=>setTimeout(r,2500));
    const h = await p.evaluate(()=>document.body.scrollHeight);
    await p.screenshot({path:path.join(OUT,name+'.png'),clip:{x:0,y:0,width:1280,height:Math.min(h,5200)}});
    console.log('OK',name,'height',h);
    await p.close();
  } catch(e){ console.log('FAIL',name,e.message.slice(0,80)); }
}
await b.close();
