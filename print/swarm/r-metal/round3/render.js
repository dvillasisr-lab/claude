const { chromium } = require('playwright');
const dir = __dirname;
const html = process.argv[2] || 'cards.html';
const pre = process.argv[3] || '';
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1500 } });
  await p.goto('file://' + dir + '/' + html);
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  for (const id of ['front', 'back']) await p.locator('#' + id).screenshot({ path: `${dir}/${pre}${id}.png` });
  await p.addStyleTag({ content: '.card::after{content:"";position:absolute;left:75px;top:75px;width:975px;height:525px;outline:1px solid rgba(0,255,255,.9);z-index:99;pointer-events:none}.card::before{content:"";position:absolute;left:37.5px;top:37.5px;width:1050px;height:600px;outline:1px solid rgba(255,0,255,.9);z-index:99;pointer-events:none}' });
  for (const id of ['front', 'back']) await p.locator('#' + id).screenshot({ path: `${dir}/${pre}guide-${id}.png` });
  const rep = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('.card').forEach(c => {
      const cr = c.getBoundingClientRect();
      c.querySelectorAll('[data-safe]').forEach(el => {
        let r = el.getBoundingClientRect();
        if (el.tagName.toLowerCase() === 'svg' && el.querySelector('path')) { // true glyph bbox
          const rs=[...el.querySelectorAll('path')].map(q=>q.getBoundingClientRect());
          r={left:Math.min(...rs.map(q=>q.left)),top:Math.min(...rs.map(q=>q.top)),right:Math.max(...rs.map(q=>q.right)),bottom:Math.max(...rs.map(q=>q.bottom))};
        }
        const x0 = r.left - cr.left, y0 = r.top - cr.top, x1 = r.right - cr.left, y1 = r.bottom - cr.top;
        const fs = parseFloat(getComputedStyle(el).fontSize);
        out.push((x0 < 75 || y0 < 75 || x1 > 1050 || y1 > 600 ? 'OUT ' : 'ok  ') + `${c.id} ${el.dataset.safe||el.className.baseVal||el.className} [${x0.toFixed(1)},${y0.toFixed(1)} -> ${x1.toFixed(1)},${y1.toFixed(1)}] fs=${fs}`);
      });
      c.querySelectorAll('*').forEach(el=>{ if(el.childNodes.length && [...el.childNodes].some(n=>n.nodeType==3&&n.textContent.trim())){const fs=parseFloat(getComputedStyle(el).fontSize); if(fs<24) out.push('SMALL '+c.id+' '+fs+' '+el.textContent.trim().slice(0,30));}});
    });
    return out;
  });
  console.log(rep.join('\n'));
  await p.addStyleTag({ content: '.card::after,.card::before{display:none!important}.tractor,.sun,.ground,.post{visibility:hidden!important}' });
  for (const id of ['front', 'back']) await p.locator('#' + id).screenshot({ path: `${dir}/scan-${id}.png` });
  const q = await b.newPage();
  await q.goto('file://' + dir + '/' + html + '#print');
  await q.evaluate(() => document.fonts.ready); await q.waitForTimeout(400);
  await q.pdf({ path: dir + '/' + pre + 'cards-rgb.pdf', width: '3.75in', height: '2.25in', printBackground: true, pageRanges: '1-2' });
  await b.close();
})();
