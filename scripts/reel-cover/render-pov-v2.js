const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  const htmlPath = path.resolve(__dirname, 'pov-dorf-cover-v2.html');
  const fileUrl = 'file:///' + htmlPath.split(path.sep).join('/');
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise(r => setTimeout(r, 1500));
  const outPath = path.resolve(__dirname, 'covers/pov-dorf-cover-v2.png');
  await page.screenshot({ path: outPath, type: 'png', omitBackground: false, fullPage: false });
  await browser.close();
  console.log('Saved:', outPath);
})();
