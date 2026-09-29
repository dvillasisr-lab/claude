const { chromium } = require('playwright');
const OUT = '/home/user/claude/print/swarm/r-iconic/round3';
const mode = process.argv[2] || '';
(async () => {
  const b = await chromium.launch({ args: ['--disable-lcd-text', '--font-render-hinting=none'] });
  const p = await b.newPage({ viewport: { width: 1200, height: 1450 }, deviceScaleFactor: 1 });
  await p.goto('file://' + OUT + '/cards.html');
  await p.waitForSelector('body[data-ready]'); await p.waitForTimeout(300);
  for (const id of ['front', 'back']) await p.locator('#' + id).screenshot({ path: `${OUT}/${id}.png` });
  const boxes = await p.evaluate(() => [...document.querySelectorAll('[data-safe]')].map(e => { const r = e.getBoundingClientRect(), c = e.closest('.card').getBoundingClientRect(); return [e.closest('.card').id, e.dataset.safe, Math.round(r.left - c.left), Math.round(r.top - c.top), Math.round(r.right - c.left), Math.round(r.bottom - c.top)] }));
  console.log(JSON.stringify(boxes)); require('fs').writeFileSync(OUT+'/work/boxes.json', JSON.stringify(boxes));
  await p.addStyleTag({ content: '.tractor,.light{visibility:hidden}' });
  for (const id of ['front', 'back']) await p.locator('#' + id).screenshot({ path: `${OUT}/work/ink-${id}.png` });
  if (mode !== 'nopdf') {
    const q = await b.newPage({ viewport: { width: 1125, height: 675 } });
    await q.goto('file://' + OUT + '/cards.html#print');
    await q.waitForSelector('body[data-ready]'); await q.waitForTimeout(300);
    await q.pdf({ path: OUT + '/work/cards-rgb.pdf', width: '3.75in', height: '2.25in', scale: 0.32, printBackground: true, pageRanges: '1-2' });
  }
  await b.close();
})();
