import puppeteer from '/home/user/mumlifebalance-workspace/scripts/karussell-render/node_modules/puppeteer/lib/esm/puppeteer/puppeteer.js';
import { fileURLToPath } from 'url';
import path from 'path';
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await puppeteer.launch({ headless:'new', args:['--no-sandbox','--disable-setuid-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width:1080, height:1920, deviceScaleFactor:2 });
await page.goto('file://'+path.join(__dirname,'prompt-mockups.html'), { waitUntil:'networkidle0' });
await new Promise(r=>setTimeout(r,1200)); // fonts
const cards = await page.$$('.chat');
for (let i=0;i<cards.length;i++){
  await cards[i].screenshot({ path: path.join(__dirname, `mockup-${i+1}.png`), omitBackground:true });
  console.log('rendered mockup-'+(i+1)+'.png');
}
await browser.close();
