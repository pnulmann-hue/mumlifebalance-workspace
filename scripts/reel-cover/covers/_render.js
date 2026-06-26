
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await page.goto('file:///C:/Users/pnulm/Desktop/Mein Business/scripts/reel-cover/covers/_work_next-level-shit.html', { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise(r => setTimeout(r, 1000));
  await page.screenshot({ path: 'C:/Users/pnulm/Desktop/Mein Business/scripts/reel-cover/covers/next-level-shit-201.png', type: 'png', omitBackground: false, fullPage: false });
  await browser.close();
})();
