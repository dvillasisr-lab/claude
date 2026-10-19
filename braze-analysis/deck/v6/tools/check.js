// Uso: NODE_PATH=/opt/node-tools/node_modules node check.js lamina.html salida.png
// Revisa una lámina armada con deck_v6_render.py --solo: texto que se sale, bloques encimados y textos SVG encimados.
const { chromium } = require('playwright');
(async () => {
  const [,, file, png] = process.argv;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  await p.goto('file://' + require('path').resolve(file)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(800);
  const r = await p.$eval('.slide', s => {
    const out = []; const R = s.getBoundingClientRect();
    const sw = s.querySelector('.sw'); const lim = sw ? sw.getBoundingClientRect().top : R.bottom;
    s.querySelectorAll('.ex, .side, .grid3, .hx, .ctx').forEach(e => { const q = e.getBoundingClientRect(); if (q.bottom > lim + 1) out.push('SE ENCIMA CON SO WHAT: ' + e.className + ' +' + Math.round(q.bottom - lim) + 'px'); if (e.scrollHeight > e.clientHeight + 2) out.push('TEXTO CORTADO en ' + e.className); });
    s.querySelectorAll('.s *').forEach(e => { const q = e.getBoundingClientRect(); if (q.height && (q.right > R.right + 1 || q.bottom > R.bottom + 1)) out.push('SE SALE: ' + e.tagName); });
    const svg = s.querySelector('.ex svg');
    if (svg) { const ts = [...svg.querySelectorAll('text')].map(t => ({ t: t.textContent.trim(), r: t.getBoundingClientRect() })).filter(x => x.t && x.r.width);
      const sr = svg.getBoundingClientRect();
      for (const a of ts) if (a.r.right > sr.right + 1 || a.r.left < sr.left - 1) out.push('TEXTO FUERA DEL SVG: ' + a.t.slice(0, 30));
      for (let i = 0; i < ts.length; i++) for (let j = i + 1; j < ts.length; j++) { const A = ts[i].r, B = ts[j].r; const ox = Math.min(A.right, B.right) - Math.max(A.left, B.left), oy = Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top); if (ox > 1.5 && oy > 1.5) out.push('TEXTOS ENCIMADOS: "' + ts[i].t.slice(0, 20) + '" / "' + ts[j].t.slice(0, 20) + '"'); }
      const fs = [...svg.querySelectorAll('text')].map(t => t.getBoundingClientRect().height).filter(Boolean); }
    return [...new Set(out)];
  });
  await (await p.$('.slide')).screenshot({ path: png });
  console.log(r.length ? r.join('\n') : 'OK sin problemas'); await b.close();
})();
