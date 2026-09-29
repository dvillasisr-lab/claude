const { chromium } = require('playwright');
const dir = __dirname;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1500 } });
  await p.goto('file://' + dir + '/cards.html');
  await p.waitForSelector('body[data-ready="1"]');
  await p.waitForTimeout(300);
  for (const id of ['front', 'back']) await p.locator('#' + id).screenshot({ path: `${dir}/${id}.png` });
  const rep = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('.card').forEach(c => {
      const cr = c.getBoundingClientRect();
      c.querySelectorAll('[data-safe]').forEach(el => {
        const r = el.getBoundingClientRect();
        const x0 = r.left - cr.left, y0 = r.top - cr.top, x1 = r.right - cr.left, y1 = r.bottom - cr.top;
        out.push((x0 < 75 || y0 < 75 || x1 > 1050 || y1 > 600 ? 'OUT ' : 'ok  ') + `${c.id} ${el.id || el.textContent.slice(0, 18)} [${x0.toFixed(1)},${y0.toFixed(1)} -> ${x1.toFixed(1)},${y1.toFixed(1)}]`);
      });
    });
    return out;
  });
  console.log(rep.join('\n'));
  if (process.argv[2] !== 'nopdf') {
    const q = await b.newPage();
    await q.goto('file://' + dir + '/cards.html#print');
    await q.waitForSelector('body[data-ready="1"]');
    await q.waitForTimeout(300);
    await q.pdf({ path: dir + '/cards-rgb.pdf', width: '3.75in', height: '2.25in', printBackground: true, pageRanges: '1-2', scale: 0.32 });
  }
  await b.close();
})();
