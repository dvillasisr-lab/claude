const { chromium } = require('playwright');
const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for (const f of ['logo-linea.svg','logo-apilado.svg']){
 const s=fs.readFileSync('/home/user/claude/print/swarm/assets/'+f,'utf8');
 await p.setContent(s.slice(s.indexOf('<svg')));
 const r=await p.evaluate(()=>{const svg=document.querySelector('svg');const bb=svg.getBBox();return [svg.getAttribute('viewBox'),bb.x,bb.y,bb.width,bb.height, [...svg.querySelectorAll('path')].map(p=>{const q=p.getBBox();return [q.x,q.y,q.width,q.height].map(Math.round)})]});
 console.log(f, JSON.stringify(r));
}
await b.close();})();
