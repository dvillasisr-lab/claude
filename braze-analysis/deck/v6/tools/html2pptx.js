// Convierte DECK_v6.html a PPTX: texto, cajas, líneas y tablas quedan nativos y editables;
// cada gráfica SVG entra como imagen PNG a alta resolución. Las láminas "oculta" quedan ocultas en PowerPoint.
// Uso: NODE_PATH=<node_modules con playwright y pptxgenjs> node html2pptx.js entrada.html salida.pptx
const { chromium } = require('playwright');
const pptxgen = require('pptxgenjs');
const fs = require('fs');

const [, , IN, OUT] = process.argv;
const W_IN = 13.333, H_IN = 7.5;

// Corre dentro del navegador: describe cada lámina como lista de rectángulos, líneas, textos e imágenes
function extract() {
  const out = [];
  const rgba = (c) => {
    const m = c && c.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(',').map((x) => parseFloat(x));
    const a = p.length > 3 ? p[3] : 1;
    if (a === 0) return null;
    const hex = p.slice(0, 3).map((v) => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();
    return { hex, a };
  };
  const INLINE = new Set(['inline', 'inline-block', 'contents']);
  const isInline = (el) => INLINE.has(getComputedStyle(el).display) && el.tagName !== 'svg' && el.tagName !== 'BR';
  const tf = (s, t) => (t === 'uppercase' ? s.toUpperCase() : s);
  document.querySelectorAll('section.slide').forEach((sl) => {
    const R = sl.getBoundingClientRect();
    const sc = 13.333 / R.width; // pulgadas por px
    const box = (r) => ({ x: (r.left - R.left) * sc, y: (r.top - R.top) * sc, w: r.width * sc, h: r.height * sc });
    const items = [];
    const bg = rgba(getComputedStyle(sl).backgroundColor);
    const runsOf = (el) => {
      const runs = [];
      const walk = (n) => {
        if (n.nodeType === 3) {
          const p = n.parentElement, cs = getComputedStyle(p);
          let t = n.textContent.replace(/\s+/g, ' ');
          if (!t) return;
          const c = rgba(cs.color) || { hex: '000000', a: 1 };
          runs.push({ t: tf(t, cs.textTransform), b: parseInt(cs.fontWeight) >= 600, i: cs.fontStyle === 'italic',
            c: c.hex, ca: c.a, fs: parseFloat(cs.fontSize) * sc * 72, ls: (parseFloat(cs.letterSpacing) || 0) * sc * 72 });
        } else if (n.nodeType === 1) {
          if (n.tagName === 'BR') { runs.push({ br: true }); return; }
          n.childNodes.forEach(walk);
        }
      };
      el.childNodes.forEach(walk);
      // limpia espacios al inicio y al final
      while (runs.length && !runs[0].br && !runs[0].t.trim()) runs.shift();
      if (runs.length && runs[0].t) runs[0].t = runs[0].t.replace(/^\s+/, '');
      while (runs.length && runs[runs.length - 1].t !== undefined && !runs[runs.length - 1].t.trim()) runs.pop();
      if (runs.length && runs[runs.length - 1].t) runs[runs.length - 1].t = runs[runs.length - 1].t.replace(/\s+$/, '');
      return runs;
    };
    const textItem = (el, r, runs) => {
      const cs = getComputedStyle(el);
      const pl = parseFloat(cs.paddingLeft), pr = parseFloat(cs.paddingRight), pt = parseFloat(cs.paddingTop), pb = parseFloat(cs.paddingBottom);
      const bl = parseFloat(cs.borderLeftWidth) || 0;
      const rr = { left: r.left + pl + bl, top: r.top + pt, width: r.width - pl - pr - bl, height: r.height - pt - pb };
      const fsz = parseFloat(cs.fontSize);
      const lh = cs.lineHeight === 'normal' ? 1.2 : parseFloat(cs.lineHeight) / fsz;
      const flex = cs.display.includes('flex');
      const al = flex && cs.justifyContent === 'center' ? 'center' : cs.textAlign === 'right' || cs.textAlign === 'end' ? 'right' : cs.textAlign === 'center' ? 'center' : 'left';
      const va = flex && cs.alignItems === 'center' ? 'middle' : 'top';
      items.push({ k: 'text', ...box(rr), runs, al, va, lh });
    };
    const visit = (el) => {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return;
      if (el.tagName.toLowerCase() === 'svg') {
        items.push({ k: 'img', ...box(r), sel: true, idx: [...sl.querySelectorAll('svg')].indexOf(el) });
        return;
      }
      if (el !== sl) {
        const b = rgba(cs.backgroundColor);
        if (b) items.push({ k: 'rect', ...box(r), fill: b.hex, tr: Math.round((1 - b.a) * 100), rad: parseFloat(cs.borderTopLeftRadius) >= r.width / 2 - 1 ? 'ell' : '' });
        for (const [side, x1, y1, x2, y2] of [['Top', r.left, r.top, r.right, r.top], ['Bottom', r.left, r.bottom, r.right, r.bottom],
          ['Left', r.left, r.top, r.left, r.bottom], ['Right', r.right, r.top, r.right, r.bottom]]) {
          const wv = parseFloat(cs['border' + side + 'Width']);
          const bc = rgba(cs['border' + side + 'Color']);
          if (wv > 0 && bc && cs['border' + side + 'Style'] !== 'none') {
            const off = (wv / 2) * (side === 'Top' || side === 'Left' ? 1 : -1);
            const hz = side === 'Top' || side === 'Bottom';
            items.push({ k: 'line', x1: (x1 - R.left + (hz ? 0 : off)) * sc, y1: (y1 - R.top + (hz ? off : 0)) * sc,
              x2: (x2 - R.left + (hz ? 0 : off)) * sc, y2: (y2 - R.top + (hz ? off : 0)) * sc, c: bc.hex, w: wv * sc * 72,
              dash: cs['border' + side + 'Style'] === 'dashed' });
          }
        }
        // numerito de las listas (::before con contador)
        const ps = getComputedStyle(el, '::before');
        if (ps.content && ps.content !== 'none' && ps.content !== 'normal' && el.tagName === 'LI') {
          const pw = parseFloat(ps.width), ph = parseFloat(ps.height);
          const px = r.left + (parseFloat(ps.left) || 0), py = r.top + (parseFloat(ps.top) || 0);
          const pb = rgba(ps.backgroundColor), pc = rgba(ps.color);
          const ol = el.parentElement;
          const q = ps.content.match(/^"(.*)"$/);
          const n = ps.content.startsWith('counter') ? String([...ol.children].indexOf(el) + 1) : q ? q[1] : '';
          if (pw > 0) items.push({ k: 'dot', x: (px - R.left) * sc, y: (py - R.top) * sc, w: pw * sc, h: ph * sc,
            fill: pb ? pb.hex : null, c: pc ? pc.hex : '000000', fs: parseFloat(ps.fontSize) * sc * 72, n, rad: parseFloat(ps.borderTopLeftRadius) >= pw / 2 - 1 });
        }
      }
      const kids = [...el.childNodes];
      const blockKids = kids.filter((n) => n.nodeType === 1 && !isInline(n));
      const hasText = kids.some((n) => (n.nodeType === 3 && n.textContent.trim()) || (n.nodeType === 1 && isInline(n) && n.textContent.trim()));
      if (!blockKids.length) {
        if (hasText && el !== sl) { const runs = runsOf(el); if (runs.length) textItem(el, r, runs); }
        return;
      }
      // mezcla de texto suelto y bloques: cada tramo de texto suelto va en su propia caja
      let group = [];
      const flush = () => {
        if (!group.length) return;
        const rg = document.createRange(); rg.setStartBefore(group[0]); rg.setEndAfter(group[group.length - 1]);
        const gr = rg.getBoundingClientRect();
        const tmp = document.createElement('span'); group.forEach((n) => tmp.appendChild(n.cloneNode(true)));
        const runs = []; const pcs = getComputedStyle(el);
        const walk = (n, p) => {
          if (n.nodeType === 3) { const t = n.textContent.replace(/\s+/g, ' '); if (!t) return; const cs2 = getComputedStyle(p); const c = rgba(cs2.color) || { hex: '000000' };
            runs.push({ t: tf(t, cs2.textTransform), b: parseInt(cs2.fontWeight) >= 600, c: c.hex, fs: parseFloat(cs2.fontSize) * sc * 72, ls: (parseFloat(cs2.letterSpacing) || 0) * sc * 72 }); }
          else if (n.nodeType === 1) n.childNodes.forEach((m) => walk(m, n));
        };
        group.forEach((n) => walk(n, n.nodeType === 1 ? n : el));
        if (runs.length) { runs[0].t = runs[0].t.replace(/^\s+/, ''); runs[runs.length - 1].t = runs[runs.length - 1].t.replace(/\s+$/, ''); }
        if (runs.some((x) => x.t && x.t.trim()) && gr.width > 0)
          items.push({ k: 'text', ...box({ left: gr.left, top: gr.top, width: gr.width, height: gr.height }), runs,
            al: pcs.textAlign === 'right' ? 'right' : pcs.textAlign === 'center' ? 'center' : 'left',
            lh: pcs.lineHeight === 'normal' ? 1.2 : parseFloat(pcs.lineHeight) / parseFloat(pcs.fontSize) });
        group = [];
      };
      kids.forEach((n) => {
        if (n.nodeType === 1 && !isInline(n)) { flush(); visit(n); }
        else if (n.nodeType === 3 || n.nodeType === 1) group.push(n);
      });
      flush();
    };
    visit(sl);
    const num = sl.querySelector('.src span:last-child');
    out.push({ id: sl.id, bg: bg ? bg.hex : 'FFFFFF', hidden: sl.classList.contains('oculta'), items,
      title: (sl.querySelector('h1,h2') || {}).textContent || '', divisor: sl.classList.contains('divisor'), num: num ? num.textContent : '' });
  });
  return out;
}

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1312, height: 900 }, deviceScaleFactor: 3 });
  await p.goto('file://' + require('path').resolve(IN));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(1200);
  const slides = await p.evaluate(extract);
  // imágenes de las gráficas
  for (const s of slides) {
    for (const it of s.items.filter((x) => x.k === 'img')) {
      const el = (await p.$$(`#${s.id} svg`))[it.idx];
      const buf = await el.screenshot({ omitBackground: false });
      it.data = 'image/png;base64,' + buf.toString('base64');
    }
  }
  await b.close();

  const pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE';
  pres.title = 'Braze en Kueski';
  pres.theme = { headFontFace: 'Inter', bodyFontFace: 'Inter' };
  let sec = 'Inicio';
  pres.addSection({ title: sec });
  const hidden = [];
  slides.forEach((s, i) => {
    if (s.divisor) { sec = s.title.slice(0, 60); pres.addSection({ title: sec }); }
    const sl = pres.addSlide({ sectionTitle: sec });
    sl.background = { color: s.bg };
    if (s.hidden) hidden.push(i + 1);
    for (const it of s.items) {
      if (it.k === 'rect') {
        sl.addShape(it.rad ? pres.ShapeType.ellipse : pres.ShapeType.rect, { x: it.x, y: it.y, w: it.w, h: it.h,
          fill: { color: it.fill, transparency: it.tr }, line: { type: 'none' } });
      } else if (it.k === 'line') {
        sl.addShape(pres.ShapeType.line, { x: Math.min(it.x1, it.x2), y: Math.min(it.y1, it.y2), w: Math.abs(it.x2 - it.x1), h: Math.abs(it.y2 - it.y1),
          line: { color: it.c, width: Math.max(it.w, 0.5), dashType: it.dash ? 'dash' : 'solid' } });
      } else if (it.k === 'dot') {
        if (it.fill) sl.addShape(it.rad ? pres.ShapeType.ellipse : pres.ShapeType.rect, { x: it.x, y: it.y, w: it.w, h: it.h, fill: { color: it.fill }, line: { type: 'none' } });
        if (it.n) sl.addText(it.n, { x: it.x, y: it.y, w: it.w, h: it.h, fontSize: it.fs, bold: true, color: it.c, align: 'center', valign: 'middle',
          margin: 0, isTextBox: true, fontFace: 'Inter' });
      } else if (it.k === 'img') {
        sl.addImage({ data: it.data, x: it.x, y: it.y, w: it.w, h: it.h });
      } else if (it.k === 'text') {
        const runs = [];
        it.runs.forEach((r, j) => {
          if (r.br) { if (runs.length) runs[runs.length - 1].options.breakLine = true; return; }
          runs.push({ text: r.t, options: { bold: r.b, italic: r.i, color: r.c, fontSize: Math.round(r.fs * 10) / 10,
            charSpacing: r.ls ? Math.round(r.ls * 10) / 10 : undefined, fontFace: 'Inter' } });
        });
        if (!runs.length) continue;
        // un poco de holgura: PowerPoint corta líneas un pelo antes que el navegador
        sl.addText(runs, { x: it.x, y: it.y, w: it.w * 1.03 + 0.02, h: it.h, margin: 0, valign: it.va || 'top', align: it.al,
          lineSpacingMultiple: Math.round(it.lh / 1.21 * 100) / 100, isTextBox: true, fit: 'none', autoFit: false });
      }
    }
  });
  await pres.writeFile({ fileName: OUT });
  fs.writeFileSync(OUT + '.ocultas.json', JSON.stringify(hidden));
  console.log(OUT, slides.length, 'láminas; ocultas:', hidden.join(','));
})();
