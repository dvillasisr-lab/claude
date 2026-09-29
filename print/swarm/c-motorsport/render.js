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
    await p.addStyleTag({ content: '.card::after{content:"";position:absolute;left:75px;top:75px;width:975px;height:525px;outline:1px solid rgba(0,255,255,.9);z-index:99;pointer-events:none}.card::before{content:"";position:absolute;left:37.5px;top:37.5px;width:1050px;height:600px;outline:1px solid rgba(255,0,255,.9);z-index:99}' });
    for (const id of ['front', 'back']) await p.locator('#' + id).screenshot({ path: `${dir}/guide-${id}.png` });
  }
  // report text bounding boxes outside safe zone
  const bad = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('.card').forEach(c => {
      const cr = c.getBoundingClientRect();
      c.querySelectorAll('[data-safe]').forEach(el => {
        const r = el.getBoundingClientRect();
        const x0 = r.left - cr.left, y0 = r.top - cr.top, x1 = r.right - cr.left, y1 = r.bottom - cr.top;
        const s = `${c.id} ${el.className || el.tagName} [${x0.toFixed(1)},${y0.toFixed(1)} → ${x1.toFixed(1)},${y1.toFixed(1)}]`;
        out.push((x0 < 75 || y0 < 75 || x1 > 1050 || y1 > 600 ? 'OUT ' : 'ok  ') + s);
      });
    });
    return out;
  });
  console.log(bad.join('\n'));
  const q = await b.newPage();
  await q.goto('file://' + dir + '/cards.html#print');
  await q.evaluate(() => document.fonts.ready);
  await q.waitForTimeout(400);
  await q.pdf({ path: dir + '/cards.pdf', width: '3.75in', height: '2.25in', printBackground: true, pageRanges: '1-2' });
  await b.close();
})();
