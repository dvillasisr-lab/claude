const { chromium } = require('playwright');
const dir='/home/user/claude/print/swarm/b-machined', S=process.argv[2];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:1500}});
await p.goto('file://'+dir+'/cards.html#guides');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
for(const id of ['front','back']) await p.locator('#'+id).screenshot({path:`${S}/g-${id}.png`});
const r=await p.evaluate(()=>[...document.querySelectorAll('#front *,#back *')].filter(e=>e.dataset.chk!==undefined||e.matches('.logo,.col,.emb,.evil,.mono,.qr,.name,.row,.tag')).map(e=>{const c=e.closest('.card').getBoundingClientRect(),r=e.getBoundingClientRect();return [e.closest('.card').id,e.className.baseVal??e.className,Math.round(r.left-c.left),Math.round(r.top-c.top),Math.round(r.right-c.left),Math.round(r.bottom-c.top)].join(' ')}));
console.log(r.join('\n'));await b.close()})();
