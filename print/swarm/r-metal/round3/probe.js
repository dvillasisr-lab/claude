const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1200,height:1500}});
  await p.goto('file://' + __dirname + '/cards.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  const r = await p.evaluate(() => {
    const out=[];
    document.querySelectorAll('.card').forEach(c=>{const cr=c.getBoundingClientRect();
      c.querySelectorAll('[data-safe]').forEach(el=>{ if(el.tagName.toLowerCase()=='svg')return;
        const walker=document.createTreeWalker(el,NodeFilter.SHOW_TEXT); let n; const bl=[];
        while(n=walker.nextNode()){ if(!n.textContent.trim())continue; const s=document.createElement('span'); s.style.cssText='display:inline-block;width:0;height:0;vertical-align:baseline'; n.parentNode.insertBefore(s,n.nextSibling); bl.push(Math.round((s.getBoundingClientRect().top-cr.top)*10)/10); s.remove(); }
        out.push(c.id+' '+el.dataset.safe+' baselines '+[...new Set(bl)].join(','));
      });});
    return out.join('\n');});
  console.log(r); await b.close();
})();
