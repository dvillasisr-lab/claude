const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1200,height:1500}});
  await p.goto('file://' + __dirname + '/cards.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.locator('#'+(process.argv[3]||'front')).screenshot({ path: process.argv[2] }); await b.close();
})();
