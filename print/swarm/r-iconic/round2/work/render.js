const { chromium } = require('playwright');
const OUT = '/home/user/claude/print/swarm/r-iconic/round2';
const mode = process.argv[2] || '';
(async () => {
  const b = await chromium.launch({ args: ['--disable-lcd-text', '--font-render-hinting=none', '--disable-font-subpixel-positioning'] });
  const p = await b.newPage({ viewport: { width: 1200, height: 1450 }, deviceScaleFactor: 1 });
  await p.goto('file://' + OUT + '/cards.html');
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  for (const id of ['front', 'back']) await p.locator('#' + id).screenshot({ path: `${OUT}/${id}.png` });
  // ink-only renders (no photo, no light) for safe-zone scanning
  await p.addStyleTag({ content: '.tractor,.light{visibility:hidden}' });
  for (const id of ['front', 'back']) await p.locator('#' + id).screenshot({ path: `${OUT}/work/ink-${id}.png` });
  await p.addStyleTag({ content: '.tractor,.light{visibility:visible}.card::after{content:"";position:absolute;left:75px;top:75px;width:975px;height:525px;outline:1px solid rgba(0,255,255,.8);z-index:99}.card::before{content:"";position:absolute;left:37.5px;top:37.5px;width:1050px;height:600px;outline:1px solid rgba(255,0,255,.8);z-index:99}' });
  for (const id of ['front', 'back']) await p.locator('#' + id).screenshot({ path: `${OUT}/work/guide-${id}.png` });
  if (mode !== 'nopdf') {
    const q = await b.newPage({ viewport: { width: 1125, height: 675 } });
    await q.goto('file://' + OUT + '/cards.html#print');
    await q.evaluate(() => document.fonts.ready); await q.waitForTimeout(400);
    await q.pdf({ path: OUT + '/cards.pdf', width: '3.75in', height: '2.25in', scale: 0.32, printBackground: true, pageRanges: '1-2' });
  }
  await b.close();
})();
