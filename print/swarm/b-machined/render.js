const { chromium } = require('playwright');
const dir='/home/user/claude/print/swarm/b-machined';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:1500}});
await p.goto('file://'+dir+'/cards.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
for(const id of ['front','back']) await p.locator('#'+id).screenshot({path:`${dir}/${id}.png`});
const q=await b.newPage();await q.goto('file://'+dir+'/cards.html#print');await q.evaluate(()=>document.fonts.ready);await q.waitForTimeout(600);
await q.pdf({path:dir+'/cards.pdf',width:'3.75in',height:'2.25in',printBackground:true,pageRanges:'1-2'});await b.close()})();
