// Rasteriza las gráficas SVG del deck a PNG para el PPTX: node deck_raster.js <html> <outdir> <ids...>
const { chromium } = require('playwright');
(async () => {
  const [html, out, ...ids] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1600, height: 1200 }, deviceScaleFactor: 2 });
  await p.goto('file://' + html);
  await p.waitForTimeout(1200);
  for (const i of ids) {
    const el = await p.$('#r' + i);
    await el.screenshot({ path: `${out}/r${i}.png` });
  }
  await b.close();
})();
