// Convierte html/*.html en out/*.png (1080x1080, nitido en WhatsApp).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = __dirname, out = path.join(dir, 'out');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: 1 });
  for (const f of fs.readdirSync(path.join(dir, 'html')).filter(f => f.endsWith('.html')).sort()) {
    await page.goto('file://' + path.join(dir, 'html', f));
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(out, f.replace('.html', '.png')) });
    console.log('ok', f);
  }
  await browser.close();
})();
