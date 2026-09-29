const { chromium } = require('playwright');
const dir = __dirname;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1500 } });
  await p.goto('file://' + dir + '/cards.html');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  for (const id of ['front', 'back']) await p.locator('#' + id).screenshot({ path: `${dir}/${id}.png` });
  if (process.argv[2] === 'guides') {
    await p.addStyleTag({ content: '.card::after{content:"";position:absolute;left:75px;top:75px;width:975px;height:525px;outline:1px solid rgba(0,255,255,.8);z-index:99;pointer-events:none}.card::before{content:"";position:absolute;left:37.5px;top:37.5px;width:1050px;height:600px;outline:1px solid rgba(255,0,255,.8);z-index:99}' });
    for (const id of ['front', 'back']) await p.locator('#' + id).screenshot({ path: `${dir}/guide-${id}.png` });
  }
  const q = await b.newPage();
  await q.goto('file://' + dir + '/cards.html#print');
  await q.evaluate(() => document.fonts.ready);
  await q.waitForTimeout(400);
  await q.pdf({ path: dir + '/cards.pdf', width: '3.75in', height: '2.25in', printBackground: true, pageRanges: '1-2' });
  await b.close();
})();
